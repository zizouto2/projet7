@echo off
echo ========================================
echo  Lancement de l'assistant financier IA
echo ========================================

:: Activer l'environnement virtuel si présent
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Environnement virtuel activé.
) else (
    echo ⚠️ Aucun environnement virtuel trouvé. Assurez-vous d'en avoir un si besoin.
)

:: Lancer le serveur Uvicorn
echo 🚀 Lancement du serveur FastAPI avec uvicorn...
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause