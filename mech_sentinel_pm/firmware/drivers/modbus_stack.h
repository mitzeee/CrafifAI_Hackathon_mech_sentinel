#ifndef MODBUS_STACK_H
#define MODBUS_STACK_H

#include <stdint.h>
#include <stdbool.h>

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// Input registers 30001-30010 (10 regs)
#define MODBUS_INPUT_REG_BASE   30001
#define MODBUS_INPUT_REG_COUNT  10

typedef struct {
    int uart_num; // uart_port_t
    int gpio_tx;
    int gpio_rx;
    int gpio_de;
    int baudrate;
    uint8_t slave_id;
} modbus_stack_config_t;

typedef struct {
    // Signed/unsigned scaled values packed into 16-bit input registers.
    // Define scaling in your application layer.
    uint16_t input_regs[MODBUS_INPUT_REG_COUNT];
    uint32_t fault_flags;
} modbus_register_map_t;

typedef struct {
    modbus_stack_config_t cfg;
    modbus_register_map_t regs;
    bool initialized;
    void *lock; // SemaphoreHandle_t
} modbus_stack_t;

esp_err_t modbus_stack_init(modbus_stack_t *mb, const modbus_stack_config_t *cfg);

esp_err_t modbus_stack_deinit(modbus_stack_t *mb);

/**
 * @brief Update a single input register (30001-based) atomically.
 */
esp_err_t modbus_stack_set_input_reg(modbus_stack_t *mb, uint16_t reg_addr_30001, uint16_t value);

/**
 * @brief Serve Modbus RTU requests (non-blocking polling step).
 *
 * This is a placeholder (minimal) dispatcher; full RTU parsing can be expanded.
 */
esp_err_t modbus_stack_poll(modbus_stack_t *mb);

#ifdef __cplusplus
}
#endif

#endif // MODBUS_STACK_H
