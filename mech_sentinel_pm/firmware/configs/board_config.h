#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

#include "hal/adc_types.h"
#include "hal/uart_types.h"
#include "driver/spi_master.h"

// Board: ESP32-S3 DevKitM-1 (N16R8)
// Notes:
// - GPIO48 is a RESTRICTED pin on this board and is wired to the on-board WS2812 RGB LED.
//   Use it ONLY for status LED output.
// - Avoid assigning peripherals to restricted pins: 0, 3, 19, 20, 26-32, 45, 46, 48.

// ---- Pin safety helpers ----
// Compile-time helpers to intentionally fail builds if a restricted pin is used.
#define BOARD_GPIO_IS_RESTRICTED(gpio_) \
    ((gpio_) == 0 || (gpio_) == 3 || (gpio_) == 19 || (gpio_) == 20 || \
     ((gpio_) >= 26 && (gpio_) <= 32) || (gpio_) == 45 || (gpio_) == 46 || (gpio_) == 48)

// Use this in headers where pin macros are defined. If a restricted pin is used, compilation fails.
#define BOARD_STATIC_ASSERT_PIN_OK(name_, gpio_) \
    _Static_assert(!BOARD_GPIO_IS_RESTRICTED(gpio_), "Restricted GPIO used for " name_)

// ---- SPI (ADXL355 via SPI2/FSPI) ----
#define BOARD_ADXL355_SPI_HOST          SPI2_HOST
#define BOARD_ADXL355_GPIO_CS           10
#define BOARD_ADXL355_GPIO_SCK          12
#define BOARD_ADXL355_GPIO_MOSI         11
#define BOARD_ADXL355_GPIO_MISO         13
#define BOARD_ADXL355_SPI_CLOCK_HZ      (10 * 1000 * 1000)

// ADXL355 typical SPI mode: Mode 3 (CPOL=1, CPHA=1)
#define BOARD_ADXL355_SPI_MODE          3

// ---- I2S (INMP441) ----
#define BOARD_INMP441_I2S_PORT          0
#define BOARD_INMP441_GPIO_BCLK         14
#define BOARD_INMP441_GPIO_WS           15
#define BOARD_INMP441_GPIO_DIN          16
#define BOARD_INMP441_SAMPLE_RATE_HZ    16000
#define BOARD_INMP441_BITS_PER_SAMPLE   16

// ---- ADC (thermal sensor) ----
// GPIO4 is ADC1 channel 3 on ESP32-S3
#define BOARD_THERMAL_ADC_UNIT          ADC_UNIT_1
#define BOARD_THERMAL_ADC_CHANNEL       ADC_CHANNEL_3
#define BOARD_THERMAL_ADC_ATTEN         ADC_ATTEN_DB_12
#define BOARD_THERMAL_ADC_BITWIDTH      ADC_BITWIDTH_12

// ---- UART1 (RS485 Modbus RTU) ----
#define BOARD_MODBUS_UART_NUM           UART_NUM_1
#define BOARD_MODBUS_GPIO_TX            17
#define BOARD_MODBUS_GPIO_RX            18
#define BOARD_MODBUS_GPIO_DE            21
#define BOARD_MODBUS_BAUDRATE           115200

// ---- Status LED (WS2812 via RMT) ----
#define BOARD_STATUS_LED_GPIO           48

// ---- Core pinning ----
#define BOARD_CORE_0                    0
#define BOARD_CORE_1                    1

// ---- Task priorities ----
#define BOARD_PRIO_VIBRATION            20
#define BOARD_PRIO_ACOUSTIC             15
#define BOARD_PRIO_STATE_MACHINE        10
#define BOARD_PRIO_COMMS                5

// ---- Task periods ----
#define BOARD_VIBRATION_METRICS_PERIOD_MS   100
#define BOARD_MQTT_PUBLISH_PERIOD_MS        1000

// ---- Pin assertions (do not remove) ----
BOARD_STATIC_ASSERT_PIN_OK("ADXL355 CS", BOARD_ADXL355_GPIO_CS);
BOARD_STATIC_ASSERT_PIN_OK("ADXL355 SCK", BOARD_ADXL355_GPIO_SCK);
BOARD_STATIC_ASSERT_PIN_OK("ADXL355 MOSI", BOARD_ADXL355_GPIO_MOSI);
BOARD_STATIC_ASSERT_PIN_OK("ADXL355 MISO", BOARD_ADXL355_GPIO_MISO);

BOARD_STATIC_ASSERT_PIN_OK("INMP441 BCLK", BOARD_INMP441_GPIO_BCLK);
BOARD_STATIC_ASSERT_PIN_OK("INMP441 WS", BOARD_INMP441_GPIO_WS);
BOARD_STATIC_ASSERT_PIN_OK("INMP441 DIN", BOARD_INMP441_GPIO_DIN);

BOARD_STATIC_ASSERT_PIN_OK("Modbus TX", BOARD_MODBUS_GPIO_TX);
BOARD_STATIC_ASSERT_PIN_OK("Modbus RX", BOARD_MODBUS_GPIO_RX);
BOARD_STATIC_ASSERT_PIN_OK("Modbus DE", BOARD_MODBUS_GPIO_DE);

// Intentionally allow GPIO48 only for status LED (documented restriction above).
_Static_assert(BOARD_STATUS_LED_GPIO == 48, "Status LED GPIO must be GPIO48 on DevKitM-1");

#endif // BOARD_CONFIG_H
