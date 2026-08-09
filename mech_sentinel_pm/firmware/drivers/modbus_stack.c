#include "modbus_stack.h"

#include <string.h>

#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"

#include "driver/uart.h"
#include "driver/gpio.h"

static const char *TAG = "modbus";

static inline void lock_take(SemaphoreHandle_t lock)
{
    (void)xSemaphoreTake(lock, portMAX_DELAY);
}

static inline void lock_give(SemaphoreHandle_t lock)
{
    (void)xSemaphoreGive(lock);
}

esp_err_t modbus_stack_init(modbus_stack_t *mb, const modbus_stack_config_t *cfg)
{
    if (!mb || !cfg) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(mb, 0, sizeof(*mb));
    mb->cfg = *cfg;

    mb->lock = xSemaphoreCreateMutex();
    if (!mb->lock) {
        return ESP_ERR_NO_MEM;
    }

    const uart_config_t uart_cfg = {
        .baud_rate = cfg->baudrate,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };

    esp_err_t e = uart_driver_install(cfg->uart_num, 2048, 0, 0, NULL, 0);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "uart_driver_install failed: %s", esp_err_to_name(e));
        return e;
    }

    e = uart_param_config(cfg->uart_num, &uart_cfg);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "uart_param_config failed: %s", esp_err_to_name(e));
        return e;
    }

    e = uart_set_pin(cfg->uart_num, cfg->gpio_tx, cfg->gpio_rx, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "uart_set_pin failed: %s", esp_err_to_name(e));
        return e;
    }

    // RS485 DE pin
    gpio_config_t io = {
        .pin_bit_mask = (1ULL << cfg->gpio_de),
        .mode = GPIO_MODE_OUTPUT,
        .pull_down_en = 0,
        .pull_up_en = 0,
        .intr_type = GPIO_INTR_DISABLE,
    };
    e = gpio_config(&io);
    if (e != ESP_OK) {
        return e;
    }
    (void)gpio_set_level(cfg->gpio_de, 0); // receive by default

    mb->initialized = true;
    ESP_LOGI(TAG, "init ok: uart=%d %d bps slave_id=%u tx=%d rx=%d de=%d", cfg->uart_num, cfg->baudrate,
             (unsigned)cfg->slave_id, cfg->gpio_tx, cfg->gpio_rx, cfg->gpio_de);

    return ESP_OK;
}

esp_err_t modbus_stack_deinit(modbus_stack_t *mb)
{
    if (!mb) {
        return ESP_ERR_INVALID_ARG;
    }

    if (mb->initialized) {
        (void)uart_driver_delete(mb->cfg.uart_num);
    }

    if (mb->lock) {
        vSemaphoreDelete((SemaphoreHandle_t)mb->lock);
        mb->lock = NULL;
    }

    memset(mb, 0, sizeof(*mb));
    return ESP_OK;
}

esp_err_t modbus_stack_set_input_reg(modbus_stack_t *mb, uint16_t reg_addr_30001, uint16_t value)
{
    if (!mb || !mb->initialized) {
        return ESP_ERR_INVALID_STATE;
    }

    if (reg_addr_30001 < MODBUS_INPUT_REG_BASE) {
        return ESP_ERR_INVALID_ARG;
    }

    uint16_t idx = reg_addr_30001 - MODBUS_INPUT_REG_BASE;
    if (idx >= MODBUS_INPUT_REG_COUNT) {
        return ESP_ERR_INVALID_ARG;
    }

    lock_take((SemaphoreHandle_t)mb->lock);
    mb->regs.input_regs[idx] = value;
    lock_give((SemaphoreHandle_t)mb->lock);
    return ESP_OK;
}

esp_err_t modbus_stack_poll(modbus_stack_t *mb)
{
    if (!mb || !mb->initialized) {
        return ESP_ERR_INVALID_STATE;
    }

    // Placeholder: a real Modbus RTU implementation should parse frames, check CRC16,
    // handle function codes (0x04 for input registers), and respond.
    // This stub simply drains RX to avoid UART buffer buildup.
    uint8_t tmp[256];
    int n = uart_read_bytes(mb->cfg.uart_num, tmp, sizeof(tmp), 0);
    if (n > 0) {
        ESP_LOGD(TAG, "rx %d bytes (stub)", n);
    }

    return ESP_OK;
}
