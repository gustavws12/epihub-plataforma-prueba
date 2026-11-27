# Estados de un envío

![Estados de un envío](diagramas/estados_envio.svg)

Cada transición queda en `ejecucion_eventos` con la hora, el componente y el detalle. NO_REPRODUCIBLE se califica igual, pero queda marcado en el tablero.

## Fuente Mermaid

```mermaid
stateDiagram-v2
  [*] --> RECIBIDO: webhook del PR
  RECIBIDO --> VALIDADO: pasa hubValidations y Anexo A
  RECIBIDO --> FALLIDO: formato inválido
  VALIDADO --> REVISADO: plan aprobado por ValidadorPlan
  VALIDADO --> FALLIDO: hallazgo de seguridad o plan rechazado
  REVISADO --> EJECUTADO: corre en el sandbox
  REVISADO --> FALLIDO: error o tiempo agotado
  EJECUTADO --> REPRODUCIBLE: diferencia ≤ 1 %
  EJECUTADO --> NO_REPRODUCIBLE: diferencia > 1 %
  REPRODUCIBLE --> PUNTUADO: llegan los datos observados
  NO_REPRODUCIBLE --> PUNTUADO: se califica con marca
  PUNTUADO --> [*]
  FALLIDO --> [*]
```
