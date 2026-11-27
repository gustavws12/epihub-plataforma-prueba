# epihub-plataforma-prueba — Hub

Este es el repositorio central (el **hub**) de la simulación de la plataforma de participantes del EpiModelling Hub. Lo sube la cuenta coordinadora (por omisión `gustavws12`). Los equipos le envían pull requests desde **sus propias cuentas de GitHub**.

> Todo es sintético. No suba microdatos del SIVIGILA; el `.gitignore` bloquea `datos/`, `*.xlsx` y `*CONFIDENCIAL*`.

## Pasos de la cuenta coordinadora

| Paso | Qué hacer | Resultado esperado |
| --- | --- | --- |
| 1 | Doble clic en `1_probar_conexion.cmd` | Todas las líneas en `[OK]`, salvo el remoto, que aún no existe |
| 2 | Doble clic en `3_validar_en_local.cmd` | `✓ ... válido` (requiere Python) |
| 3 | Doble clic en `2_subir_hub_a_github.cmd` | Se abre github.com/new; cree el repo **privado y vacío** y presione Enter; se sube y la Action "Prueba de conexión" queda en verde |
| 4 | En **Settings → Collaborators → Add people**, invite cada cuenta de equipo con permiso **Write** | Cada cuenta acepta la invitación desde su correo o desde github.com/notifications |

## Qué revisa cada pull request

`.github/workflows/validar-envio.yml` corre dos revisiones:

1. **Formato del Anexo A** (`scripts/validar_envio.py`), que revisa:
   - las 8 columnas;
   - los 38 códigos;
   - los horizontes 1 a 12;
   - los 23 cuantiles;
   - las fechas;
   - que los valores no sean negativos y crezcan con el cuantil;
   - que estén las 10.488 filas;
   - que exista el archivo de metadatos.
2. **Seguridad del código** (`scripts/revisar_codigo.py`): bloquea llamadas de red, `system()`/`subprocess`, `eval(parse())` y la lectura de secretos.

El bot comenta el resultado en el PR. Si el secreto `ORQUESTADOR_URL` existe, avisa además al orquestador por webhook; para probar sin Azure, sirve una URL de https://webhook.site.

## Estructura

| Ruta | Qué es |
| --- | --- |
| `hub-config/tasks.json` | Reglas de la ronda 1: referencia 2026-11-14, horizontes 1 a 12, 23 cuantiles |
| `hub-config/entidades.csv` | Las 38 entidades con su código DIVIPOLA |
| `model-output/`, `model-metadata/`, `codigo/` | Lo que envía cada equipo |
| `pruebas/` | Archivo con errores que usa la Action de conexión |
| `docs/arquitectura/` | Arquitectura C4 de la plataforma |
