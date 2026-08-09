#include "app.h"
#include "app_config.h"
#include "logger.h"

static const char *TAG = "app";

#include "esp_err.h"

#include "utils/psram_alloc.h"
#include "app/app_tasks.h"

void app_start(void)
{
    ESP_LOGI(TAG, "firmware started");

    // PSRAM health check (non-fatal; we can still run in degraded mode)
    (void)psram_alloc_health_check(64 * 1024);

    esp_err_t e = app_tasks_start();
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "app_tasks_start failed: %s", esp_err_to_name(e));
    }
}
