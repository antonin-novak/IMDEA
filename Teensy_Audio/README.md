# Teensy Audio Processing Examples

This collection of projects is designed to provide practical introduction examples for real-time audio processing using the Teensy microcontroller. It serves as educational support for IMDEA students at Le Mans University, covering various levels of Teensy board usage of simple audio signal processing, from basic filtering to complex systems integrating Python GUIs and Bluetooth connectivity.

## Projects Overview

### [1. Teensy Real-Time 2nd Order IIR Filter (`teensy_biquad_USB_serial`)](./teensy_biquad_USB_serial/)

This project demonstrates the application of a 2nd order Infinite Impulse Response (IIR) filter using a Teensy microcontroller. The Teensy board processes computer audio in real-time, with filter parameters adjustable over UART (USB serial port).

- **Key Features**: Direct audio processing on Teensy, real-time parameter adjustment.
- **Methods Used**: Teensy audio library, USB serial communication.

### [2. Teensy Real-Time 2nd Order IIR Filter with Python GUI (`teensy_biquad_USB_serial_pyqt`)](./teensy_biquad_USB_serial_pyqt/)

Expanding on the first project, this version integrates a Python-based PyQt GUI for dynamic filter design. Users can design filters in the GUI and send coefficients to the Teensy microcontroller for real-time audio processing.

- **Key Features**: Integration with Python GUI, dynamic filter design.
- **Methods Used**: PyQt, Teensy audio library, UART communication.

### [3. Teensy Biquad Filter with LINE Input and Potentiometers (`teensy_biquad_LINE_potentiometers`)](./teensy_biquad_LINE_potentiometers/)

This project enables real-time audio signal processing through line input, with filter parameters adjustable via physical potentiometers connected to the Teensy.

- **Key Features**: Physical control over filter parameters, direct line input processing.
- **Methods Used**: Teensy audio library, analog input.

### [4. Teensy Biquad Filter with LINE Input, Bluetooth, and ESP32 (`teensy_biquad_LINE_BLE_ESP32`)](./teensy_biquad_LINE_BLE_ESP32/)

The most complex project in this series combines a Python GUI, Teensy microcontroller, and ESP32 module for Bluetooth connectivity. It allows for wireless filter design and parameter adjustment, showcasing an advanced real-time audio processing system.

- **Key Features**: Bluetooth connectivity, wireless filter parameter adjustment.
- **Methods Used**: PyQt, Teensy audio library, ESP32 Bluetooth module, UART communication.

### [5. Audio Processor (`teensy_audio_processor_USB`)](./teensy_audio_processor_USB/)

This project shows how to implement your own algorithms on Teensy microcontroller. It implements the same project as the 1st one, except this time in stead of using the build-in biquad block from Teensy audio library, it implements it sample by sample in a C++ language. This project can be used as a starting point for more complex algorithm.

- **Key Features**: Direct audio processing on Teensy using own algorithms, real-time parameter adjustment.
- **Methods Used**: Own algorithm in C++, USB serial communication.



## Getting Started

Each project folder contains a detailed `README.md` with specific instructions on setup, dependencies, and usage. It is recommended to start with the first project (`teensy_biquad_USB_serial`) and progress sequentially to understand the fundamentals before moving on to the more complex systems.

## Prerequisites

- Teensy microcontroller and audio shield
- Arduino IDE for Teensy programming
- Python with PyQt for GUI projects
- ESP32 module for Bluetooth connectivity projects

## Support

This educational material is intended for IMDEA students at Le Mans University. For support or further information, please contact your course instructor or lab supervisor.
