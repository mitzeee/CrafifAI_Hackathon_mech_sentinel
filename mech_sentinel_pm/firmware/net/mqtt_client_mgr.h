#ifndef MQTT_CLIENT_MGR_H
#define MQTT_CLIENT_MGR_H

#include <stdbool.h>
#include <stdint.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    const char *broker_uri;       // e.g. mqtt://192.168.1.10:1883
    const char *client_id;
    const char *base_topic;       // e.g. device/<id>
    uint32_t keepalive_sec;
} mqtt_client_mgr_config_t;

typedef struct {
    mqtt_client_mgr_config_t cfg;
    void *client; // esp_mqtt_client_handle_t
    bool connected;
} mqtt_client_mgr_t;

esp_err_t mqtt_client_mgr_start(mqtt_client_mgr_t *m, const mqtt_client_mgr_config_t *cfg);

esp_err_t mqtt_client_mgr_stop(mqtt_client_mgr_t *m);

bool mqtt_client_mgr_is_connected(mqtt_client_mgr_t *m);

esp_err_t mqtt_client_mgr_publish_json(mqtt_client_mgr_t *m, const char *subtopic, const char *json);

#ifdef __cplusplus
}
#endif

#endif // MQTT_CLIENT_MGR_H
