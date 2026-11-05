---
titulo: Magnetic Levitator
resumo: An object floating in mid-air thanks to an electromagnet controlled by PID on an ESP32, with live gain tuning and telemetry on Grafana.
periodo: '2025'
stack: [ESP32, C++, FreeRTOS, PID control, PWM, Grafana Cloud]
repo: https://github.com/JoaoGBarros/Levitador_Magnetico
links:
  - rotulo: Videos of it working
    url: https://github.com/JoaoGBarros/Levitador_Magnetico/tree/main/V%C3%ADdeos%20de%20Funcionamento
  - rotulo: Circuit photos
    url: https://github.com/JoaoGBarros/Levitador_Magnetico/tree/main/Fotos%20do%20Circuito
cor: '#2f6f73'
---

A magnetic levitator built as a team for the Embedded Systems course at UFES (2024/2): an electromagnet keeps an object floating in mid-air, correcting its force dozens of times per second so it neither falls nor snaps up to the magnet.

The **ESP32** reads the object's distance with an infrared sensor (turning voltage into centimeters with a calibration curve), computes the error against the target height and applies **PID control**. The result becomes a 10 kHz PWM signal that sets how hard the electromagnet pulls.

Two details made it much more fun to tune:

- **Live gain tuning:** a rotary encoder changes Kp, Ki and Kd while the system is running, and an LCD shows the current values. The encoder is read in a separate FreeRTOS task, on the ESP32's other core, so it never gets in the way of the control loop.
- **Telemetry:** the ESP32 joins Wi-Fi and sends the gains and the error to Grafana Cloud, so you can watch on a chart how the system reacts to every change.
