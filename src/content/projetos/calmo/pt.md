---
titulo: CaLMo
resumo: Ferramenta web para modelar Diagramas de Loops Causais, com editor visual, detecção automática de arquétipos e edição colaborativa em tempo real. Melhor Artigo na ERI-ES 2026.
periodo: '2026'
stack: [Vue.js, vis.js, Python, Flask, Flask-SocketIO, PostgreSQL, Apache Kafka, Nginx]
links:
  - rotulo: Abrir o CaLMo
    url: https://dev.nemo.inf.ufes.br/calmo
  - rotulo: Sobre o NEMO
    url: https://nemo.inf.ufes.br/en/about/
destaque: 2
cor: '#0f8a7c'
---

O **CaLMo** (*Causal Loop Diagram Modeler*) é uma ferramenta web para criar e analisar **Diagramas de Loops Causais**, usados no pensamento sistêmico para mostrar como as variáveis de um sistema se influenciam. A partir do diagrama, a ferramenta encontra os ciclos de realimentação (de reforço e de equilíbrio) e reconhece **arquétipos sistêmicos**, padrões clássicos como "Soluções que Falham" e "Tragédia dos Comuns".

O projeto é desenvolvido no **NEMO**, o Núcleo de Estudos em Modelagem Conceitual e Ontologias da UFES. Criado em 2006, o NEMO pesquisa modelagem conceitual e ontologias e é conhecido pela ontologia de fundamentação UFO e pela linguagem OntoUML.

## O que eu construí

Entre abril e outubro de 2026, fui o principal desenvolvedor da nova versão do CaLMo, com 70 dos 116 commits do projeto.

- **Editor visual (canvas):** construí do zero a tela de modelagem em Vue.js e vis.js, para criar variáveis e relações direto no diagrama, desfazer ações, exportar como PNG e alternar entre tema claro e escuro.
- **Análise ao vivo:** os ciclos e os arquétipos são identificados enquanto o diagrama é editado. São oito arquétipos (Soluções que Falham, Transferência de Responsabilidade, Limites ao Sucesso, Metas Declinantes, Escalada, Sucesso para os Bem-Sucedidos, Tragédia dos Comuns e Crescimento e Subinvestimento), agora também nas variações com **atraso**.
- **Atrasos e subsistemas:** notação de atraso nas relações e subsistemas temáticos para organizar diagramas grandes.
- **Importação e exportação** de variáveis, relações e diagramas em JSON, CSV e **XMILE**, o formato padrão das ferramentas de dinâmica de sistemas.
- **Colaboração em tempo real:** links de compartilhamento e edição simultânea. As alterações chegam por WebSocket (Flask-SocketIO) e passam por um broker **Apache Kafka**, que ordena cada mudança e serve de fonte para o histórico de edição do diagrama.
- **Arquitetura:** refatorei o frontend seguindo MVVM, com componentes para os modais e elementos visuais do canvas.
- **Deploy:** coloquei o sistema no ar no servidor do NEMO (gunicorn com eventlet via systemd, PostgreSQL, Kafka em Docker e Nginx) e escrevi o guia de deploy e manutenção para quem vier depois.

## Reconhecimento

O trabalho virou o artigo *Evolving CaLMo to Enhance Causal Loop Diagram Modeling*, que recebeu o **Prêmio de Melhor Artigo** na Escola Regional de Informática do Espírito Santo (ERI-ES 2026), em coautoria com J. de Souza Borges, T. F. N. Lahass, A. B. Apolinário e M. P. Barcellos.
