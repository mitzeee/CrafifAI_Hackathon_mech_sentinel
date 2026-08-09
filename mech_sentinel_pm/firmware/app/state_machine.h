#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

#include <stdint.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    MACHINE_STATE_NORMAL = 0,
    MACHINE_STATE_WARNING,
    MACHINE_STATE_CRITICAL,
} machine_state_t;

typedef struct {
    float vib_rms_mm_s;
    float temp_c;
} machine_health_inputs_t;

typedef struct {
    machine_state_t state;
} machine_state_machine_t;

typedef void (*machine_state_cb_t)(machine_state_t new_state, void *user_ctx);

void machine_sm_init(machine_state_machine_t *sm, machine_state_cb_t cb, void *user_ctx);

machine_state_t machine_sm_get(machine_state_machine_t *sm);

machine_state_t machine_sm_update(machine_state_machine_t *sm, const machine_health_inputs_t *in);

#ifdef __cplusplus
}
#endif

#endif // STATE_MACHINE_H
