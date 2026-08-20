param(
  [ValidateSet("all", "frontend", "backend", "ingestion")]
  [string]$Module = "all"
)

$ErrorActionPreference = "Continue"
$root = $PSScriptRoot
$failures = @()

function Invoke-Step {
  param(
    [string]$Name,
    [string]$Dir,
    [string]$Cmd
  )
  Write-Host "==> $Name" -ForegroundColor Cyan
  Push-Location (Join-Path $root $Dir)
  try {
    $global:LASTEXITCODE = 0
    try {
      Invoke-Expression $Cmd 2>&1 | ForEach-Object { Write-Host $_ }
    } catch {
      Write-Host "    $($_.Exception.Message)" -ForegroundColor Yellow
      $global:LASTEXITCODE = 1
    }
    if ($LASTEXITCODE -ne 0) {
      Write-Host "    FAIL: $Name (exit $LASTEXITCODE)" -ForegroundColor Red
      $script:failures += $Name
    } else {
      Write-Host "    OK: $Name" -ForegroundColor Green
    }
  } finally {
    Pop-Location
  }
}

switch ($Module) {
  "frontend" {
    Invoke-Step "frontend: lint" "frontend" "npm run lint"
    Invoke-Step "frontend: build" "frontend" "npm run build"
  }
  "backend" {
    Invoke-Step "backend: test" "backend" ".\mvnw.cmd test"
  }
  "ingestion" {
    Invoke-Step "ingestion: build" "ingestion" "go build ./..."
    Invoke-Step "ingestion: test" "ingestion" "go test ./..."
  }
  default {
    Invoke-Step "frontend: lint" "frontend" "npm run lint"
    Invoke-Step "frontend: build" "frontend" "npm run build"
    Invoke-Step "backend: test" "backend" ".\mvnw.cmd test"
    Invoke-Step "ingestion: build" "ingestion" "go build ./..."
    Invoke-Step "ingestion: test" "ingestion" "go test ./..."
  }
}

Write-Host ""
if ($failures.Count -gt 0) {
  Write-Host "HARNESS FALHOU - etapas com erro:" -ForegroundColor Red
  $failures | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}

Write-Host "HARNESS OK - todos os modulos validados" -ForegroundColor Green
exit 0