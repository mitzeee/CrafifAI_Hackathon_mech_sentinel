#include "thermal_adc.h"

#include <string.h>

#include "esp_log.h"
#include "esp_err.h"

#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"

static const char *TAG = "thermal_adc";

static esp_err_t try_create_cali(adc_unit_t unit, adc_atten_t atten, adc_bitwidth_t bitwidth,
                                adc_cali_handle_t *out)
{
    *out = NULL;

#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
    adc_cali_curve_fitting_config_t cali_cfg = {
        .unit_id = unit,
        .atten = atten,
        .bitwidth = bitwidth,
    };
    esp_err_t e = adc_cali_create_scheme_curve_fitting(&cali_cfg, out);
    if (e == ESP_OK) {
        return ESP_OK;
    }
#endif

#if ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
    adc_cali_line_fitting_config_t cali_cfg = {
        .unit_id = unit,
        .atten = atten,
        .bitwidth = bitwidth,
    };
    esp_err_t e = adc_cali_create_scheme_line_fitting(&cali_cfg, out);
    if (e == ESP_OK) {
        return ESP_OK;
    }
#endif

    return ESP_ERR_NOT_SUPPORTED;
}

esp_err_t thermal_adc_init(thermal_adc_t *t, const thermal_adc_config_t *cfg)
{
    if (!t || !cfg) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(t, 0, sizeof(*t));
    t->cfg = *cfg;
    adc_oneshot_unit_handle_t oneshot = NULL;

    adc_oneshot_unit_init_cfg_t unit_cfg = {
        .unit_id = (adc_unit_t)cfg->adc_unit,
        .ulp_mode = ADC_ULP_MODE_DISABLE,
    };

    esp_err_t e = adc_oneshot_new_unit(&unit_cfg, &oneshot);
    if (e != ESP_OK) {
        return e;
    }

    adc_oneshot_chan_cfg_t chan_cfg = {
        .bitwidth = (adc_bitwidth_t)cfg->bitwidth,
        .atten = (adc_atten_t)cfg->atten,
    };

    e = adc_oneshot_config_channel(oneshot, (adc_channel_t)cfg->adc_channel, &chan_cfg);
    if (e != ESP_OK) {
        (void)adc_oneshot_del_unit(oneshot);
        return e;
    }

    adc_cali_handle_t cali = NULL;
    esp_err_t ce = try_create_cali((adc_unit_t)cfg->adc_unit, (adc_atten_t)cfg->atten,
                                  (adc_bitwidth_t)cfg->bitwidth, &cali);
    if (ce == ESP_OK) {
        t->cali_handle = cali;
        ESP_LOGI(TAG, "ADC calibration enabled");
    } else {
        ESP_LOGW(TAG, "ADC calibration not supported; using raw-to-mV approximation");
    }

    t->oneshot = oneshot;
    t->initialized = true;

    ESP_LOGI(TAG, "init ok: unit=%d ch=%d atten=%d bitwidth=%d", cfg->adc_unit, cfg->adc_channel,
             cfg->atten, cfg->bitwidth);
    return ESP_OK;
}

esp_err_t thermal_adc_deinit(thermal_adc_t *t)
{
    if (!t) {
        return ESP_ERR_INVALID_ARG;
    }

    
    if (t->cali_handle) {
#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED
        (void)adc_cali_delete_scheme_curve_fitting((adc_cali_handle_t)t->cali_handle);
#endif
#if ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED
        (void)adc_cali_delete_scheme_line_fitting((adc_cali_handle_t)t->cali_handle);
#endif
        t->cali_handle = NULL;
    }

    if (t->oneshot) {
        (void)adc_oneshot_del_unit((adc_oneshot_unit_handle_t)t->oneshot);
        t->oneshot = NULL;
    }

    memset(t, 0, sizeof(*t));
    return ESP_OK;
}

esp_err_t thermal_adc_read_mv(thermal_adc_t *t, int *out_mv)
{
    if (!t || !t->initialized || !out_mv) {
        return ESP_ERR_INVALID_ARG;
    }
    if (!t->oneshot) {
        return ESP_ERR_INVALID_STATE;
    }

    int raw = 0;
    esp_err_t e = adc_oneshot_read((adc_oneshot_unit_handle_t)t->oneshot,
                                  (adc_channel_t)t->cfg.adc_channel, &raw);
    if (e != ESP_OK) {
        return e;
    }

    if (t->cali_handle) {
        int mv = 0;
        e = adc_cali_raw_to_voltage((adc_cali_handle_t)t->cali_handle, raw, &mv);
        if (e == ESP_OK) {
            *out_mv = mv;
            return ESP_OK;
        }
    }

    // Fallback: approximate mV from raw. For ADC1 the full-scale depends on attenuation.
    // This approximation is coarse; prefer calibration.
    int max_raw = (1 << 12) - 1;
    int approx_mv = (raw * 3300) / max_raw;
    *out_mv = approx_mv;
    return ESP_OK;
}

esp_err_t thermal_adc_read_temp_c(thermal_adc_t *t, float *out_temp_c)
{
    if (!t || !t->initialized || !out_temp_c) {
        return ESP_ERR_INVALID_ARG;
    }

    int mv = 0;
    esp_err_t e = thermal_adc_read_mv(t, &mv);
    if (e != ESP_OK) {
        return e;
    }

    *out_temp_c = (mv - t->cfg.offset_mv) * t->cfg.scale_c_per_mv;
    return ESP_OK;
}
