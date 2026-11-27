# Decisiones de arquitectura (ADR)

| # | Decisión | Por qué | Alternativa descartada |
| --- | --- | --- | --- |
| ADR-01 | Envíos por pull request en GitHub (GitOps) | Es el estándar hubverse; deja historial, revisión y validación automática sin construir un cargador propio | Carga de archivos desde el portal |
| ADR-02 | Validación doble: GitHub Actions y Validador oficial en Azure | Actions avisa en segundos; la oficial corre en un entorno controlado y es la que cuenta | Solo Actions |
| ADR-03 | El agente IA propone un plan y no ejecuta | Evita que un prompt malicioso dentro del código de un equipo se convierta en una acción | Agente con herramientas de ejecución |
| ADR-04 | ValidadorPlan con lista de permitidos | Corta cualquier plan que pida paquetes o comandos fuera de lo acordado | Revisión manual de cada plan |
| ADR-05 | Sandbox en sesiones dinámicas de Container Apps sin internet | Aislamiento por sesión, cobro por uso y sin exfiltración de datos | Máquinas virtuales por equipo |
| ADR-06 | Copia inmutable en Blob con SHA-256 | Prueba de qué se entregó y cuándo, ante reclamos | Confiar en el historial de git |
| ADR-07 | Reproducibilidad con tolerancia del 1 % | Los modelos con semilla o MCMC no dan cifras idénticas | Igualdad exacta |
| ADR-08 | Puntaje con R hubEvals | Es la implementación de referencia de WIS en hubverse | Métricas propias en Python |
| ADR-09 | Entra External ID para participantes | Registro propio sin crear cuentas en el directorio del INS | Invitados B2B en el tenant del INS |
| ADR-10 | Repositorios de equipos privados; microdatos nunca en GitHub | Acuerdo de confidencialidad y Habeas Data | Repositorios públicos |
