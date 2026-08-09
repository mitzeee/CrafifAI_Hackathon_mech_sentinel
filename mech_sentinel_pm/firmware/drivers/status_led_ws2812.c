#include "status_led_ws2812.h"

#include <string.h>

#include "esp_log.h"

#include "led_strip.h"
#include "led_strip_rmt.h"

static const char *TAG = "status_led";

static esp_err_t apply_color(status_led_ws2812_t *led, bool on)
{
    led_strip_handle_t strip = (led_strip_handle_t)led->strip;
    uint8_t r = on ? led->color.r : 0;
    uint8_t g = on ? led->color.g : 0;
    uint8_t b = on ? led->color.b : 0;

    esp_err_t e = led_strip_set_pixel(strip, 0, r, g, b);
    if (e != ESP_OK) {
        return e;
    }
    return led_strip_refresh(strip);
}

esp_err_t status_led_ws2812_init(status_led_ws2812_t *led, const status_led_ws2812_config_t *cfg)
{
    if (!led || !cfg) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(led, 0, sizeof(*led));
    led->cfg = *cfg;

    led_strip_config_t strip_cfg = {
        .strip_gpio_num = cfg->gpio,
        .max_leds = 1,
        .led_model = LED_MODEL_WS2812,
        .color_component_format = LED_STRIP_COLOR_COMPONENT_FMT_GRB,
        .flags = {
            .invert_out = false,
        },
    };

    led_strip_rmt_config_t rmt_cfg = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = cfg->rmt_resolution_hz,
        .mem_block_symbols = 0,
        .flags = {
            .with_dma = cfg->use_dma,
        },
    };

    led_strip_handle_t strip = NULL;
    esp_err_t e = led_strip_new_rmt_device(&strip_cfg, &rmt_cfg, &strip);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "led_strip_new_rmt_device failed: %s", esp_err_to_name(e));
        return e;
    }

    led->strip = strip;
    led->initialized = true;

    led->mode = STATUS_LED_MODE_OFF;
    led->color = (status_led_rgb_t){0, 0, 0};
    led->blink_period_ms = 1000;

    (void)led_strip_clear(strip);

    ESP_LOGI(TAG, "init ok: gpio=%d res=%u dma=%d", cfg->gpio, (unsigned)cfg->rmt_resolution_hz, (int)cfg->use_dma);
    return ESP_OK;
}

esp_err_t status_led_ws2812_deinit(status_led_ws2812_t *led)
{
    if (!led) {
        return ESP_ERR_INVALID_ARG;
    }

    if (led->strip) {
        led_strip_handle_t strip = (led_strip_handle_t)led->strip;
        (void)led_strip_clear(strip);
        (void)led_strip_del(strip);
        led->strip = NULL;
    }

    memset(led, 0, sizeof(*led));
    return ESP_OK;
}

esp_err_t status_led_ws2812_set_off(status_led_ws2812_t *led)
{
    if (!led || !led->initialized) {
        return ESP_ERR_INVALID_STATE;
    }
    led->mode = STATUS_LED_MODE_OFF;
    led->color = (status_led_rgb_t){0, 0, 0};
    return apply_color(led, false);
}

esp_err_t status_led_ws2812_set_solid(status_led_ws2812_t *led, status_led_rgb_t c)
{
    if (!led || !led->initialized) {
        return ESP_ERR_INVALID_STATE;
    }
    led->mode = STATUS_LED_MODE_SOLID;
    led->color = c;
    return apply_color(led, true);
}

esp_err_t status_led_ws2812_set_blink(status_led_ws2812_t *led, status_led_rgb_t c, uint32_t period_ms)
{
    if (!led || !led->initialized || period_ms == 0) {
        return ESP_ERR_INVALID_ARG;
    }
    led->mode = STATUS_LED_MODE_BLINK;
    led->color = c;
    led->blink_period_ms = period_ms;
    return ESP_OK;
}

void status_led_ws2812_tick(status_led_ws2812_t *led, uint32_t now_ms)
{
    if (!led || !led->initialized) {
        return;
    }

    if (led->mode == STATUS_LED_MODE_SOLID) {
        (void)apply_color(led, true);
        return;
    }

    if (led->mode == STATUS_LED_MODE_OFF) {
        (void)apply_color(led, false);
        return;
    }

    if (led->mode == STATUS_LED_MODE_BLINK) {
        uint32_t phase = (now_ms / (led->blink_period_ms / 2)) & 0x01;
        bool on = (phase == 0);
        (void)apply_color(led, on);
        return;
    }
}
