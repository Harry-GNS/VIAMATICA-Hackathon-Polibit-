Param(
    [switch]$ForceRest
)

Write-Host "> Creando/activando entorno virtual (venv)..."
if (!(Test-Path .\venv)) {
    python -m venv venv
}

Write-Host "> Activando venv..."
. .\venv\Scripts\Activate.ps1

Write-Host "> Actualizando pip e instalando dependencias..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install requests==2.31.0

if (!(Test-Path .env)) {
    Copy-Item .env.example .env -Force
    Write-Host ".env creado a partir de .env.example - edita .env y añade tu GROQ_API_KEY"
}

if ($ForceRest) {
    Write-Host "> Forzando uso REST de Groq (USE_GROQ_REST=1) para esta sesion"
    $env:USE_GROQ_REST = "1"
}

Write-Host "> Inicializando base de datos (init_database.py)..."
python init_database.py

Write-Host "> Iniciando la aplicación (main.py)..."
python main.py
