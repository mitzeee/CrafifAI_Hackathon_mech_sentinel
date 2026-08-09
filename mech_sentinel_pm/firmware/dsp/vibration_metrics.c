#include "vibration_metrics.h"

#include <math.h>

#include "esp_dsp.h"
#include "dsps_dotprod.h"
#include "esp_log.h"

static const char *TAG = "vib_metrics";
static bool s_dsp_ok;

esp_err_t vibration_metrics_init(void)
{
    esp_err_t e = dsps_fft2r_init_fc32(NULL, CONFIG_DSP_MAX_FFT_SIZE);
    if (e == ESP_OK) {
        s_dsp_ok = true;
        ESP_LOGI(TAG, "ESP-DSP init OK");
        return ESP_OK;
    }

    s_dsp_ok = false;
    ESP_LOGW(TAG, "ESP-DSP init failed (%s); falling back to scalar", esp_err_to_name(e));
    return ESP_OK;
}

esp_err_t vibration_metrics_compute(const float *mag_g, size_t n, vibration_metrics_t *out)
{
    if (!mag_g || n == 0 || !out) {
        return ESP_ERR_INVALID_ARG;
    }

    float peak = 0.0f;
    float sum_sq = 0.0f;

    if (s_dsp_ok) {        // Peak (compute scalar here; keep DSP for dot product)
        for (size_t i = 0; i < n; i++) {
            float v = fabsf(mag_g[i]);
            if (v > peak) {
                peak = v;
            }
        }

        // RMS
        // dsps_dotprod can be used for sum of squares
        float dot = 0;
        (void)dsps_dotprod_f32_aes3(mag_g, mag_g, &dot, (int)n);
        sum_sq = dot;
    } else {
        for (size_t i = 0; i < n; i++) {
            float v = fabsf(mag_g[i]);
            if (v > peak) {
                peak = v;
            }
            sum_sq += mag_g[i] * mag_g[i];
        }
    }

    float rms = sqrtf(sum_sq / (float)n);

    out->peak_g = peak;
    out->rms_g = rms;
    out->crest_factor = (rms > 1e-6f) ? (peak / rms) : 0.0f;

    return ESP_OK;
}
