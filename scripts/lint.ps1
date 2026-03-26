$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"

$services = Get-ChildItem -Path $backend -Directory -Filter "*_service" | Sort-Object Name

Write-Host "Running pylint per service (isolated sys.path)..."
foreach ($svc in $services) {
  Write-Host ""
  Write-Host "== pylint $($svc.Name) ==" -ForegroundColor Cyan
  $env:PYTHONPATH = $svc.FullName
  python -m pylint $svc.FullName --rcfile (Join-Path $root ".pylintrc") --score y
}

Write-Host ""
Write-Host "Running prospector per service..."
foreach ($svc in $services) {
  Write-Host ""
  Write-Host "== prospector $($svc.Name) ==" -ForegroundColor Cyan
  $env:PYTHONPATH = $svc.FullName
  prospector $svc.FullName -o text --profile-path $root
}


