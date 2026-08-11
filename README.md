# CraftifAI_Hackathon_RotatingMachineSentinel

> **Edge Predictive Maintenance Sentinel for Industrial Rotating Machinery**  
> *Generated using Craftif AI FirmGen (v0.3.1) for the Craftif AI Orbit Hackathon.*[cite: 1]

---

## Executive Summary & Problem Definition

In industrial manufacturing, power plants, and processing facilities, unexpected downtime on critical rotating equipment (e.g., induction motors, gearboxes, centrifugal pumps, and compressors) costs an average of $260,000 per hour[cite: 1]. Standard monitoring systems are often reactive, triggering alerts only after thermal or mechanical breakdown has already occurred[cite: 1].

The **Edge Predictive Maintenance Sentinel** is a multi-sensor, edge-processing IoT node powered by the **ESP32-S3**. It continuously samples high-frequency 3-axis vibration data and acoustic signals, performing real-time Digital Signal Processing (DSP) and Fast Fourier Transform (FFT) analysis directly at the edge. By detecting early bearing lubrication loss, rotor imbalance, and shaft misalignment, the sentinel transitions equipment monitoring from reactive maintenance to true predictive maintenance[cite: 1].

### Target Users & Applications
* **Plant Maintenance Engineers:** Require continuous, localized health indicators (ISO 10816 severity standards) without manual vibration probe readings.
* **SCADA / PLC System Operators:** Need native RS485 Modbus RTU telemetry directly integrated into factory automation networks.
* **Industry 4.0 Cloud Integrators:** Require lightweight MQTT JSON streams over Wi-Fi for remote fleet analytics dashboards.

---

## Hardware Architecture & Bill of Materials (BOM)

### Target Microcontroller
* **Development Board:** ESP32-S3-DevKitM-1 (N16R8)
* **Core Microcontroller:** Xtensa Dual-Core 32-bit LX7 (up to 240 MHz) with SIMD Vector Extensions
* **Memory Constraints:** 16MB Quad SPI Flash, 8MB Octal SPI PSRAM

### Pinout & Peripheral Assignment Map

The hardware interface map defines peripherals, pin allocations, DMA channels, and communication buses:

| Peripheral | Component | Bus / Protocol | ESP32-S3 Pin Allocation | Operational Role |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration Sensor** | ADXL355 | SPI2 (FSPI DMA) | `CS: GPIO10`, `SCK: GPIO12`<br>`MOSI: GPIO11`, `MISO: GPIO13` | High-precision 3-axis acceleration sampling up to 10 MHz (SPI Mode 3). |
| **Acoustic Sensor** | INMP441 | I2S0 (DMA) | `BCLK: GPIO14`, `WS: GPIO15`<br>`SD: GPIO16` | Continuous 16 kHz 16-bit PCM audio stream for bearing click/transient detection. |
| **Thermal Sensor** | Thermistor / PT100 | ADC1 (Channel 3) | `Signal: GPIO4` (11dB Atten) | Bearing temperature profiling with calibration fallback models. |
| **SCADA Interface** | MAX485 Transceiver | UART1 (RS485) | `TX: GPIO17`, `RX: GPIO18`<br>`DE/RTS: GPIO21` | Downstream industrial Modbus RTU slave interface (115200 8N1). |
| **Status Indicator** | WS2812B RGB LED | RMT Peripheral | `Data: GPIO48` | Multi-color visual health feedback (`NORMAL`, `WARNING`, `CRITICAL`). |
| **Connectivity** | Wi-Fi / BLE | Wireless | Internal (NimBLE Stack) | Bluetooth LE provisioning via ESP Provisioning mobile app + MQTT telemetry. |

> **Hardware Pin Guarding Constraint:**  
> GPIO48 is restricted on the ESP32-S3 DevKitM-1 as it is wired to the internal WS2812 LED. The firmware includes compile-time static assertions (`BOARD_STATIC_ASSERT_PIN_OK`) in `board_config.h` to prevent accidental assignment of sensor buses to GPIO48 or other strapped pins[cite: 2].

