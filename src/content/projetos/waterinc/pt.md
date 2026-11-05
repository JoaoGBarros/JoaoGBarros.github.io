---
titulo: WaterInc
resumo: Um app para incentivar a beber mais água, com cadastro, registro do consumo e histórico em gráficos, feito em Flutter com Riverpod e Appwrite.
periodo: '2023'
stack: [Flutter, Dart, Riverpod, Appwrite, Java, Spring Boot]
repo: https://github.com/JoaoGBarros/WaterIncMobile
cor: '#0369a1'
---

O WaterInc é um projeto para ajudar as pessoas a beber mais água. A ideia era transformar o hábito num jogo: cada copo registrado contaria pontos, e os usuários subiriam em rankings e ganhariam medalhas conforme mantivessem a constância.

O **app mobile** foi feito em Flutter e já cobre a base dessa ideia:

- cadastro e login com email e senha;
- registro do consumo com botões rápidos ou entrada livre, em mL ou L;
- histórico do que foi registrado, com gráficos.

Por trás, o app usa o **Appwrite** (rodando numa instância própria) para autenticação e banco de dados, e o estado é gerenciado com **Riverpod**. O código é organizado por funcionalidade (auth, água, home e usuário), cada uma com a mesma divisão entre acesso à API, regras e telas.

O projeto também teve um backend em Java com Spring Boot e JPA. Os rankings e as medalhas ficaram no plano e não chegaram a ser implementados nesta versão.
