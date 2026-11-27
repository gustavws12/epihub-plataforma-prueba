# Prueba la conexión de este computador con GitHub. Uso (PowerShell, en la carpeta del repo):
#   powershell -ExecutionPolicy Bypass -File scripts\probar_conexion.ps1 -Usuario <tu_usuario_github>
param([string]$Usuario = "")
function Ok($m){ Write-Host "  [OK] $m" -ForegroundColor Green }
function Mal($m){ Write-Host "  [X]  $m" -ForegroundColor Red }

Write-Host "1. Git instalado"
if (Get-Command git -ErrorAction SilentlyContinue) { Ok (git --version) } else { Mal "Instale Git: https://git-scm.com/download/win"; exit 1 }

Write-Host "2. Identidad de git"
$n = git config --global user.name; $e = git config --global user.email
if ($n -and $e) { Ok "$n <$e>" } else { Mal "Configure: git config --global user.name 'Su Nombre'; git config --global user.email 'correo'" }

Write-Host "3. GitHub CLI (opcional, recomendado)"
if (Get-Command gh -ErrorAction SilentlyContinue) {
  gh auth status 2>&1 | ForEach-Object { "     $_" }
  if ($LASTEXITCODE -eq 0) { Ok "gh autenticado" } else { Mal "Ejecute: gh auth login" }
} else { Write-Host "     gh no está instalado (winget install GitHub.cli). Se puede seguir solo con git." }

Write-Host "4. Acceso HTTPS a github.com"
try { $r = Invoke-WebRequest -Uri "https://api.github.com" -UseBasicParsing -TimeoutSec 15; Ok "api.github.com responde ($($r.StatusCode))" } catch { Mal "Sin acceso a api.github.com: revise proxy o firewall" }

if ($Usuario) {
  Write-Host "5. Usuario $Usuario en GitHub"
  try { $u = Invoke-RestMethod "https://api.github.com/users/$Usuario" -TimeoutSec 15; Ok "$($u.login) ($($u.public_repos) repos públicos)" } catch { Mal "No se encontró el usuario $Usuario" }
}

Write-Host "6. Remoto del repositorio"
$remoto = git remote get-url origin 2>$null
if ($remoto) {
  git ls-remote --heads origin 2>&1 | Select-Object -First 3 | ForEach-Object { "     $_" }
  if ($LASTEXITCODE -eq 0) { Ok "Lectura de $remoto" } else { Mal "No se pudo leer $remoto (credenciales)" }
} else { Write-Host "     Aún no hay remoto 'origin'. Use 2_subir_hub_a_github.cmd" }
