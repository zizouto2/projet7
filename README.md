# fin-llm-api

Assistant IA spécialisé dans la finance, les investissements et la bourse.
Basé sur FastAPI, Transformers et une interface web simple. Il est capable de :

✅ Répondre uniquement à des questions liées à la finance.  
✅ Détecter automatiquement les noms des 100 actifs les plus connus (Apple, Tesla, etc.).  
✅ Fournir les 3 dernières actualités financières liées, uniquement depuis :
   - https://www.bloomberg.com
   - https://www.investing.com

---

## 🔧 Installation

1. Créer un environnement virtuel (recommandé) :
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```

3. Configurer le fichier `.env` :
   ```
   MODEL_NAME=google/gemma-3-1b-it
   SERPAPI_KEY=votre_clé_serpapi
   HUGGINGFACE_HUB_TOKEN=optionnel_si_nécessaire
   ```

---

## 🚀 Lancement du projet

Utilisez le fichier `start.bat` :
```
start.bat
```

L'API sera disponible sur :
http://127.0.0.1:8000

L'interface web est accessible à la racine (`/`).

---

## 📁 Structure

- `app/` → code Python (FastAPI, modèle, logique métier)
- `static/index.html` → Interface utilisateur
- `.env` → Configuration privée
- `app.log` → Fichier de logs généré automatiquement
- `start.bat` → Script de lancement

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

Développé pour une exécution rapide, ciblée, et avec une précision spécialisée sur les domaines financiers.
