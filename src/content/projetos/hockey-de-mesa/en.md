---
titulo: Table Hockey
resumo: An automated table hockey game, with 3D-printed players on printer rails, solenoid kicks and Bluetooth controllers wired to an ESP32.
periodo: '2025'
stack: [ESP32, C++, Bluepad32, Stepper motors, Solenoids, Blender, 3D printing]
repo: https://github.com/JoaoGBarros/Hockey-de-Mesa
links:
  - rotulo: Photos, videos and files
    url: https://drive.google.com/drive/folders/1O0BGBbFdcr47wDU5BUUsXc0_4UtAozr7?usp=sharing
destaque: 3
cor: '#b9562a'
---

An automated table hockey game, inspired by foosball and air hockey, built as a team with Luca Avila and Tales Viana Ferracioli for the Integrated Computing Project II course at UFES (2025/1).

Two players face off using Bluetooth controllers. Each "athlete" runs on a rail salvaged from an old printer, and the kick comes from an impact solenoid that pushes the ball toward the opponent's goal. Everything is coordinated by an **ESP32**, which reads the controllers with the Bluepad32 library, drives the stepper motors through an H-bridge and fires the solenoids through relays.

- **Left stick:** moves the player along the rail.
- **X (PlayStation) / A (Xbox):** kick.
- **L2 + R2 / LT + RT:** a special move that inverts the opponent's controls for a while.

The project literally started in e-waste: we collected used printers around UFES and took them apart to reuse the cartridge rails. Then came testing the motors, connecting the controllers and the solenoids, one at a time. The players were modeled in Blender (it took five versions to get the size right) and 3D-printed, and the MDF box and field were built with help from Reginaldo, the campus carpenter.
