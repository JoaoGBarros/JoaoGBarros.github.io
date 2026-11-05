---
titulo: Levitador Magnético
resumo: Um objeto flutuando no ar graças a um eletroímã controlado por PID em um ESP32, com ajuste dos ganhos em tempo real e telemetria no Grafana.
periodo: '2025'
stack: [ESP32, C++, FreeRTOS, Controle PID, PWM, Grafana Cloud]
repo: https://github.com/JoaoGBarros/Levitador_Magnetico
links:
  - rotulo: Vídeos funcionando
    url: https://github.com/JoaoGBarros/Levitador_Magnetico/tree/main/V%C3%ADdeos%20de%20Funcionamento
  - rotulo: Fotos do circuito
    url: https://github.com/JoaoGBarros/Levitador_Magnetico/tree/main/Fotos%20do%20Circuito
cor: '#2f6f73'
---

Um levitador magnético feito em grupo para a disciplina de Sistemas Embarcados da UFES (2024/2): um eletroímã segura um objeto flutuando no ar, corrigindo a força dezenas de vezes por segundo para ele não cair nem grudar.

O **ESP32** lê a distância do objeto com um sensor infravermelho (convertendo a tensão em centímetros com uma curva de calibração), calcula o erro em relação à altura desejada e aplica um **controle PID**. O resultado vira um sinal PWM de 10 kHz que define quanta força o eletroímã faz.

Dois detalhes deixaram o projeto mais divertido de ajustar:

- **Ganhos ajustáveis na hora:** um encoder rotativo permite mudar Kp, Ki e Kd com o sistema funcionando, e um display LCD mostra os valores atuais. A leitura do encoder roda numa tarefa separada do FreeRTOS, no outro núcleo do ESP32, para não atrapalhar o laço de controle.
- **Telemetria:** o ESP32 se conecta ao Wi-Fi e envia os ganhos e o erro para o Grafana Cloud, então dá para ver em gráfico como o sistema reage a cada ajuste.
