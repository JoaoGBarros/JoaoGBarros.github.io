---
titulo: AutoShinyHunter
resumo: A Python bot that hunts shiny Pokémon on its own in HeartGold/SoulSilver, using computer vision to recognize what shows up on the emulator screen.
periodo: '2021'
stack: [Python, OpenCV, PyAutoGUI, deepgaze]
repo: https://github.com/JoaoGBarros/AutoShinyHunter
cor: '#a16207'
---

Anyone who plays Pokémon knows: finding a **shiny** (the rare, differently colored version of a Pokémon) can take thousands of attempts. Instead of spending hours pressing the same buttons, I wrote a program to do it for me.

AutoShinyHunter plays Pokémon HeartGold/SoulSilver on an emulator (tested on DeSmuME), driving the keyboard with PyAutoGUI. On every attempt it captures the screen and uses **OpenCV** and the **deepgaze** library to compare the colors of the Pokémon that appeared with its regular version. When the colors don't match, it's a shiny, and the bot stops and lets me know.

It started as a smaller project, only for *soft resetting* the Johto starters, and then grew to cover:

- *soft resetting* the starter Pokémon;
- wild encounters on routes 29 and 30;
- *headbutt* and static encounters, which stayed on the to-do list.

It was one of my first projects on my own, combining two things I really enjoy: Pokémon and automating boring tasks.
