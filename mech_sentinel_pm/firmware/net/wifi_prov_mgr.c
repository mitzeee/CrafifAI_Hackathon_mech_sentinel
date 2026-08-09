#include "wifi_prov_mgr.h"

#include <string.h>

#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "esp_wifi.h"
#include "nvs_flash.h"

#include "wifi_provisioning/manager.h"
#include "wifi_provisioning/scheme_ble.h"

#include "qrcode.h"

static const char *TAG = "wifi_prov";

static bool s_connected;

static void wifi_event_handler(void *arg, esp_event_base_t event_base,
                              int32_t event_id, void *event_data)
{
    (void)arg;

    if (event_base == WIFI_EVENT) {
        switch (event_id) {
        case WIFI_EVENT_STA_START:
            esp_wifi_connect();
            break;
        case WIFI_EVENT_STA_DISCONNECTED:
            s_connected = false;
            // Let esp_wifi reconnect policy handle it (we call connect again)
            esp_wifi_connect();
            break;
        default:
            break;
        }
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        s_connected = true;
    }
}

static void prov_event_handler(void *arg, esp_event_base_t event_base,
                              int32_t event_id, void *event_data)
{
    (void)arg;
    if (event_base != WIFI_PROV_EVENT) {
        return;
    }

    switch (event_id) {
    case WIFI_PROV_START:
        ESP_LOGI(TAG, "Provisioning started");
        break;
    case WIFI_PROV_CRED_RECV: {
        wifi_sta_config_t *sta_cfg = (wifi_sta_config_t *)event_data;
        ESP_LOGI(TAG, "Received Wi-Fi credentials for SSID: %s", (const char *)sta_cfg->ssid);
        break;
    }
    case WIFI_PROV_CRED_SUCCESS:
        ESP_LOGI(TAG, "Provisioning success");
        break;
    case WIFI_PROV_END:
        ESP_LOGI(TAG, "Provisioning ended");
        wifi_prov_mgr_deinit();
        break;
    default:
        break;
    }
}

static void print_qr(const char *name, const char *pop)
{
    // Using Security 1 via PoP
    const char *transport = "ble";
    const char *username = "";
    char payload[200];

    // Format per Espressif provisioning QR schema
    // {"ver":"v1","name":"<name>","pop":"<pop>","transport":"ble"}
    snprintf(payload, sizeof(payload),
             "{\"ver\":\"v1\",\"name\":\"%s\",\"pop\":\"%s\",\"transport\":\"%s\"}",
             name ? name : "", pop ? pop : "", transport);

    ESP_LOGI(TAG, "Scan this QR with ESP Provisioning app");
    ESP_LOGI(TAG, "Payload: %s", payload);

    esp_qrcode_config_t cfg = ESP_QRCODE_CONFIG_DEFAULT();
    esp_qrcode_generate(&cfg, payload);
    (void)username;
}

esp_err_t wifi_prov_mgr_app_start(const wifi_prov_mgr_app_config_t *cfg)
{
    if (!cfg || !cfg->service_name || !cfg->pop) {
        return ESP_ERR_INVALID_ARG;
    }

    // Init NVS
    esp_err_t e = nvs_flash_init();
    if (e == ESP_ERR_NVS_NO_FREE_PAGES || e == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        e = nvs_flash_erase();
        if (e != ESP_OK) {
            ESP_LOGE(TAG, "nvs_flash_erase failed: %s", esp_err_to_name(e));
            return e;
        }
        e = nvs_flash_init();
    }
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "nvs_flash_init failed: %s", esp_err_to_name(e));
        return e;
    }

    e = esp_netif_init();
    if (e != ESP_OK && e != ESP_ERR_INVALID_STATE) {
        ESP_LOGE(TAG, "esp_netif_init failed: %s", esp_err_to_name(e));
        return e;
    }

    esp_err_t le = esp_event_loop_create_default();
    if (le != ESP_OK && le != ESP_ERR_INVALID_STATE) {
        ESP_LOGE(TAG, "esp_event_loop_create_default failed: %s", esp_err_to_name(le));
        return le;
    }

    e = esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "register WIFI_EVENT handler failed: %s", esp_err_to_name(e));
        return e;
    }
    e = esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "register IP_EVENT handler failed: %s", esp_err_to_name(e));
        return e;
    }
    e = esp_event_handler_register(WIFI_PROV_EVENT, ESP_EVENT_ANY_ID, &prov_event_handler, NULL);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "register WIFI_PROV_EVENT handler failed: %s", esp_err_to_name(e));
        return e;
    }

    esp_netif_create_default_wifi_sta();

    wifi_init_config_t wifi_init_cfg = WIFI_INIT_CONFIG_DEFAULT();
    e = esp_wifi_init(&wifi_init_cfg);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "esp_wifi_init failed: %s", esp_err_to_name(e));
        return e;
    }

    bool provisioned = false;

    wifi_prov_mgr_config_t prov_mgr_cfg = {
        .scheme = wifi_prov_scheme_ble,
        .scheme_event_handler = WIFI_PROV_SCHEME_BLE_EVENT_HANDLER_FREE_BTDM,
    };

    e = wifi_prov_mgr_init(prov_mgr_cfg);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "wifi_prov_mgr_init failed: %s", esp_err_to_name(e));
        return e;
    }

    e = wifi_prov_mgr_is_provisioned(&provisioned);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "wifi_prov_mgr_is_provisioned failed: %s", esp_err_to_name(e));
        return e;
    }

    if (provisioned && !cfg->enable_reprovisioning) {
        ESP_LOGI(TAG, "Already provisioned, starting Wi-Fi STA");
        (void)wifi_prov_mgr_deinit();

        e = esp_wifi_set_mode(WIFI_MODE_STA);
        if (e != ESP_OK) {
            ESP_LOGE(TAG, "esp_wifi_set_mode failed: %s", esp_err_to_name(e));
            return e;
        }

        e = esp_wifi_start();
        if (e != ESP_OK) {
            ESP_LOGE(TAG, "esp_wifi_start failed: %s", esp_err_to_name(e));
            return e;
        }

        return ESP_OK;
    }

    // Start provisioning using Security 1
    wifi_prov_security_t security = WIFI_PROV_SECURITY_1;
    const char *service_key = cfg->service_key; // unused for BLE
    ESP_LOGI(TAG, "Starting BLE provisioning. service_name=%s", cfg->service_name);

    e = wifi_prov_mgr_start_provisioning(security, cfg->pop, cfg->service_name, service_key);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "wifi_prov_mgr_start_provisioning failed: %s", esp_err_to_name(e));
        return e;
    }

    print_qr(cfg->service_name, cfg->pop);
    return ESP_OK;
}

bool wifi_prov_mgr_app_is_connected(void)
{
    return s_connected;
}
