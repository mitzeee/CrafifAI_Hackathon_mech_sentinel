#include "psram_alloc.h"

#include <string.h>

#include "esp_heap_caps.h"
#include "esp_log.h"

static const char *TAG = "psram_alloc";

static psram_alloc_stats_t s_stats;

void psram_alloc_init(void)
{
    memset(&s_stats, 0, sizeof(s_stats));
}

static void *alloc_caps(size_t size, size_t alignment, uint32_t caps)
{
    if (alignment && alignment > 1) {
        return heap_caps_aligned_alloc(alignment, size, caps);
    }
    return heap_caps_malloc(size, caps);
}

void *psram_alloc(size_t size, size_t alignment, bool allow_fallback_internal)
{
    void *p = alloc_caps(size, alignment, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
    if (p) {
        s_stats.bytes_allocated_spiram += size;
        return p;
    }

    s_stats.alloc_failures++;
    ESP_LOGW(TAG, "PSRAM alloc failed (size=%u).%s", (unsigned)size,
             allow_fallback_internal ? " Falling back to internal RAM" : "");

    if (!allow_fallback_internal) {
        return NULL;
    }

    p = alloc_caps(size, alignment, MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
    if (p) {
        s_stats.bytes_allocated_internal += size;
    }
    return p;
}

void psram_free(void *ptr)
{
    heap_caps_free(ptr);
}

psram_alloc_stats_t psram_alloc_get_stats(void)
{
    return s_stats;
}

esp_err_t psram_alloc_health_check(size_t test_bytes)
{
    void *p = heap_caps_malloc(test_bytes, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
    if (!p) {
        ESP_LOGE(TAG, "PSRAM health check failed: alloc %u bytes", (unsigned)test_bytes);
        return ESP_ERR_NO_MEM;
    }

    memset(p, 0xA5, test_bytes);

    // Touch a few positions to ensure memory is mapped and writable
    volatile uint8_t *b = (volatile uint8_t *)p;
    uint8_t v = b[0] ^ b[test_bytes / 2] ^ b[test_bytes - 1];
    (void)v;

    heap_caps_free(p);
    ESP_LOGI(TAG, "PSRAM health check OK (%u bytes)", (unsigned)test_bytes);
    return ESP_OK;
}
