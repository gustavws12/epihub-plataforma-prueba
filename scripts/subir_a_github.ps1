# Sube el repositorio del HUB a la cuenta de GitHub del coordinador (sin GitHub CLI).
param([string]$Usuario = "gustavws12", [string]$Repo = "epihub-plataforma-prueba")
$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Host "Instale Git: https://git-scm.com/download/win" -ForegroundColor Red; exit 1 }

if (-not (Test-Path .git)) {
  git init -b main | Out-Null
  git add .
  git -c user.name="$Usuario" -c user.email="$Usuario@users.noreply.github.com" commit -m "Hub de prueba de la plataforma de participantes" | Out-Null
  Write-Host "Repositorio local creado con el primer commit." -ForegroundColor Green
}

Write-Host "`n1) Se abrirá GitHub para crear el repositorio."
Write-Host "   Nombre: $Repo   |   Visibilidad: Private   |   NO marque README, .gitignore ni licencia."
Start-Process "https://github.com/new?name=$Repo&visibility=private"
Read-Host "`n   Presione Enter cuando el repositorio esté creado"

git remote remove origin 2>$null
git remote add origin "https://$Usuario@github.com/$Usuario/$Repo.git"
Write-Host "`n2) Subiendo. Si se abre una ventana de inicio de sesión, entre con la cuenta $Usuario."
git push -u origin main
if ($LASTEXITCODE -eq 0) {
  Write-Host "`nListo. Revise que la Action 'Prueba de conexión' quede en verde:" -ForegroundColor Green
  Write-Host "   https://github.com/$Usuario/$Repo/actions"
  Start-Process "https://github.com/$Usuario/$Repo/actions"
  Write-Host "`n3) Invite a las cuentas de los equipos como colaboradores (permiso Write):"
  Write-Host "   https://github.com/$Usuario/$Repo/settings/access"
} else { Write-Host "No se pudo subir. Revise el usuario y que el repo exista y esté vacío." -ForegroundColor Red }
