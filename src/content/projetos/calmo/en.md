---
titulo: CaLMo
resumo: A web tool for Causal Loop Diagram modeling, with a visual editor, automatic archetype detection and real-time collaborative editing. Best Paper at ERI-ES 2026.
periodo: '2026'
stack: [Vue.js, vis.js, Python, Flask, Flask-SocketIO, PostgreSQL, Apache Kafka, Nginx]
links:
  - rotulo: Open CaLMo
    url: https://dev.nemo.inf.ufes.br/calmo
  - rotulo: About NEMO
    url: https://nemo.inf.ufes.br/en/about/
destaque: 2
cor: '#0f8a7c'
---

**CaLMo** (*Causal Loop Diagram Modeler*) is a web tool for building and analyzing **Causal Loop Diagrams**, which systems thinking uses to show how the variables of a system influence each other. From the diagram, the tool finds feedback loops (reinforcing and balancing) and recognizes **system archetypes**, classic patterns such as "Fixes that Fail" and "Tragedy of the Commons".

The project is developed at **NEMO**, the Ontology and Conceptual Modeling Research Group at UFES. Founded in 2006, NEMO researches conceptual modeling and ontologies and is known for the Unified Foundational Ontology (UFO) and the OntoUML modeling language.

## What I built

Between April and October 2026, I was the main developer of the new version of CaLMo, with 70 of the project's 116 commits.

- **Visual editor (canvas):** I built the modeling screen from scratch in Vue.js and vis.js, for creating variables and relationships right on the diagram, undoing actions, exporting to PNG and switching between light and dark themes.
- **Live analysis:** loops and archetypes are identified while the diagram is being edited. There are eight archetypes (Fixes that Fail, Shifting the Burden, Limits to Success, Drifting Goals, Escalation, Success to the Successful, Tragedy of the Commons and Growth and Underinvestment), now also in their **delay-aware** variants.
- **Delays and subsystems:** delay notation on relationships and thematic subsystems to organize large diagrams.
- **Import and export** of variables, relationships and diagrams in JSON, CSV and **XMILE**, the standard format of system dynamics tools.
- **Real-time collaboration:** share links and simultaneous editing. Changes arrive over WebSocket (Flask-SocketIO) and go through an **Apache Kafka** broker, which orders every change and is the source of each diagram's edit history.
- **Architecture:** I refactored the frontend following MVVM, with components for the canvas modals and visual elements.
- **Deployment:** I put the system live on the NEMO server (gunicorn with eventlet under systemd, PostgreSQL, Kafka in Docker and Nginx) and wrote the deployment and maintenance guide for whoever comes next.

## Recognition

The work became the paper *Evolving CaLMo to Enhance Causal Loop Diagram Modeling*, which received the **Best Paper Award** at the Regional School of Informatics of Espírito Santo (ERI-ES 2026), co-authored with J. de Souza Borges, T. F. N. Lahass, A. B. Apolinário and M. P. Barcellos.
