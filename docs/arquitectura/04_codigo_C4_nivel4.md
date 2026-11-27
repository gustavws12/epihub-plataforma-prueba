# Nivel 4 — Código del Agente revisor IA

![Nivel 4 — Código del Agente revisor IA](diagramas/c4_nivel4_codigo.svg)

El agente no ejecuta nada: devuelve un `PlanEjecucion`. Solo el `ControladorSandbox` corre comandos, y solo los de un plan que el `ValidadorPlan` aprobó.

Ejemplo de plan que devuelve Claude:

```json
{
  "lenguaje": "R",
  "paquetes": ["data.table", "INLA", "hubValidations"],
  "comandos": ["Rscript scripts/ajustar_modelo.R --corte 2026-11-14"],
  "salidas_esperadas": ["model-output/equipo-modelo/2026-11-14-equipo-modelo.csv"],
  "justificacion": "El script lee la serie y las covariables, ajusta un modelo INLA y escribe los 23 cuantiles."
}
```

## Fuente Mermaid

```mermaid
classDiagram
  class Envio {
    +str id_envio
    +str equipo
    +str modelo
    +date reference_date
    +str sha256
    +EstadoEnvio estado
    +avanzar(nuevo: EstadoEnvio)
  }
  class EstadoEnvio {
    <<enumeration>>
    RECIBIDO
    VALIDADO
    REVISADO
    EJECUTADO
    REPRODUCIBLE
    NO_REPRODUCIBLE
    PUNTUADO
    FALLIDO
  }
  class Inventario {
    +listar(ruta) List~Archivo~
    +clasificar(archivo) TipoArchivo
  }
  class FiltroSeguridad {
    +reglas: List~str~
    +revisar(archivos) List~Hallazgo~
    +bloquea(hallazgos) bool
  }
  class GestorPrompts {
    +plantilla: str
    +armar(inventario, hallazgos, anexoA) str
  }
  class ClienteFoundry {
    +despliegue: str
    +max_tokens: int
    +proponer_plan(prompt) PlanEjecucion
  }
  class PlanEjecucion {
    +lenguaje: str
    +paquetes: List~str~
    +comandos: List~str~
    +salidas_esperadas: List~str~
    +justificacion: str
  }
  class ValidadorPlan {
    +paquetes_permitidos: Set~str~
    +comandos_permitidos: Set~str~
    +validar(plan) Resultado
  }
  class AgenteRevisor {
    +revisar(envio) PlanEjecucion
  }
  class ControladorSandbox {
    +crear_sesion(imagen) Sesion
    +ejecutar(plan, sesion) SalidaEjecucion
    +cerrar(sesion)
  }
  class VerificadorReproducibilidad {
    +tolerancia: float = 0.01
    +comparar(entregado, regenerado) bool
  }
  AgenteRevisor --> Inventario
  AgenteRevisor --> FiltroSeguridad
  AgenteRevisor --> GestorPrompts
  AgenteRevisor --> ClienteFoundry
  ClienteFoundry --> PlanEjecucion
  ValidadorPlan --> PlanEjecucion
  ControladorSandbox --> PlanEjecucion
  Envio --> EstadoEnvio
  VerificadorReproducibilidad --> Envio
```
