#ifndef WIFI_PROV_MGR_APP_H
#define WIFI_PROV_MGR_APP_H

#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    const char *service_name;   // BLE device name
    const char *service_key;    // not used for BLE (can be NULL)
    const char *pop;            // proof-of-possession (Security 1)
    bool enable_reprovisioning;
} wifi_prov_mgr_app_config_t;

esp_err_t wifi_prov_mgr_app_start(const wifi_prov_mgr_app_config_t *cfg);

bool wifi_prov_mgr_app_is_connected(void);

#ifdef __cplusplus
}
#endif

#endif // WIFI_PROV_MGR_APP_H
