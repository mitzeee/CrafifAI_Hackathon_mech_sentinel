#ifndef INMP441_H
#define INMP441_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int i2s_port; // logical port index
    int gpio_bclk;
    int gpio_ws;
    int gpio_din;

    int sample_rate_hz;
    int bits_per_sample;

    size_t dma_frame_bytes;
    int dma_desc_num;

    int read_timeout_ms;
} inmp441_config_t;

typedef struct {
    inmp441_config_t cfg;
    bool initialized;
    void *chan; // opaque handle (i2s_chan_handle_t)
    void *rx_handle;
} inmp441_t;

esp_err_t inmp441_init(inmp441_t *mic, const inmp441_config_t *cfg);

esp_err_t inmp441_deinit(inmp441_t *mic);

/**
 * @brief Read a PCM block from I2S.
 *
 * @param out_buf Destination buffer
 * @param out_len_bytes Buffer length
 * @param bytes_read Returned bytes
 */
esp_err_t inmp441_read(inmp441_t *mic, void *out_buf, size_t out_len_bytes, size_t *bytes_read);

#ifdef __cplusplus
}
#endif

#endif // INMP441_H
