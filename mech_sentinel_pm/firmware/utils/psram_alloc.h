#ifndef PSRAM_ALLOC_H
#define PSRAM_ALLOC_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    size_t bytes_allocated_spiram;
    size_t bytes_allocated_internal;
    size_t alloc_failures;
} psram_alloc_stats_t;

/**
 * @brief Initialize allocation statistics.
 */
void psram_alloc_init(void);

/**
 * @brief Allocate from PSRAM (preferred) with optional internal-RAM fallback.
 *
 * @param size        Bytes
 * @param alignment   Alignment in bytes (power of two). Use 0 to disable.
 * @param allow_fallback_internal If true, falls back to internal RAM when PSRAM alloc fails.
 */
void *psram_alloc(size_t size, size_t alignment, bool allow_fallback_internal);

/**
 * @brief Free memory allocated by psram_alloc.
 *
 * Note: Free works for both PSRAM and internal allocations.
 */
void psram_free(void *ptr);

/**
 * @brief Snapshot allocation stats.
 */
psram_alloc_stats_t psram_alloc_get_stats(void);

/**
 * @brief Basic PSRAM health check (alloc/free test).
 */
esp_err_t psram_alloc_health_check(size_t test_bytes);

#ifdef __cplusplus
}
#endif

#endif // PSRAM_ALLOC_H