---

## Software Architecture & Firmware Engineering

The firmware is built using **ESP-IDF (v5.2+)** on FreeRTOS, structured with core separation, non-blocking task loops, and PSRAM memory buffers[cite: 2].

              +-----------------------------------+
              |  Industrial Rotating Equipment    |
              +-----------------------------------+
                 | (Vibration)  | (Acoustics)  | (Temp)
                 v              v              v
              +-----------------------------------+
              |      Hardware Drivers & DMA       |
              |  (SPI DMA, I2S DMA, ADC Read)     |
              +-----------------------------------+
                                |
                   [PSRAM Dynamic Ring Buffers][cite: 2]
                                |
      +-------------------------+-------------------------+
      | Core 1 (DSP & Sampling) | Core 0 (Control & Comms)|
      +-------------------------+-------------------------+
      | - Task_Vibration (DMA)  | - Task_State_Machine    |
      | - Task_Acoustics (I2S)  | - Task_Modbus_RS485     |
      | - Metric Calculation    | - Task_MQTT_Telemetry   |
      +-------------------------+-------------------------+
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
       +--------------------+        +--------------------+
       | RS485 / Modbus RTU |        | Wi-Fi MQTT Telemetry|
       | (Plant SCADA/PLC)  |        | (Cloud Dashboard)  |
       +--------------------+        +--------------------+

### FreeRTOS Dual-Core Task Distribution

1. **`Task_Vibration_Acquisition` (Core 1 | Priority 20):**
   * Reads 3-axis acceleration vectors from the ADXL355 over 10 MHz SPI DMA[cite: 2].
   * Pushes raw magnitude vectors into an 8MB PSRAM ring buffer (`ringbuf_psram.c`) using a `DROP_OLDEST` overflow strategy[cite: 2].
   * Computes Peak Acceleration ($g$), RMS Velocity ($mm/s$), and Crest Factor via vector-accelerated `ESP-DSP` library functions every 100 ms[cite: 2].
2. **`Task_Acoustic_Processing` (Core 1 | Priority 15):**
   * Ingests 512-byte PCM audio blocks from the INMP441 I2S DMA pipeline[cite: 2].
   * Executes short-time energy band calculations to detect ultrasonic acoustic transients (lubrication breakdown clicks)[cite: 2].
3. **`Task_State_Machine` (Core 0 | Priority 10):**
   * Evaluates machine metrics against ISO 10816 severity thresholds[cite: 2].
   * Controls system health state transitions (`NORMAL`, `WARNING`, `CRITICAL`) and drives WS2812 LED behavior[cite: 2].
   * Atomically updates local Modbus Input Registers (30001–30010)[cite: 2].
4. **`Task_Comms_Modbus_MQTT` (Core 0 | Priority 5):**
   * Continuously services incoming RS485 Modbus RTU master queries via UART1[cite: 2].
   * Dispatches periodic JSON telemetry packets over Wi-Fi/MQTT (QoS 1)[cite: 2].

---

## Industrial Fault Tolerance & Robustness

To ensure 24/7 reliability in noisy industrial electromagnetic interference (EMI) environments:

* **Automated SPI Bus Recovery:** If 5 consecutive SPI DMA timeouts occur (e.g., due to transient noise on the SPI clock), the driver automatically tears down and re-initializes the SPI host peripheral without rebooting the system[cite: 2].
* **Task Watchdog Timer (TWDT):** Critical sampling loops (`Task_Vibration_Acquisition` and `Task_State_Machine`) subscribe to the hardware TWDT, triggering a system reset if a thread starves or deadlocks[cite: 2].
* **PSRAM Allocation Fallback:** Dynamic allocations utilize `heap_caps_malloc(..., MALLOC_CAP_SPIRAM)`. If PSRAM allocation fails, system memory gracefully falls back to internal SRAM in degraded mode[cite: 2].
* **Bounded Queues & Non-Blocking Loops:** Data queues between Core 1 and Core 0 use single-element overwrite semantics (`xQueueOverwrite`) to eliminate backpressure deadlocks[cite: 2].

