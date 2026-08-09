#include "app_tasks.h"

#include <math.h>
#include <string.h>

#include "board_config.h"

#include "esp_log.h"
#include "esp_timer.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"

#include "esp_task_wdt.h"

#include "utils/psram_alloc.h"
#include "utils/ringbuf_psram.h"

#include "drivers/adxl355.h"
#include "drivers/inmp441.h"
#include "drivers/thermal_adc.h"
#include "drivers/status_led_ws2812.h"
#include "drivers/modbus_stack.h"

#include "dsp/vibration_metrics.h"
#include "app/state_machine.h"
#include "net/wifi_prov_mgr.h"
#include "net/mqtt_client_mgr.h"

static const char *TAG = "app_tasks";

typedef struct {
    float vib_rms_g;
    float vib_peak_g;
    float vib_crest;
    float temp_c;
} machine_health_msg_t;

static QueueHandle_t s_q_health;

static ringbuf_psram_t s_vib_mag_rb;

static adxl355_t s_adxl;
static inmp441_t s_mic;
static thermal_adc_t s_therm;
static status_led_ws2812_t s_led;
static modbus_stack_t s_modbus;
static mqtt_client_mgr_t s_mqtt;
static machine_state_machine_t s_sm;

static uint32_t now_ms(void)
{
    return (uint32_t)(esp_timer_get_time() / 1000ULL);
}

static void on_state_change(machine_state_t st, void *user_ctx)
{
    (void)user_ctx;
    if (st == MACHINE_STATE_NORMAL) {
        (void)status_led_ws2812_set_solid(&s_led, (status_led_rgb_t){ .r = 0, .g = 32, .b = 0 });
    } else if (st == MACHINE_STATE_WARNING) {
        (void)status_led_ws2812_set_solid(&s_led, (status_led_rgb_t){ .r = 32, .g = 16, .b = 0 });
    } else {
        (void)status_led_ws2812_set_blink(&s_led, (status_led_rgb_t){ .r = 48, .g = 0, .b = 0 }, 500);
    }
}

