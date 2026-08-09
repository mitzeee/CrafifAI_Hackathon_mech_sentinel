#include "adxl355.h"

#include <string.h>

#include "board_config.h"
#include "esp_log.h"

static const char *TAG = "adxl355";

// Minimal register addresses for burst read
#define ADXL355_REG_XDATA3   0x08

// Read bit per ADXL355 SPI protocol: bit7=1 for read, bit7=0 for write
#define ADXL355_SPI_READ     0x01

// Sensitivity depends on range; this stub assumes +-2g typical scale.
// TODO: make range configurable and implement proper scale based on datasheet.
#define ADXL355_LSB_PER_G    (256000.0f) // placeholder

static esp_err_t spi_bus_init_if_needed(const adxl355_config_t *cfg)
{
    spi_bus_config_t buscfg = {
        .mosi_io_num = cfg->gpio_mosi,
        .miso_io_num = cfg->gpio_miso,
        .sclk_io_num = cfg->gpio_sck,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 64,
    };

    esp_err_t e = spi_bus_initialize(cfg->host, &buscfg, SPI_DMA_CH_AUTO);
    if (e == ESP_ERR_INVALID_STATE) {
        // Already initialized elsewhere; treat as OK.
        return ESP_OK;
    }
    return e;
}

static esp_err_t device_add(adxl355_t *s)
{
    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = s->cfg.clock_hz,
        .mode = s->cfg.spi_mode,
        .spics_io_num = s->cfg.gpio_cs,
        .queue_size = s->cfg.spi_queue_size,
        .flags = SPI_DEVICE_HALFDUPLEX,
    };
    return spi_bus_add_device(s->cfg.host, &devcfg, &s->dev);
}

esp_err_t adxl355_init(adxl355_t *s, const adxl355_config_t *cfg)
{
    if (!s || !cfg) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(s, 0, sizeof(*s));
    s->cfg = *cfg;
    s->host = cfg->host;

    ESP_LOGI(TAG, "init: host=%d cs=%d sck=%d mosi=%d miso=%d clk=%d mode=%d", (int)cfg->host,
             cfg->gpio_cs, cfg->gpio_sck, cfg->gpio_mosi, cfg->gpio_miso, cfg->clock_hz, cfg->spi_mode);

    esp_err_t e = spi_bus_init_if_needed(cfg);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "spi_bus_initialize failed: %s", esp_err_to_name(e));
        return e;
    }

    e = device_add(s);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "spi_bus_add_device failed: %s", esp_err_to_name(e));
        return e;
    }

    s->initialized = true;
    return ESP_OK;
}

esp_err_t adxl355_deinit(adxl355_t *s)
{
    if (!s) {
        return ESP_ERR_INVALID_ARG;
    }

    if (s->dev) {
        spi_bus_remove_device(s->dev);
        s->dev = NULL;
    }

    // Note: we do not call spi_bus_free() because other devices may share the bus.
    s->initialized = false;
    return ESP_OK;
}

static esp_err_t read_burst_9bytes(adxl355_t *s, uint8_t reg, uint8_t out9[9])
{
    // Burst read: send address with read bit, then read 9 bytes (X/Y/Z each 20-bit packed).
    uint8_t tx[1] = { (uint8_t)((reg << 1) | ADXL355_SPI_READ) };

    spi_transaction_t t = {
        .length = 8,
        .tx_buffer = tx,
        .rxlength = 9 * 8,
        .rx_buffer = out9,
    };

    // Two-phase half-duplex: command (TX) then RX
    esp_err_t e = spi_device_transmit(s->dev, &t);
    return e;
}

static int32_t unpack_20bit(const uint8_t b3, const uint8_t b2, const uint8_t b1)
{
    // Datasheet: XDATA3:XDATA2:XDATA1, where XDATA1 bits[7:4] carry lowest 4 bits.
    int32_t raw = ((int32_t)b3 << 12) | ((int32_t)b2 << 4) | ((int32_t)(b1 >> 4) & 0x0F);
    // Sign extend 20-bit
    if (raw & (1 << 19)) {
        raw |= ~((1 << 20) - 1);
    }
    return raw;
}

esp_err_t adxl355_recover(adxl355_t *s)
{
    if (!s) {
        return ESP_ERR_INVALID_ARG;
    }

    ESP_LOGW(TAG, "recover: deinit+reinit after %u consecutive timeouts", (unsigned)s->consecutive_timeouts);

    (void)adxl355_deinit(s);

    esp_err_t e = adxl355_init(s, &s->cfg);
    if (e == ESP_OK) {
        s->consecutive_timeouts = 0;
    }
    return e;
}

esp_err_t adxl355_read_accel_g(adxl355_t *s, adxl355_accel_g_t *out)
{
    if (!s || !out || !s->initialized || !s->dev) {
        return ESP_ERR_INVALID_STATE;
    }

    uint8_t rx[9] = {0};
    esp_err_t e = read_burst_9bytes(s, ADXL355_REG_XDATA3, rx);
    if (e == ESP_ERR_TIMEOUT) {
        s->consecutive_timeouts++;
        ESP_LOGW(TAG, "SPI timeout (%u/%u)", (unsigned)s->consecutive_timeouts,
                 (unsigned)s->cfg.max_consecutive_timeouts);

        if (s->consecutive_timeouts >= s->cfg.max_consecutive_timeouts) {
            (void)adxl355_recover(s);
        }
        return e;
    }

    if (e != ESP_OK) {
        ESP_LOGE(TAG, "SPI read failed: %s", esp_err_to_name(e));
        return e;
    }

    s->consecutive_timeouts = 0;

    int32_t x = unpack_20bit(rx[0], rx[1], rx[2]);
    int32_t y = unpack_20bit(rx[3], rx[4], rx[5]);
    int32_t z = unpack_20bit(rx[6], rx[7], rx[8]);

    out->ax_g = (float)x / ADXL355_LSB_PER_G;
    out->ay_g = (float)y / ADXL355_LSB_PER_G;
    out->az_g = (float)z / ADXL355_LSB_PER_G;

    return ESP_OK;
}
