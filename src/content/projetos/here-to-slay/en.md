---
titulo: Here To Slay
resumo: An unofficial digital version of the Here to Slay card game, with an Electron desktop client and an event-driven backend on Apache Kafka.
periodo: '2025 – 2026'
stack: [React, TypeScript, Electron, Java 21, Apache Kafka, Docker, Nginx]
repo: https://github.com/JoaoGBarros/HereToSlay
destaque: 1
cor: '#34507f'
downloads: []
---

[Here to Slay](https://www.unstablegames.com) is a fantasy strategy card game by Unstable Games, TeeTurtle's games label and the team behind Unstable Unicorns. Each player builds a party of heroes, tries to slay monsters and, of course, sabotages their opponents along the way. This project is an unofficial digital version of the game, which I built to study distributed systems in practice and to play with friends.

The **client** is a React and TypeScript desktop app running on Electron. It talks to the backend through a WebSocket gateway, and the whole stack runs with Docker Compose behind an Nginx reverse proxy.

The **backend** is event-driven: the gateway, lobby and game-engine services never call each other directly and communicate only through an Apache Kafka cluster (3 brokers, KRaft mode). Game state is rebuilt through event sourcing, and crash recovery relies on compacted topics.

## Disclaimer

- This is an **unofficial, unlicensed fan project**. It is not affiliated with Unstable Games or TeeTurtle, and it is not sponsored, endorsed or approved by them.
- "Here to Slay", "Unstable Games", "TeeTurtle", card names, artwork and all other game elements are trademarks and intellectual property of their respective owners. I claim no ownership of any of them.
- The project is **non-commercial**: it is free, it is not sold and it generates no revenue of any kind. It exists for learning and portfolio purposes only.
- Card images were taken from the [official Unstable Games wiki](https://www.unstablegameswiki.com/index.php).
- If you enjoy the game, please support its creators and buy the [original Here to Slay](https://www.unstablegames.com).
- If you hold the rights to any of these elements and want them removed, [email me](mailto:jgabriel.b.rocha@gmail.com) and I will take the content down as soon as possible.
