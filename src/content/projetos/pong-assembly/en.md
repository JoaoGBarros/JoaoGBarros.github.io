---
titulo: Pong in Assembly
resumo: Pong written from scratch in 16-bit x86 Assembly, drawing straight into VGA video memory, with difficulty levels, pause and side blocks.
periodo: '2024'
stack: [x86 Assembly, NASM, DOS, VGA]
repo: https://github.com/JoaoGBarros/T1-Embarcados
cor: '#334155'
---

A complete Pong written in **16-bit x86 Assembly**, built as a team with Luca Avila and Tales Viana for the Embedded Systems course at UFES (2024/2). It's almost 1,400 lines with no libraries at all: every pixel on screen is drawn by our own code.

The game runs in 640×480 VGA graphics mode and draws the ball, paddles and field by writing straight to video memory and the graphics card's ports. To keep the picture from flickering, the main loop waits for the monitor's **vertical sync** before redrawing, and only erases and redraws what moved.

Besides the game itself, it has:

- a difficulty selection screen (easy, medium and hard);
- pause, restart and quit, with confirmation;
- colored blocks along the sides of the field;
- a game over screen.

Working at this level changes how you think: there is no "draw a circle", there is computing every point, keeping track of every register and remembering what was on screen before.
