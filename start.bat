@echo off
echo ========================================
echo Lancement de l'assistant financier IA...
echo ========================================

:: Activer l'environnement virtuel s'il existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Environnement virtuel activé.
)

:: Charger les variables d'environnement depuis le fichier .env (si tu utilises Python dotenv)
setlocal EnableDelayedExpansion
for /f "usebackq delims=" %%a in (".env") do (
    set "line=%%a"
    if not "!line!"=="" (
        echo !line! | findstr /b /r "[A-Z_][A-Z_0-9]*=" >nul
        if !errorlevel! == 0 (
            for /f "tokens=1,* delims==" %%i in ("!line!") do set "%%i=%%j"
        )
    )
)

:: Lancer le serveur FastAPI avec Uvicorn
echo 🚀 Lancement de l'API...
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