---

## Effective Use of FirmGen

This project was planned, designed, and synthesized using **Craftif AI FirmGen (v0.3.1)**[cite: 1, 2].

### Master Prompt Provided to FirmGen

```text
[SYSTEM CONTEXT]
Target Controller: ESP32-S3 (ESP32-S3-DevKitM-1 / N16R8, 16MB Flash, 8MB PSRAM)
Architecture: Xtensa Dual-Core LX7 with Vector Extensions (FreeRTOS)
Application Domain: Industrial Predictive Maintenance for Rotating Equipment
Goal: Generate modular, non-blocking, multi-task RTOS firmware with fault isolation, PSRAM dynamic ring buffers, ESP-DSP vector acceleration, and Modbus RTU / MQTT dual telemetry.

[HARDWARE MAPPINGS & CONFIGURATION - ESP32-S3 SPECIFIC]
- SPI Master (ADXL355 Vibration Sensor via SPI2/FSPI):
  * Pins: CS=10, SCK=12, MOSI=11, MISO=13
  * Clock Speed: 10 MHz via SPI DMA Channel Auto
- I2S Peripheral (INMP441 Acoustic Sensor):
  * Pins: SCK=14, WS=15, SD=16
  * Sample Rate: 16 kHz 16-bit PCM Mono
- ADC Channel (Thermal Sensor):
  * Pin: GPIO 4 (ADC1 Channel 3), 12-bit attenuation 11dB
- UART1 (RS485 Modbus RTU):
  * Pins: TX=17, RX=18, Direction Control (RTS/DE)=21
  * Baud Rate: 115200 8N1
- RMT Driver (Status Light):
  * Pin: GPIO 48 (ESP32-S3 Native On-Board Addressable RGB LED)

[SOFTWARE ARCHITECTURE & RTOS TASKS]
1. Core 1 - Task_Vibration_Acquisition (Priority: High / 20):
   - Continuously read 3-axis acceleration data via SPI DMA into a 1024-sample ring buffer allocated in PSRAM (using heap_caps_malloc with MALLOC_CAP_SPIRAM).
   - Compute Peak Acceleration (g), RMS Velocity (mm/s), and Crest Factor using ESP-DSP vector optimized functions.
   - Push calculated metrics into Queue_MachineHealth every 100 ms.

2. Core 1 - Task_Acoustic_Processing (Priority: Medium-High / 15):
   - Sample I2S audio stream in 512-byte PCM blocks into PSRAM.
   - Run short-time energy band analysis / FFT to detect high-frequency acoustic transients (ultrasonic clicks from bearing lubrication loss).

3. Core 0 - Task_State_Machine (Priority: Medium / 10):
   - Consume data from Queue_MachineHealth and read ADC GPIO 4.
   - Manage System State Machine:
     * NORMAL: Vibration RMS < 2.8 mm/s AND Temp < 65°C -> Status LED Green
     * WARNING: Vibration RMS 2.8–7.1 mm/s OR Temp 65–85°C -> Status LED Yellow
     * CRITICAL: Vibration RMS > 7.1 mm/s OR Temp > 85°C -> Status LED Flash Red
   - Maintain Modbus Registers (Input Registers 30001-30010) with live metrics.

4. Core 0 - Task_Comms_Modbus_MQTT (Priority: Low-Medium / 5):
   - Serve incoming RS485 Modbus RTU requests from SCADA PLC via UART1.
   - If Wi-Fi is connected, stream JSON telemetry packets over MQTT to central dashboard.

[FAULT TOLERANCE & INDUSTRIAL EDGE CASES]
- Implement automated SPI bus recovery routine: If 5 consecutive SPI DMA timeouts occur, re-initialize SPI peripheral bus without rebooting the system.
- Include Hardware Watchdog (Task WDT) subscription for Task_Vibration_Acquisition and Task_State_Machine.
- Driver Abstraction: Keep hardware registers encapsulated inside `adxl355.h/c`, `inmp441.h/c`, and `modbus_stack.h/c`.

[OUTPUT REQUIREMENTS]
Generate full C code including:
- main.c / main.h with app_main initialization, PSRAM health check, and FreeRTOS task creation pinned to specific cores.
- Pin configuration definitions header (board_config.h).
- State machine Enum definitions and state transition callbacks.
- FreeRTOS Queue, Semaphore, and PSRAM memory allocation wrappers.
```

