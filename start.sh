#!/bin/bash
echo "========================================"
echo "  Lancement de l'assistant financier IA"
echo "========================================"

# Activer l'environnement virtuel si présent
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
  echo "✅ Environnement virtuel activé."
else
  echo "⚠️ Aucun environnement virtuel trouvé. Assurez-vous d'en avoir un si besoin."
fi

# Lancer le serveur
echo "🚀 Lancement de FastAPI avec uvicorn..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload