# Заполняет wheelhouse_linux колёсами под образ python:3.12-slim (manylinux, cp312, amd64).
# Нужен доступ в интернет. После изменения версий в wheelhouse_requirements.txt и backend/*/requirements.txt
# запустите этот скрипт и закоммитьте обновлённый каталог wheelhouse_linux/.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$dest = Join-Path $root "wheelhouse_linux"
New-Item -ItemType Directory -Force $dest | Out-Null
Get-ChildItem -Path $dest -Filter "*.whl" -File -ErrorAction SilentlyContinue | Remove-Item -Force

$platform = "manylinux_2_17_x86_64"
$pythonVersion = "3.12"
$implementation = "cp"
$abi = "cp312"

$req = Join-Path $root "wheelhouse_requirements.txt"
if (-not (Test-Path $req)) {
  throw "Missing $req"
}

python -m pip download `
  --dest $dest `
  --platform $platform `
  --python-version $pythonVersion `
  --implementation $implementation `
  --abi $abi `
  --only-binary=:all: `
  -r $req

Write-Host "OK: wheels saved to $dest"
