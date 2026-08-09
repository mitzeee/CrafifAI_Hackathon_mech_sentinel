#ifndef STATUS_LED_WS2812_H
#define STATUS_LED_WS2812_H

#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    STATUS_LED_MODE_OFF = 0,
    STATUS_LED_MODE_SOLID,
    STATUS_LED_MODE_BLINK,
} status_led_mode_t;

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
} status_led_rgb_t;

typedef struct {
    int gpio;
    uint32_t rmt_resolution_hz;
    bool use_dma;
} status_led_ws2812_config_t;

typedef struct {
    status_led_ws2812_config_t cfg;
    void *strip; // led_strip_handle_t
    status_led_mode_t mode;
    status_led_rgb_t color;
    uint32_t blink_period_ms;
    bool initialized;
} status_led_ws2812_t;

esp_err_t status_led_ws2812_init(status_led_ws2812_t *led, const status_led_ws2812_config_t *cfg);

esp_err_t status_led_ws2812_deinit(status_led_ws2812_t *led);

esp_err_t status_led_ws2812_set_off(status_led_ws2812_t *led);

esp_err_t status_led_ws2812_set_solid(status_led_ws2812_t *led, status_led_rgb_t c);

esp_err_t status_led_ws2812_set_blink(status_led_ws2812_t *led, status_led_rgb_t c, uint32_t period_ms);

/**
 * @brief Tick function to be called periodically from a task/timer.
 */
void status_led_ws2812_tick(status_led_ws2812_t *led, uint32_t now_ms);

#ifdef __cplusplus
}
#endif

#endif // STATUS_LED_WS2812_H
