$projectPath = "C:\Users\Jose L\Desktop\Scrapy-Selenium-01"
$venvPath = Join-Path $projectPath "venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"
$scriptPath = Join-Path $projectPath "src\launcher.py"

# Activar el entorno virtual
& $pythonPath -m venv $venvPath | Out-Null
$activatePath = Join-Path $venvPath "Scripts\Activate.ps1"
. $activatePath

# Ejecutar el script launcher.py
& $pythonPath $scriptPath