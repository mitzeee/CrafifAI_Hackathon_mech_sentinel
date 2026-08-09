#ifndef RINGBUF_PSRAM_H
#define RINGBUF_PSRAM_H

#include <stddef.h>
#include <stdint.h>

#include "esp_err.h"
#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    RINGBUF_OVERFLOW_DROP_OLDEST = 0,
    RINGBUF_OVERFLOW_DROP_NEWEST = 1,
} ringbuf_overflow_policy_t;

typedef struct {
    uint32_t drops_oldest;
    uint32_t drops_newest;
    uint32_t pushes;
    uint32_t pops;
} ringbuf_stats_t;

typedef struct {
    uint8_t *buf;
    size_t capacity;
    size_t elem_size;

    size_t head; // next write
    size_t tail; // next read
    size_t count;

    ringbuf_overflow_policy_t policy;

    SemaphoreHandle_t lock;
    ringbuf_stats_t stats;
} ringbuf_psram_t;

esp_err_t ringbuf_psram_init(ringbuf_psram_t *rb, size_t capacity_elems, size_t elem_size,
                            ringbuf_overflow_policy_t policy,
                            bool allocate_in_psram);

void ringbuf_psram_deinit(ringbuf_psram_t *rb);

bool ringbuf_psram_push(ringbuf_psram_t *rb, const void *elem);

bool ringbuf_psram_pop(ringbuf_psram_t *rb, void *out_elem);

size_t ringbuf_psram_count(ringbuf_psram_t *rb);

ringbuf_stats_t ringbuf_psram_get_stats(ringbuf_psram_t *rb);

#ifdef __cplusplus
}
#endif

#endif // RINGBUF_PSRAM_H
