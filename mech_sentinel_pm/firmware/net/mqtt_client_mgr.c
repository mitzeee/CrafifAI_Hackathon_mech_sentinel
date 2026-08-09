#include "mqtt_client_mgr.h"

#include <string.h>

#include "esp_log.h"
#include "mqtt_client.h"

static const char *TAG = "mqtt_mgr";

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    (void)base;
    (void)event_id;

    mqtt_client_mgr_t *m = (mqtt_client_mgr_t *)handler_args;
    esp_mqtt_event_handle_t ev = (esp_mqtt_event_handle_t)event_data;

    switch ((esp_mqtt_event_id_t)ev->event_id) {
    case MQTT_EVENT_CONNECTED:
        m->connected = true;
        ESP_LOGI(TAG, "connected");
        break;
    case MQTT_EVENT_DISCONNECTED:
        m->connected = false;
        ESP_LOGW(TAG, "disconnected");
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGW(TAG, "error");
        break;
    default:
        break;
    }
}

esp_err_t mqtt_client_mgr_start(mqtt_client_mgr_t *m, const mqtt_client_mgr_config_t *cfg)
{
    if (!m || !cfg || !cfg->broker_uri || !cfg->client_id || !cfg->base_topic) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(m, 0, sizeof(*m));
    m->cfg = *cfg;

    esp_mqtt_client_config_t mc = {
        .broker.address.uri = cfg->broker_uri,
        .credentials.client_id = cfg->client_id,
        .session.keepalive = cfg->keepalive_sec,
        .network.disable_auto_reconnect = false,
    };

    // LWT: device/<id>/status = offline
    char lwt_topic[128];
    snprintf(lwt_topic, sizeof(lwt_topic), "%s/status", cfg->base_topic);
    mc.session.last_will.topic = lwt_topic;
    mc.session.last_will.msg = "offline";
    mc.session.last_will.qos = 1;
    mc.session.last_will.retain = 0;

    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mc);
    if (!client) {
        return ESP_ERR_NO_MEM;
    }

    m->client = client;

    esp_err_t re = esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, m);
    if (re != ESP_OK) {
        ESP_LOGE(TAG, "register_event failed: %s", esp_err_to_name(re));
        return re;
    }

    esp_err_t e = esp_mqtt_client_start(client);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "start failed: %s", esp_err_to_name(e));
        return e;
    }

    ESP_LOGI(TAG, "starting: %s", cfg->broker_uri);
    return ESP_OK;
}

esp_err_t mqtt_client_mgr_stop(mqtt_client_mgr_t *m)
{
    if (!m) {
        return ESP_ERR_INVALID_ARG;
    }

    if (m->client) {
        esp_mqtt_client_handle_t client = (esp_mqtt_client_handle_t)m->client;
        (void)esp_mqtt_client_stop(client);
        (void)esp_mqtt_client_destroy(client);
        m->client = NULL;
    }

    memset(m, 0, sizeof(*m));
    return ESP_OK;
}

bool mqtt_client_mgr_is_connected(mqtt_client_mgr_t *m)
{
    return m && m->connected;
}

esp_err_t mqtt_client_mgr_publish_json(mqtt_client_mgr_t *m, const char *subtopic, const char *json)
{
    if (!m || !m->client || !subtopic || !json) {
        return ESP_ERR_INVALID_ARG;
    }

    if (!m->connected) {
        return ESP_ERR_INVALID_STATE;
    }

    char topic[192];
    snprintf(topic, sizeof(topic), "%s/%s", m->cfg.base_topic, subtopic);

    int msg_id = esp_mqtt_client_publish((esp_mqtt_client_handle_t)m->client,
                                        topic, json, 0 /* len */, 1 /* qos */, 0 /* retain */);
    if (msg_id < 0) {
        return ESP_FAIL;
    }

    return ESP_OK;
}
