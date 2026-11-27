# Requisitos de Azure

Suscripción actual: **Suscripción 1** (EnterpriseAgreement), rol **Contributor** en la suscripción.

## Lo que se puede hacer con el rol actual

- Crear el grupo de recursos y casi todos los servicios: App Service, Functions, Storage, Container Apps y Jobs, PostgreSQL, Key Vault, Application Insights y el despliegue de Claude en Foundry.
- Usar claves y cadenas de conexión guardadas en Key Vault en lugar de identidades administradas con roles.

## Lo que hay que pedir al administrador

| Solicitud | Para qué |
| --- | --- |
| Rol *Role Based Access Control Administrator* en `rg-epimodeling-plataforma` | Asignar roles a las identidades administradas (Blob, Key Vault, cola) sin usar claves |
| Permiso para crear un tenant de Entra External ID, o *Application Developer* + *Guest Inviter* | Registro de participantes y registro de la aplicación |
| Revisión de Azure Policy | Confirmar que no bloquean sesiones dinámicas, contenedores propios ni regiones |
| Registro DNS (por ejemplo `hub.ins.gov.co`) | Dominio propio del portal |
| Microsoft Defender for Storage con escaneo de malware | Revisar los archivos que suben los equipos |
| Aval de datos y Habeas Data | Tratamiento de datos de participantes y uso de SIVIGILA |

## Lo que se prueba ya con GitHub personal

El archivo `epihub-plataforma-prueba.zip` prueba la parte de GitHub del flujo, sin Azure:

1. El repositorio.
2. La Action de validación.
3. El pull request.
4. El webhook opcional.
