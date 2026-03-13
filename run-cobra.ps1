$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $projectRoot ".venv"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$cobraExe = Join-Path $projectRoot ".venv\Scripts\cobra.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[INFO] Creating Python virtual environment in .venv..." -ForegroundColor Cyan

    $venvCreated = $false
    $venvCommands = @(
        @{ Command = "py"; Args = @("-3.12", "-m", "venv", $venvPath) },
        @{ Command = "py"; Args = @("-3", "-m", "venv", $venvPath) },
        @{ Command = "py"; Args = @("-m", "venv", $venvPath) },
        @{ Command = "python"; Args = @("-m", "venv", $venvPath) }
    )

    foreach ($candidate in $venvCommands) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) {
            continue
        }

        & $candidate.Command @($candidate.Args)
        if ($LASTEXITCODE -eq 0 -and (Test-Path $pythonExe)) {
            $venvCreated = $true
            break
        }
    }

    if (-not $venvCreated) {
        Write-Host "[ERROR] Failed to create .venv automatically." -ForegroundColor Red
        Write-Host "Install Python 3.12+ and make sure 'py' or 'python' is available in PATH." -ForegroundColor Yellow
        exit 1
    }
}

if (-not (Test-Path $cobraExe)) {
    Write-Host "[INFO] Installing local cobra command into .venv..." -ForegroundColor Cyan
    & $pythonExe -m pip install -e $projectRoot
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install cobra CLI." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

& $cobraExe @args
exit $LASTEXITCODE
