#include "ringbuf_psram.h"

#include <string.h>

#include "esp_heap_caps.h"
#include "esp_log.h"

static const char *TAG = "ringbuf_psram";

static inline void lock_take(SemaphoreHandle_t lock)
{
    (void)xSemaphoreTake(lock, portMAX_DELAY);
}

static inline void lock_give(SemaphoreHandle_t lock)
{
    (void)xSemaphoreGive(lock);
}

esp_err_t ringbuf_psram_init(ringbuf_psram_t *rb, size_t capacity_elems, size_t elem_size,
                            ringbuf_overflow_policy_t policy,
                            bool allocate_in_psram)
{
    if (!rb || capacity_elems == 0 || elem_size == 0) {
        return ESP_ERR_INVALID_ARG;
    }

    memset(rb, 0, sizeof(*rb));
    rb->capacity = capacity_elems;
    rb->elem_size = elem_size;
    rb->policy = policy;

    uint32_t caps = MALLOC_CAP_8BIT;
    if (allocate_in_psram) {
        caps |= MALLOC_CAP_SPIRAM;
    } else {
        caps |= MALLOC_CAP_INTERNAL;
    }

    rb->buf = (uint8_t *)heap_caps_malloc(capacity_elems * elem_size, caps);
    if (!rb->buf) {
        ESP_LOGE(TAG, "alloc failed: %u elems of %u bytes (caps=0x%08x)",
                 (unsigned)capacity_elems, (unsigned)elem_size, (unsigned)caps);
        return ESP_ERR_NO_MEM;
    }

    rb->lock = xSemaphoreCreateMutex();
    if (!rb->lock) {
        heap_caps_free(rb->buf);
        rb->buf = NULL;
        return ESP_ERR_NO_MEM;
    }

    ESP_LOGI(TAG, "init ok: capacity=%u elems, elem_size=%u bytes (%s)",
             (unsigned)capacity_elems, (unsigned)elem_size,
             allocate_in_psram ? "PSRAM" : "internal");

    return ESP_OK;
}

void ringbuf_psram_deinit(ringbuf_psram_t *rb)
{
    if (!rb) {
        return;
    }

    if (rb->lock) {
        vSemaphoreDelete(rb->lock);
        rb->lock = NULL;
    }

    if (rb->buf) {
        heap_caps_free(rb->buf);
        rb->buf = NULL;
    }

    memset(rb, 0, sizeof(*rb));
}

static inline size_t idx_next(ringbuf_psram_t *rb, size_t idx)
{
    idx++;
    if (idx >= rb->capacity) {
        idx = 0;
    }
    return idx;
}

bool ringbuf_psram_push(ringbuf_psram_t *rb, const void *elem)
{
    if (!rb || !rb->buf || !rb->lock || !elem) {
        return false;
    }

    lock_take(rb->lock);

    if (rb->count == rb->capacity) {
        if (rb->policy == RINGBUF_OVERFLOW_DROP_OLDEST) {
            rb->tail = idx_next(rb, rb->tail);
            rb->stats.drops_oldest++;
            // count remains full
        } else {
            rb->stats.drops_newest++;
            lock_give(rb->lock);
            return false;
        }
    } else {
        rb->count++;
    }

    memcpy(&rb->buf[rb->head * rb->elem_size], elem, rb->elem_size);
    rb->head = idx_next(rb, rb->head);
    rb->stats.pushes++;

    lock_give(rb->lock);
    return true;
}

bool ringbuf_psram_pop(ringbuf_psram_t *rb, void *out_elem)
{
    if (!rb || !rb->buf || !rb->lock || !out_elem) {
        return false;
    }

    lock_take(rb->lock);

    if (rb->count == 0) {
        lock_give(rb->lock);
        return false;
    }

    memcpy(out_elem, &rb->buf[rb->tail * rb->elem_size], rb->elem_size);
    rb->tail = idx_next(rb, rb->tail);
    rb->count--;
    rb->stats.pops++;

    lock_give(rb->lock);
    return true;
}

size_t ringbuf_psram_count(ringbuf_psram_t *rb)
{
    if (!rb || !rb->lock) {
        return 0;
    }

    lock_take(rb->lock);
    size_t c = rb->count;
    lock_give(rb->lock);
    return c;
}

ringbuf_stats_t ringbuf_psram_get_stats(ringbuf_psram_t *rb)
{
    ringbuf_stats_t s = {0};
    if (!rb || !rb->lock) {
        return s;
    }

    lock_take(rb->lock);
    s = rb->stats;
    lock_give(rb->lock);
    return s;
}
