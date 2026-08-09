#ifndef THERMAL_ADC_H
#define THERMAL_ADC_H

#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int adc_unit;       // adc_unit_t
    int adc_channel;    // adc_channel_t
    int atten;          // adc_atten_t
    int bitwidth;       // adc_bitwidth_t

    // Temperature conversion (linear model): temp_c = (mv - offset_mv) * scale_c_per_mv
    // Defaults should be set based on your actual sensor and divider.
    float offset_mv;
    float scale_c_per_mv;
} thermal_adc_config_t;

typedef struct {
    thermal_adc_config_t cfg;
    bool initialized;
    void *oneshot;     // adc_oneshot_unit_handle_t
    void *cali_handle; // adc_cali_handle_t
} thermal_adc_t;

esp_err_t thermal_adc_init(thermal_adc_t *t, const thermal_adc_config_t *cfg);

esp_err_t thermal_adc_deinit(thermal_adc_t *t);

esp_err_t thermal_adc_read_mv(thermal_adc_t *t, int *out_mv);

esp_err_t thermal_adc_read_temp_c(thermal_adc_t *t, float *out_temp_c);

#ifdef __cplusplus
}
#endif

#endif // THERMAL_ADC_H
