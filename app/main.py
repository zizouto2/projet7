from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging
from collections import deque

from app.config import settings
from app.model_loader import generator, tokenizer
from app.utils import (
    is_off_topic,
    is_current_event_question,
    perform_targeted_search,
    detect_stock_names
)

app = FastAPI()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Historique limité aux 3 dernières interactions
chat_history = deque(maxlen=3)

SYSTEM_PROMPT = (
    "Tu es un expert en finance, spécialisé dans l’économie, la comptabilité, la bourse et l’investissement.\n\n"
    "Tu ne dois répondre qu’à des questions **financières**. Si une question ne concerne pas la finance, "
    "tu dois répondre : **'Je suis désolé, je ne peux répondre qu’à des questions financières.'**\n\n"
    "✅ Si une question mentionne le nom d’une entreprise cotée en bourse ou d’un actif financier connu (exemples : Apple, Tesla, Amazon, Bitcoin, CAC 40, Nasdaq…), "
    "considère automatiquement qu’il s’agit d’une **question liée à la finance**, même si la formulation est vague.\n\n"
    "❗ Ne rejette jamais une question qui contient le nom d’un actif financier ou d’une entreprise cotée.\n"
    "Tu dois alors fournir une réponse dans le contexte financier, comme : investissement, analyse, performance, risques, etc.\n\n"
    "📝 Réponds toujours en un maximum de 500 mots."
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")

    names = detect_stock_names(question)
    if is_off_topic(question) and not names:
        return {"response": "Je suis désolé, je ne peux répondre qu’à des questions financières.", "news": []}

    news_items = []
    search_context = ""

    if is_current_event_question(question):
        news_items = perform_targeted_search(question)
    elif names:
        query = " ".join(names)
        news_items = perform_targeted_search(query)

    if news_items:
        search_context = "Actualités liées :\n\n" + "\n".join(
            f"- {item['title']}\n  {item['link']}" for item in news_items
        ) + "\n\n"

    # Ajout de l'historique dans le prompt
    chat_history_text = "\n\n".join(
        f"Q: {entry['question']}\nR: {entry['answer']}" for entry in chat_history
    )
    context_block = f"{search_context}{chat_history_text}".strip()

    prompt = tokenizer.apply_chat_template(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question if not context_block else f"{context_block}\n{question}"}
        ],
        tokenize=False,
        add_generation_prompt=True
    )

    try:
        outputs = generator(
            prompt,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        full_output = outputs[0]["generated_text"]
        response = full_output.replace(prompt, "").strip()
    except Exception as e:
        logging.error(f"Erreur lors de la génération : {e}")
        response = "Une erreur est survenue lors de la génération de la réponse."

    # Mise à jour de l'historique
    chat_history.append({"question": question, "answer": response})

    # Création d’un résumé de l’historique (max 500 mots)
    history_summary = "\n\n".join(
        f"Q: {entry['question']}\nR: {entry['answer']}" for entry in list(chat_history)
    )
    total_words = len(history_summary.split())
    summary_text = history_summary if total_words <= 500 else " ".join(history_summary.split()[:500]) + "..."

    return {
        "response": response,
        "news": news_items,
        "history_summary": summary_text,
        "word_count": len(summary_text.split())
    }

@app.post("/clear-history")
async def clear_history():
    chat_history.clear()
    return {"message": "Historique effacé."}

@app.get("/")
async def index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
