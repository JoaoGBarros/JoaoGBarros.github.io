---
titulo: Pong em Assembly
resumo: Pong escrito do zero em Assembly x86 de 16 bits, desenhando direto na memória de vídeo VGA, com níveis de dificuldade, pausa e blocos nas laterais.
periodo: '2024'
stack: [Assembly x86, NASM, DOS, VGA]
repo: https://github.com/JoaoGBarros/T1-Embarcados
cor: '#334155'
---

Um Pong completo escrito em **Assembly x86 de 16 bits**, feito em grupo com Luca Avila e Tales Viana para a disciplina de Sistemas Embarcados da UFES (2024/2). São quase 1.400 linhas sem nenhuma biblioteca: cada pixel na tela foi desenhado pelo nosso código.

O jogo roda no modo gráfico VGA de 640×480 e desenha a bola, as raquetes e o cenário escrevendo direto na memória de vídeo e nas portas da placa. Para a imagem não piscar, o laço principal espera o **sincronismo vertical** do monitor antes de redesenhar, e só apaga e redesenha o que se moveu.

Além do jogo em si, tem:

- tela de escolha de dificuldade (fácil, médio e difícil);
- pausa, reiniciar e sair, com confirmação;
- blocos coloridos nas laterais do campo;
- tela de *game over*.

Trabalhar nesse nível muda a forma de pensar: não existe "desenhe um círculo", existe calcular cada ponto, cuidar de cada registrador e lembrar o que estava na tela antes.
