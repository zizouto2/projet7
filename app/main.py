from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import logging

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

SYSTEM_PROMPT = (
    "Tu es un expert financier spécialisé dans l’économie, la comptabilité, la bourse et l’investissement. "
    "Tu ne dois répondre qu’à des questions exclusivement financières. Pour toute question qui ne relève pas de la finance, "
    "réponds immédiatement : 'Je suis désolé, je ne peux répondre qu’à des questions financières.' "
    "Si un nom d'entreprise cotée ou un actif financier connu est mentionné (comme Apple, Tesla, etc.), considère qu'on parle de finance."
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
        search_context = "".join(
            f"Titre: {item['title']}\nExtrait: {item['snippet']}\nURL: {item['link']}\n\n"
            for item in news_items
        )

    prompt = tokenizer.apply_chat_template(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question if not search_context else f"{search_context}\n{question}"}
        ],
        tokenize=False,
        add_generation_prompt=True
    )

    try:
        outputs = generator(
            prompt,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        full_output = outputs[0]["generated_text"]
        response = full_output.replace(prompt, "").strip()
    except Exception as e:
        logging.error(f"Erreur lors de la génération : {e}")
        response = "Une erreur est survenue lors de la génération de la réponse."

    return {"response": response, "news": news_items}

@app.get("/")
async def index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
