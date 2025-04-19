# fin-llm-api

Assistant IA spécialisé dans la finance, les investissements et la bourse.
Basé sur FastAPI, Transformers et une interface web simple. Il est capable de :

✅ Répondre uniquement à des questions liées à la finance.  
✅ Détecter automatiquement les noms les actifs (Apple, Tesla, etc.).  
✅ Fournir les 3 dernières actualités financières

---

## 🔧 Installation

1. Créer un environnement virtuel (recommandé) avec `venv` :
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Ou avec `conda` :
   ```bash
   conda create --name fin-llm-api python=3.9
   conda activate fin-llm-api
   ```

2. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```
   3. Configurer le fichier `.env` :
      ```bash
      Renommer le fichier `env-exemple` en `.env` puis ajouter vos clés d'API

      MODEL_NAME=google/gemma-3-1b-it
      SERPAPI_KEY=votre_clé_serpapi
      HUGGINGFACE_HUB_TOKEN=optionnel_si_nécessaire
      ```

      - **SERPAPI_KEY** : Obtenez votre clé API sur [SerpAPI](https://serpapi.com/).
      - **HUGGINGFACE_HUB_TOKEN** : Si nécessaire, générez un token sur [Hugging Face](https://huggingface.co/settings/tokens).

---

## 🚀 Lancement du projet

L'API LLM sera disponible sur :
http://127.0.0.1:8000

L'interface web est accessible à la racine (`/`).

---

## 📁 Structure

- `app/` → code Python (FastAPI, modèle, logique métier)
- `static/index.html` → Interface utilisateur
- `.env` → Configuration privée
- `app.log` → Fichier de logs généré automatiquement

---

## 🧠 Modèles supportés

Par défaut : `google/gemma-3-1b-it`  
Optionnel : support de `mistralai/Mistral-7B` (version quantifiée 4-bit via AutoGPTQ)

---

## ✉️ Exemples de requêtes

- ✅ "Je veux acheter Apple"
- ✅ "Que penses-tu de Tesla en ce moment ?"
- ❌ "Donne-moi une recette de lasagnes" → rejetée (hors finance)

---
