#include "state_machine.h"

#include <string.h>

#include "esp_log.h"

static const char *TAG = "state_machine";

// Thresholds per requirement
#define TH_VIB_WARN_MIN   2.8f
#define TH_VIB_CRIT_MIN   7.1f
#define TH_TEMP_WARN_MIN  65.0f
#define TH_TEMP_CRIT_MIN  85.0f

typedef struct {
    machine_state_cb_t cb;
    void *user_ctx;
} sm_priv_t;

static sm_priv_t s_priv;

void machine_sm_init(machine_state_machine_t *sm, machine_state_cb_t cb, void *user_ctx)
{
    if (!sm) {
        return;
    }

    memset(sm, 0, sizeof(*sm));
    sm->state = MACHINE_STATE_NORMAL;

    s_priv.cb = cb;
    s_priv.user_ctx = user_ctx;
}

machine_state_t machine_sm_get(machine_state_machine_t *sm)
{
    if (!sm) {
        return MACHINE_STATE_CRITICAL;
    }
    return sm->state;
}

static machine_state_t eval_state(const machine_health_inputs_t *in)
{
    bool vib_crit = (in->vib_rms_mm_s > TH_VIB_CRIT_MIN);
    bool temp_crit = (in->temp_c > TH_TEMP_CRIT_MIN);
    if (vib_crit || temp_crit) {
        return MACHINE_STATE_CRITICAL;
    }

    bool vib_warn = (in->vib_rms_mm_s >= TH_VIB_WARN_MIN);
    bool temp_warn = (in->temp_c >= TH_TEMP_WARN_MIN);
    if (vib_warn || temp_warn) {
        return MACHINE_STATE_WARNING;
    }

    return MACHINE_STATE_NORMAL;
}

machine_state_t machine_sm_update(machine_state_machine_t *sm, const machine_health_inputs_t *in)
{
    if (!sm || !in) {
        return MACHINE_STATE_CRITICAL;
    }

    machine_state_t new_state = eval_state(in);
    if (new_state != sm->state) {
        ESP_LOGW(TAG, "state transition %d -> %d (vib=%.2f mm/s, temp=%.1f C)",
                 (int)sm->state, (int)new_state, (double)in->vib_rms_mm_s, (double)in->temp_c);
        sm->state = new_state;
        if (s_priv.cb) {
            s_priv.cb(new_state, s_priv.user_ctx);
        }
    }

    return sm->state;
}
