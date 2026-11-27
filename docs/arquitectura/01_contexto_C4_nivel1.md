# Nivel 1 — Contexto

![Nivel 1 — Contexto](diagramas/c4_nivel1_contexto.svg)

La plataforma es la puerta única de los equipos al Hub. El equipo se registra con Entra External ID y envía cada ronda como pull request en GitHub. Recibe la validación y el puntaje como check runs en ese mismo PR.

| Actor o sistema | Papel |
| --- | --- |
| Equipo participante | Envía pronósticos (CSV hubverse), covariables y scripts de R o Python |
| Equipo INS | Publica las rondas, la serie observada y revisa los tableros |
| GitHub | Repositorio del hub, pull requests y GitHub Actions |
| Entra External ID | Registro e inicio de sesión de los participantes |
| SIVIGILA | Fuente de la serie observada contra la que se califica |
| Azure AI Foundry (Claude) | Lee el código y propone el plan de ejecución |

## Fuente Mermaid

```mermaid
flowchart LR
  EQ["👥 Equipo participante<br/>(investigadores)"]
  INS["🏛️ Equipo INS<br/>(coordinación del Hub)"]
  subgraph PLAT["Plataforma de participantes EpiModelling Hub"]
    P["Recibe, valida, revisa con IA,<br/>ejecuta y califica los envíos"]
  end
  GH["GitHub<br/>(repositorio del hub, PR, Actions)"]
  ENTRA["Microsoft Entra External ID<br/>(registro e inicio de sesión)"]
  SIV["SIVIGILA<br/>(casos observados)"]
  FOUNDRY["Azure AI Foundry<br/>(Claude)"]
  EQ -->|"se registra"| ENTRA
  EQ -->|"envía pull request con<br/>pronósticos, covariables y scripts"| GH
  GH -->|"webhook del PR"| P
  P -->|"check runs y comentarios"| GH
  P -->|"lee y propone plan"| FOUNDRY
  SIV -->|"serie observada semanal"| P
  INS -->|"publica rondas y revisa tableros"| P
  P -->|"tablero de puntajes"| INS
  P -->|"resultado y retroalimentación"| EQ
```
