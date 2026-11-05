---
titulo: Pokémon UFES Crater
resumo: Um jogo de Pokémon multiplayer no navegador, com servidor autoritativo em Java, cliente em React e tudo em tempo real por WebSockets.
periodo: '2025'
stack: [Java 21, React, Vite, WebSockets, SQLite, Docker]
repo: https://github.com/JoaoGBarros/Pokemon-UFES-Crater
cor: '#2563eb'
---

Um jogo de Pokémon multiplayer para o navegador, feito para o trabalho de Redes de Computadores da UFES (2025/1), cujo desafio era construir um servidor de jogo multiplayer.

A inspiração foi o **Pokémon Crater**, um antigo jogo de fã que rodava no navegador e deixava vários jogadores explorarem o mesmo mapa e batalharem entre si. Aqui, os jogadores se conectam, se veem num mundo compartilhado, andam em tempo real e podem:

- batalhar uns contra os outros em duelos 1v1 por turnos;
- enfrentar Pokémon selvagens, que são encontros só daquele jogador;
- conversar pelo chat do jogo.

O **servidor** é autoritativo e escrito em Java 21: é ele quem guarda o estado do jogo e decide o que vale, e os clientes só mostram o resultado. A comunicação é toda por **WebSockets**, o que exige cuidado especial nas batalhas PvP, porque os dois participantes precisam ver exatamente a mesma coisa ao mesmo tempo. O **cliente** é em React com Vite, os dados dos jogadores ficam em SQLite e o projeto inteiro sobe com um `docker-compose up`.
