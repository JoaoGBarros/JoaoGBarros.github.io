---
titulo: Here To Slay
resumo: Versão digital não oficial do jogo de cartas Here to Slay, com client desktop em Electron e backend orientado a eventos sobre Apache Kafka.
periodo: '2025 – 2026'
stack: [React, TypeScript, Electron, Java 21, Apache Kafka, Docker, Nginx]
repo: https://github.com/JoaoGBarros/HereToSlay
destaque: 1
cor: '#34507f'
# Para publicar um download, adicione itens assim (a URL normalmente é de uma GitHub Release):
# downloads:
#   - rotulo: Client para Windows
#     plataforma: Windows
#     versao: '1.0.0'
#     tamanho: 84 MB
#     data: 2026-11-01
#     url: https://github.com/JoaoGBarros/HereToSlay/releases/download/v1.0.0/here-to-slay-setup.exe
downloads: []
---

O [Here to Slay](https://www.unstablegames.com) é um jogo de cartas de estratégia e fantasia da Unstable Games, marca da TeeTurtle e a mesma equipe por trás de Unstable Unicorns. Cada jogador monta um grupo de heróis, tenta derrotar monstros e, claro, sabotar os adversários pelo caminho. Este projeto é uma versão digital não oficial do jogo, que construí para estudar sistemas distribuídos na prática e jogar com os amigos.

O **client** é uma aplicação desktop em React e TypeScript rodando sobre Electron. Ele conversa com o backend por um gateway WebSocket, e toda a stack sobe com Docker Compose atrás de um reverse proxy Nginx.

O **backend** é orientado a eventos: os serviços de gateway, lobby e game-engine não se chamam diretamente, e se comunicam apenas por um cluster Apache Kafka (3 brokers, em modo KRaft). O estado das partidas é reconstruído por event sourcing, e a recuperação de falhas usa tópicos compactados.

## Aviso legal

- Este é um **projeto de fã, não oficial e não licenciado**. Ele não tem nenhuma relação com a Unstable Games ou a TeeTurtle, e não é patrocinado, endossado nem aprovado por elas.
- "Here to Slay", "Unstable Games", "TeeTurtle", os nomes das cartas, as ilustrações e os demais elementos do jogo são marcas e propriedade intelectual de seus respectivos donos. Não reivindico a posse de nenhum deles.
- O projeto **não tem fins lucrativos**: é gratuito, não é vendido e não gera nenhum tipo de receita. Existe apenas para fins de estudo e de portfólio.
- As imagens das cartas foram obtidas na [wiki oficial da Unstable Games](https://www.unstablegameswiki.com/index.php).
- Se você gostou do jogo, apoie quem o criou e compre o [Here to Slay original](https://www.unstablegames.com).
- Se você detém os direitos sobre algum desses elementos e quer que ele seja removido, [me mande um email](mailto:jgabriel.b.rocha@gmail.com) e eu retiro o conteúdo o quanto antes.
