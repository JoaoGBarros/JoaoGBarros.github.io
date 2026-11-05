---
titulo: Hockey de Mesa
resumo: Um hockey de mesa automatizado, com jogadores impressos em 3D sobre trilhos de impressora, chute por solenoide e controles Bluetooth ligados a um ESP32.
periodo: '2025'
stack: [ESP32, C++, Bluepad32, Motores de passo, Solenoides, Blender, Impressão 3D]
repo: https://github.com/JoaoGBarros/Hockey-de-Mesa
links:
  - rotulo: Fotos, vídeos e arquivos
    url: https://drive.google.com/drive/folders/1O0BGBbFdcr47wDU5BUUsXc0_4UtAozr7?usp=sharing
destaque: 3
cor: '#b9562a'
---

Um jogo de hockey de mesa automatizado, inspirado no pebolim e no air hockey, feito em grupo com Luca Avila e Tales Viana Ferracioli para a disciplina de Projeto Integrado de Computação II da UFES (2025/1).

Dois jogadores se enfrentam com controles Bluetooth. Cada "atleta" corre sobre um trilho tirado de uma impressora velha, e o chute é dado por um solenoide de impacto que empurra a bola em direção ao gol adversário. Tudo é coordenado por um **ESP32**, que lê os controles com a biblioteca Bluepad32, move os motores de passo pela ponte H e aciona os solenoides pelos relés.

- **Joystick esquerdo:** move o jogador ao longo do trilho.
- **X (PlayStation) / A (Xbox):** chuta.
- **L2 + R2 / LT + RT:** um comando especial que inverte, por um tempo, os controles do adversário.

O projeto começou literalmente no lixo eletrônico: buscamos impressoras usadas na UFES e desmontamos para aproveitar os trilhos dos cartuchos. Depois vieram os testes dos motores, a conexão dos controles e os solenoides, um de cada vez. Os jogadores foram modelados no Blender (foram cinco versões até acertar o tamanho) e impressos em 3D, e a caixa de MDF e o campo foram construídos com a ajuda do Reginaldo, marceneiro do CT.
