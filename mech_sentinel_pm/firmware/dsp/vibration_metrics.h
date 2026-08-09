#ifndef VIBRATION_METRICS_H
#define VIBRATION_METRICS_H

#include <stddef.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float peak_g;
    float rms_g;
    float crest_factor;
} vibration_metrics_t;

esp_err_t vibration_metrics_init(void);

/**
 * @brief Compute basic vibration metrics from magnitude in g.
 */
esp_err_t vibration_metrics_compute(const float *mag_g, size_t n, vibration_metrics_t *out);

#ifdef __cplusplus
}
#endif

#endif // VIBRATION_METRICS_H
