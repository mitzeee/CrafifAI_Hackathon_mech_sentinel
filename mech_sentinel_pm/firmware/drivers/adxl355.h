#ifndef ADXL355_H
#define ADXL355_H

#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"
#include "driver/spi_master.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    spi_host_device_t host;
    int gpio_cs;
    int gpio_sck;
    int gpio_mosi;
    int gpio_miso;
    int spi_mode;              // 0..3
    int clock_hz;
    int spi_queue_size;
    int timeout_ms;

    // Recovery policy
    uint32_t max_consecutive_timeouts;
} adxl355_config_t;

typedef struct {
    spi_device_handle_t dev;
    spi_host_device_t host;
    adxl355_config_t cfg;
    uint32_t consecutive_timeouts;
    bool initialized;
} adxl355_t;

typedef struct {
    float ax_g;
    float ay_g;
    float az_g;
} adxl355_accel_g_t;

esp_err_t adxl355_init(adxl355_t *s, const adxl355_config_t *cfg);

esp_err_t adxl355_deinit(adxl355_t *s);

/**
 * @brief Read 3-axis acceleration sample.
 *
 * This function performs SPI transactions and may return ESP_ERR_TIMEOUT.
 * On N consecutive timeouts (cfg->max_consecutive_timeouts) it attempts bus recovery.
 */
esp_err_t adxl355_read_accel_g(adxl355_t *s, adxl355_accel_g_t *out);

/**
 * @brief Force SPI bus + device recovery (deinit + init).
 */
esp_err_t adxl355_recover(adxl355_t *s);

#ifdef __cplusplus
}
#endif

#endif // ADXL355_H
