---
titulo: AutoShinyHunter
resumo: Um bot em Python que caça Pokémon shiny sozinho em HeartGold/SoulSilver, usando visão computacional para reconhecer o que aparece na tela do emulador.
periodo: '2021'
stack: [Python, OpenCV, PyAutoGUI, deepgaze]
repo: https://github.com/JoaoGBarros/AutoShinyHunter
cor: '#a16207'
---

Quem joga Pokémon sabe: encontrar um **shiny** (a versão rara, de cor diferente, de um Pokémon) pode levar milhares de tentativas. Em vez de passar horas apertando os mesmos botões, eu escrevi um programa para fazer isso por mim.

O AutoShinyHunter joga Pokémon HeartGold/SoulSilver no emulador (testado no DeSmuME), controlando o teclado com PyAutoGUI. A cada tentativa, ele captura a tela e usa **OpenCV** e a biblioteca **deepgaze** para comparar as cores do Pokémon que apareceu com a versão normal. Quando a cor não bate, é shiny, e o bot para e avisa.

Ele começou como um projeto menor, só para o *soft reset* dos iniciais de Johto, e depois cresceu para:

- *soft reset* dos Pokémon iniciais;
- encontros selvagens nas rotas 29 e 30;
- *headbutt* e encontros estáticos, que ficaram na lista de planos.

Foi um dos meus primeiros projetos por conta própria, juntando duas coisas que eu gosto muito: Pokémon e automatizar tarefas chatas.
