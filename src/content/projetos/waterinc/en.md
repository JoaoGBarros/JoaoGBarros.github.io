---
titulo: WaterInc
resumo: An app that encourages people to drink more water, with sign-up, intake logging and a chart history, built in Flutter with Riverpod and Appwrite.
periodo: '2023'
stack: [Flutter, Dart, Riverpod, Appwrite, Java, Spring Boot]
repo: https://github.com/JoaoGBarros/WaterIncMobile
cor: '#0369a1'
---

WaterInc is a project to help people drink more water. The idea was to turn the habit into a game: every glass logged would earn points, and users would climb leaderboards and earn medals as they stayed consistent.

The **mobile app** was built in Flutter and already covers the core of that idea:

- sign-up and login with email and password;
- intake logging with quick buttons or free input, in mL or L;
- a history of what was logged, with charts.

Under the hood, the app uses **Appwrite** (running on a self-hosted instance) for authentication and data, and state is managed with **Riverpod**. The code is organized by feature (auth, water, home and user), each with the same split between API access, logic and screens.

The project also had a Java backend with Spring Boot and JPA. Leaderboards and medals stayed on the plan and were not implemented in this version.