---

## FirmGen Artifacts & Screenshots

### 1. Strategic Prompt Planning & Task List
FirmGen automatically decomposed the master prompt into 17 execution steps, managing dependencies, pin assertions, and driver abstractions[cite: 2].
* **Planning Phase:** ![Planning Phase](assets/FirmGenPlanning.jpg)
* **Generated Execution Plan:** ![Generated Execution Plan](assets/FirmGenTaskList.jpg)

### 2. Generated Firmware Topology & High-Level Architecture (HLD)
FirmGen synthesized a 14-node, 31-connection interactive firmware topology map establishing data bindings between physical pins, DMA channels, FreeRTOS tasks, and cloud/SCADA endpoints[cite: 2].
* **High-Level Architecture (HLD):** ![High-Level Architecture](assets/FirmGenHLD.jpg)
* **Wiring Topology Graph:** ![Wiring Topology Graph](assets/FirmGenFirmwareTree.jpg)

---

## Modbus Register Map & Telemetry Schema

### Modbus RTU Input Registers (30001–30010)

| Register Address | Metric | Units / Scaling | Description |
| :--- | :--- | :--- | :--- |
| **30001** | Vibration Velocity RMS | $0.1 \text{ mm/s}$ (e.g., $28 = 2.8\text{ mm/s}$) | Primary ISO 10816 severity metric[cite: 2]. |
| **30002** | Bearing Temperature | $0.1\ ^\circ\text{C}$ (e.g., $650 = 65.0\ ^\circ\text{C}$) | ADC1 thermistor reading[cite: 2]. |
| **30003** | Peak Acceleration | $0.01\ g$ (e.g., $150 = 1.50\ g$) | High-frequency impact indicator[cite: 2]. |
| **30004** | Crest Factor | Scaled $\times 100$ | Ratio of peak acceleration to RMS[cite: 2]. |
| **30005** | Acoustic Transient Score | $0 - 1000$ | Ultrasonic lubrication click index[cite: 2]. |
| **30006** | System Health State | Enum (0: NORMAL, 1: WARN, 2: CRIT) | Current machine operational state[cite: 2]. |
| **30007** | SPI Timeout Counter | Raw Integer | Fault telemetry counter for SPI recovery[cite: 2]. |
| **30008** | PSRAM Drop Counter | Raw Integer | Buffer overflow counter[cite: 2]. |
| **30009** | System Uptime (High) | Seconds (MSB 16-bit) | Uptime telemetry |
| **30010** | System Uptime (Low) | Seconds (LSB 16-bit) | Uptime telemetry |

### MQTT Telemetry JSON Payload
Published every 1000 ms to `device/mech-sentinel/telemetry`[cite: 2]:

```json
{
  "device_id": "mech-sentinel-01",
  "state": "NORMAL",
  "metrics": {
    "vibration_rms_mm_s": 1.42,
    "vibration_peak_g": 0.85,
    "crest_factor": 2.15,
    "temperature_c": 48.3,
    "acoustic_transient_score": 12
  },
  "diagnostics": {
    "psram_free_bytes": 7864320,
    "spi_timeouts": 0,
    "buffer_drops": 0
  }
}
```

---

## Build & Setup Instructions

### Prerequisites
* **ESP-IDF:** v5.2 or later installed and exported in path.
* **Target Board:** ESP32-S3-DevKitM-1 (N16R8)[cite: 2].

### 1. Repository Setup