static void task_vibration(void *arg)
{
    (void)arg;

    const size_t window = 256;
    float *window_buf = (float *)psram_alloc(window * sizeof(float), 16, true);
    if (!window_buf) {
        ESP_LOGE(TAG, "no mem for vibration window");
        vTaskDelete(NULL);
        return;
    }

    vibration_metrics_t m = {0};

    uint32_t last_pub = now_ms();
    while (1) {
        (void)esp_task_wdt_reset();
        adxl355_accel_g_t a;
        esp_err_t e = adxl355_read_accel_g(&s_adxl, &a);
        if (e == ESP_OK) {
            float mag = sqrtf(a.ax_g * a.ax_g + a.ay_g * a.ay_g + a.az_g * a.az_g);
            (void)ringbuf_psram_push(&s_vib_mag_rb, &mag);
        }

        // Every 100ms compute from the latest window
        uint32_t nnow = now_ms();
        if ((nnow - last_pub) >= BOARD_VIBRATION_METRICS_PERIOD_MS) {
            last_pub = nnow;

            // Pull up to window samples (non-blocking)
            size_t got = 0;
            float tmp;
            while (got < window && ringbuf_psram_pop(&s_vib_mag_rb, &tmp)) {
                window_buf[got++] = tmp;
            }

            if (got > 0) {
                (void)vibration_metrics_compute(window_buf, got, &m);

                machine_health_msg_t msg = {
                    .vib_rms_g = m.rms_g,
                    .vib_peak_g = m.peak_g,
                    .vib_crest = m.crest_factor,
                    .temp_c = NAN,
                };
                (void)xQueueOverwrite(s_q_health, &msg);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

static void task_state_machine(void *arg)
{
    (void)arg;

    machine_health_msg_t msg;
    while (1) {
        (void)esp_task_wdt_reset();
        if (xQueueReceive(s_q_health, &msg, pdMS_TO_TICKS(200)) == pdTRUE) {
            // read temp
            float tc = 0;
            if (thermal_adc_read_temp_c(&s_therm, &tc) == ESP_OK) {
                msg.temp_c = tc;
            }

            // Convert vib RMS g -> mm/s placeholder (needs calibration/integration model)
            // For now expose g-based RMS * 1000 as scaled mm/s-ish.
            float vib_mm_s = msg.vib_rms_g * 1000.0f;

            machine_health_inputs_t in = {
                .vib_rms_mm_s = vib_mm_s,
                .temp_c = msg.temp_c,
            };
            (void)machine_sm_update(&s_sm, &in);

            // Update a few Modbus input regs (simple scaling)
            // 30001: vib_rms*10
            (void)modbus_stack_set_input_reg(&s_modbus, 30001, (uint16_t)(vib_mm_s * 10));
            // 30002: temp*10
            if (!isnan(msg.temp_c)) {
                (void)modbus_stack_set_input_reg(&s_modbus, 30002, (uint16_t)(msg.temp_c * 10));
            }
        }

        status_led_ws2812_tick(&s_led, now_ms());
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

static void task_comms(void *arg)
{
    (void)arg;

    uint32_t last_pub = now_ms();

    while (1) {
        (void)modbus_stack_poll(&s_modbus);

        // Comms task is not watchdog-critical by default

        uint32_t nnow = now_ms();
        if ((nnow - last_pub) >= BOARD_MQTT_PUBLISH_PERIOD_MS) {
            last_pub = nnow;

            if (mqtt_client_mgr_is_connected(&s_mqtt)) {
                // Publish minimal JSON from Modbus registers
                // TODO: publish richer metrics
                const char *json = "{\"msg\":\"telemetry\"}";
                (void)mqtt_client_mgr_publish_json(&s_mqtt, "telemetry", json);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

esp_err_t app_tasks_start(void)
{
    psram_alloc_init();

    // Queue: overwrite semantics (latest value)
    s_q_health = xQueueCreate(1, sizeof(machine_health_msg_t));
    if (!s_q_health) {
        return ESP_ERR_NO_MEM;
    }

    ESP_ERROR_CHECK(ringbuf_psram_init(&s_vib_mag_rb, 1024, sizeof(float), RINGBUF_OVERFLOW_DROP_OLDEST, true));

    // Init drivers
    adxl355_config_t acfg = {
        .host = BOARD_ADXL355_SPI_HOST,
        .gpio_cs = BOARD_ADXL355_GPIO_CS,
        .gpio_sck = BOARD_ADXL355_GPIO_SCK,
        .gpio_mosi = BOARD_ADXL355_GPIO_MOSI,
        .gpio_miso = BOARD_ADXL355_GPIO_MISO,
        .spi_mode = BOARD_ADXL355_SPI_MODE,
        .clock_hz = BOARD_ADXL355_SPI_CLOCK_HZ,
        .spi_queue_size = 2,
        .timeout_ms = 50,
        .max_consecutive_timeouts = 5,
    };
    ESP_ERROR_CHECK(adxl355_init(&s_adxl, &acfg));

    inmp441_config_t mcfg = {
        .i2s_port = BOARD_INMP441_I2S_PORT,
        .gpio_bclk = BOARD_INMP441_GPIO_BCLK,
        .gpio_ws = BOARD_INMP441_GPIO_WS,
        .gpio_din = BOARD_INMP441_GPIO_DIN,
        .sample_rate_hz = BOARD_INMP441_SAMPLE_RATE_HZ,
        .bits_per_sample = BOARD_INMP441_BITS_PER_SAMPLE,
        .dma_frame_bytes = 512,
        .dma_desc_num = 4,
        .read_timeout_ms = 50,
    };
    ESP_ERROR_CHECK(inmp441_init(&s_mic, &mcfg));

    thermal_adc_config_t tcfg = {
        .adc_unit = BOARD_THERMAL_ADC_UNIT,
        .adc_channel = BOARD_THERMAL_ADC_CHANNEL,
        .atten = BOARD_THERMAL_ADC_ATTEN,
        .bitwidth = BOARD_THERMAL_ADC_BITWIDTH,
        .offset_mv = 500.0f,
        .scale_c_per_mv = 0.1f,
    };
    ESP_ERROR_CHECK(thermal_adc_init(&s_therm, &tcfg));

    status_led_ws2812_config_t lcfg = {
        .gpio = BOARD_STATUS_LED_GPIO,
        .rmt_resolution_hz = 10 * 1000 * 1000,
        .use_dma = true,
    };
    ESP_ERROR_CHECK(status_led_ws2812_init(&s_led, &lcfg));

    modbus_stack_config_t bcfg = {
        .uart_num = BOARD_MODBUS_UART_NUM,
        .gpio_tx = BOARD_MODBUS_GPIO_TX,
        .gpio_rx = BOARD_MODBUS_GPIO_RX,
        .gpio_de = BOARD_MODBUS_GPIO_DE,
        .baudrate = BOARD_MODBUS_BAUDRATE,
        .slave_id = 1,
    };
    ESP_ERROR_CHECK(modbus_stack_init(&s_modbus, &bcfg));

    (void)vibration_metrics_init();

    machine_sm_init(&s_sm, on_state_change, NULL);
    on_state_change(MACHINE_STATE_NORMAL, NULL);

    // Start provisioning (non-blocking; will connect if already provisioned)
    wifi_prov_mgr_app_config_t pcfg = {
        .service_name = "mech-sentinel",
        .service_key = NULL,
        .pop = "esp32s3-pop",
        .enable_reprovisioning = true,
    };
    ESP_ERROR_CHECK(wifi_prov_mgr_app_start(&pcfg));

    // Start MQTT (will connect when Wi-Fi is up)
    mqtt_client_mgr_config_t mqc = {
        .broker_uri = "mqtt://192.168.1.10:1883",
        .client_id = "mech-sentinel",
        .base_topic = "device/mech-sentinel",
        .keepalive_sec = 60,
    };
    ESP_ERROR_CHECK(mqtt_client_mgr_start(&s_mqtt, &mqc));

    BaseType_t ok;

    ok = xTaskCreatePinnedToCore(task_vibration, "Task_Vibration_Acquisition", 8192, NULL,
                                 BOARD_PRIO_VIBRATION, NULL, BOARD_CORE_1);
    if (ok != pdPASS) {
        return ESP_ERR_NO_MEM;
    }

    ok = xTaskCreatePinnedToCore(task_state_machine, "Task_State_Machine", 6144, NULL,
                                 BOARD_PRIO_STATE_MACHINE, NULL, BOARD_CORE_0);
    if (ok != pdPASS) {
        return ESP_ERR_NO_MEM;
    }

    ok = xTaskCreatePinnedToCore(task_comms, "Task_Comms_Modbus_MQTT", 6144, NULL,
                                 BOARD_PRIO_COMMS, NULL, BOARD_CORE_0);
    if (ok != pdPASS) {
        return ESP_ERR_NO_MEM;
    }

    // Task Watchdog: subscribe critical tasks (vibration + state machine)
    // Note: requires CONFIG_ESP_TASK_WDT to be enabled in sdkconfig.
    esp_task_wdt_config_t twdt_cfg = {
        .timeout_ms = 5000,
        .idle_core_mask = 0, // don't watch idle tasks
        .trigger_panic = true,
    };
    ESP_ERROR_CHECK(esp_task_wdt_init(&twdt_cfg));
    // Tasks reset WDT from inside their loops, so just add them after creation.
    TaskHandle_t hv = xTaskGetHandle("Task_Vibration_Acquisition");
    TaskHandle_t hs = xTaskGetHandle("Task_State_Machine");
    if (hv) {
        ESP_ERROR_CHECK(esp_task_wdt_add(hv));
    }
    if (hs) {
        ESP_ERROR_CHECK(esp_task_wdt_add(hs));
    }

    ESP_LOGI(TAG, "tasks started");
    return ESP_OK;
}
