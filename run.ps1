$outputDir = "output"
if (-not (Test-Path $outputDir -PathType Container)) {
    New-Item $outputDir -ItemType Directory
}
$logDir = "log"
if (-not (Test-Path $logDir -PathType Container)) {
    New-Item $logDir -ItemType Directory
}
$configDir = "config"
if (-not (Test-Path $configDir -PathType Container)) {
    New-Item $configDir -ItemType Directory
}
$venvDir = ".venv"
if (-not (Test-Path $venvDir -PathType Container)) {
    python -m venv $venvDir
    Write-Host "Created python virtual environment at $venvDir."
}
& "$venvDir/Scripts/Activate.ps1"
Write-Host "Using python in $venvDir."

Write-Host "Installing dependencies using pip..."
pip install -r requirements.txt
Write-Host "Finished installing."

Write-Host "Running main.py..."
Write-Host "-------------------------------"
try {
    python src/main.py
} finally {
    Write-Host "-------------------------------"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Abort!"
    }
    Write-Host "Deactivating..."
    deactivate
    Write-Host "Quit."
}