```bash
git clone https://github.com/YourUsername/CraftifAI_Hackathon_RotatingMachineSentinel.git
cd CraftifAI_Hackathon_RotatingMachineSentinel/mech_sentinel_pm
```

### 2. Target Configuration & Building

```bash
# Set ESP32-S3 target
idf.py set-target esp32s3

# Build the project scaffold generated by FirmGen
idf.py build
```

### 3. Flashing & Monitoring

```bash
# Flash firmware and launch serial console
idf.py -p /dev/ttyUSB0 flash monitor
```

### 4. BLE Provisioning
Upon first boot or unprovisioned state, the device advertises over Bluetooth LE as `mech-sentinel`[cite: 2]. Scan the QR code emitted in the serial console using the **ESP SoftAP/BLE Provisioning** app (iOS/Android) to configure Wi-Fi credentials[cite: 2].

---

## Repository Structure

```text
CraftifAI_Hackathon_RotatingMachineSentinel/
├── README.md                           # Master Project Documentation
├── FirmGen_Chat_Export.html            # Complete Exported FirmGen Conversation Log
├── assets/                             # Screenshots & Architecture Visuals
│   ├── FirmGenPlanning.jpg             # FirmGen Prompt Planning Screenshot
│   ├── FirmGenTaskList.jpg            # FirmGen Task List Screenshot
│   ├── FirmGenHLD.jpg                  # FirmGen High-Level Architecture Graph
│   └── FirmGenFirmwareTree.jpg         # FirmGen Wiring Topology Graph
└── mech_sentinel_pm/                   # ESP-IDF C Project Source Directory
    ├── CMakeLists.txt
    ├── sdkconfig.defaults              # PSRAM, NimBLE & FreeRTOS Configurations
    ├── firmware/
    │   ├── configs/
    │   │   └── board_config.h          # Hardware Pin Allocations & Assertions
    │   ├── drivers/
    │   │   ├── adxl355.h/c             # SPI DMA ADXL355 Driver with Auto-Recovery
    │   │   ├── inmp441.h/c             # I2S DMA INMP441 Microphone Driver
    │   │   ├── thermal_adc.h/c         # ADC1 Calibration & Temperature Driver
    │   │   ├── status_led_ws2812.h/c   # RMT WS2812 Status LED Driver
    │   │   └── modbus_stack.h/c        # UART1 RS485 Half-Duplex Modbus Stack
    │   ├── dsp/
    │   │   └── vibration_metrics.h/c   # ESP-DSP Vector Acceleration Module
    │   ├── app/
    │   │   ├── state_machine.h/c       # ISO 10816 Health State Machine
    │   │   └── app_tasks.h/c           # FreeRTOS Dual-Core Task Creation
    │   ├── net/
    │   │   ├── wifi_prov_mgr.h/c       # BLE NimBLE Provisioning Manager
    │   │   └── mqtt_client_mgr.h/c     # MQTT Client & LWT Manager
    │   └── utils/
    │       ├── psram_alloc.h/c         # SPIRAM Dynamic Heap Wrappers
    │       └── ringbuf_psram.h/c       # Lock-Free PSRAM Ring Buffer
    └── main/
        └── app_main.c                  # System Initialization Entry Point
```

---

## Limitations & Future Roadmap

* **Physical FFT Resolution:** While current processing computes time-domain velocity RMS and peak values via vector operations, future firmware updates will integrate full 512-point FFT spectral bins over MQTT for detailed bearing defect frequency tracking (BPFO, BPFI).
* **Modbus RTU Slave Extension:** The included Modbus stack provides an atomic input register shadow map (30001–30010)[cite: 2]. Complete function code handlers (0x03, 0x04, 0x06) can be hooked directly into `modbus_stack_poll`[cite: 2].
* **Local Edge AI Inference:** The Xtensa LX7 SIMD vector instructions permit running quantized micro-TFLite anomaly detection models directly on the accelerometer ring buffer in PSRAM[cite: 2].
