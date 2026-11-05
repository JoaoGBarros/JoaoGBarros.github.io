---
titulo: Pokémon UFES Crater
resumo: A multiplayer Pokémon game in the browser, with an authoritative Java server, a React client and everything in real time over WebSockets.
periodo: '2025'
stack: [Java 21, React, Vite, WebSockets, SQLite, Docker]
repo: https://github.com/JoaoGBarros/Pokemon-UFES-Crater
cor: '#2563eb'
---

A multiplayer Pokémon game for the browser, built for the Computer Networks course at UFES (2025/1), where the challenge was to build a multiplayer game server.

The inspiration was **Pokémon Crater**, an old fan-made browser game that let lots of players explore the same map and battle each other. Here, players connect, see each other in a shared world, move around in real time and can:

- battle each other in turn-based 1v1 duels;
- face wild Pokémon, which are encounters unique to each player;
- talk through the in-game chat.

The **server** is authoritative and written in Java 21: it holds the game state and decides what counts, while clients just display the result. All communication goes over **WebSockets**, which takes extra care in PvP battles, since both players need to see exactly the same thing at the same time. The **client** is React with Vite, player data lives in SQLite, and the whole project starts with a single `docker-compose up`.
