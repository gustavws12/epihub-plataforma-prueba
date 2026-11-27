# Arquitectura — Plataforma de participantes del EpiModelling Hub (INS)

Versión preliminar · 26 de noviembre de 2026 · Gustavo A Romero

La plataforma recibe los pronósticos, covariables y scripts de R y Python de los equipos y los procesa en cinco pasos:

1. Los valida con las reglas del hub (formato hubverse).
2. Un agente de IA revisa el código y propone un plan de ejecución.
3. El plan corre en un entorno aislado.
4. Se verifica que el resultado sea reproducible.
5. Se califica con WIS.

El modelo de trabajo es **GitOps**: cada envío es un *pull request* en GitHub.

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `01_contexto_C4_nivel1.md` | Actores y sistemas externos (C4 nivel 1) |
| `02_contenedores_C4_nivel2.md` | Servicios de Azure y GitHub que componen la plataforma (C4 nivel 2) |
| `03_componentes_C4_nivel3.md` | Componentes del Pipeline de Evaluación (C4 nivel 3) |
| `04_codigo_C4_nivel4.md` | Clases del Agente revisor IA y del ValidadorPlan (C4 nivel 4) |
| `05_estados_envio.md` | Ciclo de vida de un envío |
| `06_secuencia_envio.md` | Secuencia completa de un pull request |
| `07_decisiones_ADR.md` | Decisiones de arquitectura y sus razones |
| `08_requisitos_azure.md` | Qué se puede hacer con la suscripción actual y qué pedir al administrador |
| `diagramas/` | Fuentes Mermaid (`.mmd`) y su render en SVG |

## Principios

1. **El agente propone, no ejecuta.** El Agente revisor IA lee el código y devuelve un plan. El plan solo corre si pasa la lista de permitidos del ValidadorPlan.
2. **Sandbox sin internet.** El código de los equipos corre en sesiones dinámicas de Container Apps con un contenedor R + Python propio, sin salida a internet y con paquetes permitidos.
3. **Todo envío es inmutable.** El Recolector copia cada archivo a Blob con huella SHA-256 y retención inmutable.
4. **Datos del SIVIGILA fuera de GitHub.** Los repositorios de los equipos son privados y nunca llevan microdatos.
5. **Trazabilidad.** Cada cambio de estado queda en PostgreSQL (`ejecucion_eventos`) y en Application Insights.
