#include "inmp441.h"

#include <string.h>

#include "esp_log.h"
#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/i2s_std.h"

static const char *TAG = "inmp441";

typedef struct {
    i2s_chan_handle_t rx_chan;
} inmp441_priv_t;

esp_err_t inmp441_init(inmp441_t *mic, const inmp441_config_t *cfg)
{
    if (!mic || !cfg) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(mic, 0, sizeof(*mic));
    mic->cfg = *cfg;

    inmp441_priv_t *p = (inmp441_priv_t *)calloc(1, sizeof(*p));
    if (!p) {
        return ESP_ERR_NO_MEM;
    }

    // New I2S driver (ESP-IDF v5)
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(cfg->i2s_port, I2S_ROLE_MASTER);
    chan_cfg.auto_clear = true;

    esp_err_t e = i2s_new_channel(&chan_cfg, NULL, &p->rx_chan);
    if (e != ESP_OK) {
        free(p);
        ESP_LOGE(TAG, "i2s_new_channel failed: %s", esp_err_to_name(e));
        return e;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(cfg->sample_rate_hz),
        .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(
            (cfg->bits_per_sample == 16) ? I2S_DATA_BIT_WIDTH_16BIT : I2S_DATA_BIT_WIDTH_32BIT,
            I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .mclk = I2S_GPIO_UNUSED,
            .bclk = cfg->gpio_bclk,
            .ws = cfg->gpio_ws,
            .dout = I2S_GPIO_UNUSED,
            .din = cfg->gpio_din,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    // INMP441 outputs I2S standard; MSB justified is typical. If channel swap needed, adjust slot_cfg.
    e = i2s_channel_init_std_mode(p->rx_chan, &std_cfg);
    if (e != ESP_OK) {
        (void)i2s_del_channel(p->rx_chan);
        free(p);
        ESP_LOGE(TAG, "i2s_channel_init_std_mode failed: %s", esp_err_to_name(e));
        return e;
    }

    e = i2s_channel_enable(p->rx_chan);
    if (e != ESP_OK) {
        (void)i2s_del_channel(p->rx_chan);
        free(p);
        ESP_LOGE(TAG, "i2s_channel_enable failed: %s", esp_err_to_name(e));
        return e;
    }

    mic->rx_handle = p;
    mic->initialized = true;

    ESP_LOGI(TAG, "init ok: rate=%d Hz, bits=%d, bclk=%d ws=%d din=%d", cfg->sample_rate_hz,
             cfg->bits_per_sample, cfg->gpio_bclk, cfg->gpio_ws, cfg->gpio_din);

    return ESP_OK;
}

esp_err_t inmp441_deinit(inmp441_t *mic)
{
    if (!mic) {
        return ESP_ERR_INVALID_ARG;
    }

    inmp441_priv_t *p = (inmp441_priv_t *)mic->rx_handle;
    if (p && p->rx_chan) {
        (void)i2s_channel_disable(p->rx_chan);
        (void)i2s_del_channel(p->rx_chan);
        p->rx_chan = NULL;
    }

    if (p) {
        free(p);
    }

    memset(mic, 0, sizeof(*mic));
    return ESP_OK;
}

esp_err_t inmp441_read(inmp441_t *mic, void *out_buf, size_t out_len_bytes, size_t *bytes_read)
{
    if (!mic || !mic->initialized || !out_buf || out_len_bytes == 0) {
        return ESP_ERR_INVALID_ARG;
    }

    inmp441_priv_t *p = (inmp441_priv_t *)mic->rx_handle;
    if (!p || !p->rx_chan) {
        return ESP_ERR_INVALID_STATE;
    }

    size_t br = 0;
    esp_err_t e = i2s_channel_read(p->rx_chan, out_buf, out_len_bytes, &br,
                                  pdMS_TO_TICKS(mic->cfg.read_timeout_ms));

    if (bytes_read) {
        *bytes_read = br;
    }

    if (e == ESP_ERR_TIMEOUT) {
        // Not fatal; caller task can continue.
        return e;
    }

    if (e != ESP_OK) {
        ESP_LOGW(TAG, "i2s_channel_read failed: %s", esp_err_to_name(e));
        return e;
    }

    return ESP_OK;
}
