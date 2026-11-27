# Nivel 2 — Contenedores

![Nivel 2 — Contenedores](diagramas/c4_nivel2_contenedores.svg)

| Contenedor | Tecnología | Responsabilidad |
| --- | --- | --- |
| Portal de participantes | App Service, Streamlit | Registro, perfil del equipo, estado de sus envíos y tablero |
| Repositorio del hub | GitHub | `model-output/`, `model-metadata/`, `hub-config/` |
| Validación en el PR | GitHub Actions | Revisión rápida del formato antes del webhook |
| Orquestador | Azure Functions + Storage Queue | Recibe el webhook, encola y mueve los estados |
| Jobs del pipeline | Container Apps Jobs | Recolector, Validador oficial, Agente revisor, Motor de puntaje |
| Sandbox | Container Apps, sesiones dinámicas | Ejecuta el código de los equipos sin internet |
| Almacenamiento | Blob Storage con retención inmutable | Copia de cada envío con SHA-256 |
| Base de datos | PostgreSQL Flexible Server | Equipos, envíos, `ejecucion_eventos`, puntajes |
| Secretos | Key Vault | Token de la GitHub App, claves de Foundry |
| IA | Azure AI Foundry | Despliegue de Claude para el Agente revisor |
| Observabilidad | Application Insights, Azure Monitor | Trazas, métricas y alertas |

## Fuente Mermaid

```mermaid
flowchart TB
  EQ["Equipo participante"]
  subgraph GITHUB["GitHub"]
    REPO["Repositorio del hub<br/>model-output/, model-metadata/"]
    GHA["GitHub Actions<br/>validación hubverse"]
  end
  subgraph AZ["Azure — rg-epimodeling-plataforma"]
    PORTAL["Portal de participantes<br/>App Service (Streamlit)"]
    ENTRA["Entra External ID"]
    FUNC["Orquestador<br/>Azure Functions"]
    COLA["Storage Queue<br/>cola de envíos"]
    BLOB["Blob Storage<br/>copias inmutables"]
    JOBS["Container Apps Jobs<br/>Recolector · Validador · Puntaje"]
    SES["Container Apps<br/>sesiones dinámicas (sandbox)"]
    PG["PostgreSQL Flexible<br/>envíos y eventos"]
    KV["Key Vault"]
    AI["Azure AI Foundry<br/>Claude"]
    MON["Application Insights<br/>Azure Monitor"]
  end
  EQ --> PORTAL
  PORTAL --> ENTRA
  EQ -->|"pull request"| REPO
  REPO --> GHA
  GHA -->|"webhook"| FUNC
  FUNC --> COLA
  COLA --> JOBS
  JOBS --> BLOB
  JOBS --> AI
  JOBS --> SES
  JOBS --> PG
  FUNC --> PG
  FUNC -->|"check runs"| REPO
  PORTAL --> PG
  FUNC --> KV
  JOBS --> KV
  JOBS --> MON
  FUNC --> MON
```
