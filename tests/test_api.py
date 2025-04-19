import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_finance_question():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "Je veux acheter Apple"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)

@pytest.mark.asyncio
async def test_off_topic_question():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "Donne-moi une recette de couscous"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"].startswith("Je suis désolé")

@pytest.mark.asyncio
async def test_actuality_detection():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask", json={"question": "Quelles sont les dernières nouvelles sur Tesla ?"})
        assert response.status_code == 200
        data = response.json()
        assert "news" in data
        assert isinstance(data["news"], list)