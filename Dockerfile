FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système minimales + git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port de FastAPI
EXPOSE 8000

# Démarrer l'application via le module Python
CMD ["python", "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
