import json

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
database = client["customer-care-db"]
message_collection = database["messages"]

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

# Configurar a pasta onde estão os templates Jinja2
templates = Jinja2Templates(directory="frontend/src/templates")


chat_messages = []  # Lista para armazenar as mensagens do chat


# Rota para receber mensagens de chat (POST)
@router.post("/")
async def receive_chat_message(request: Request):
    data = await request.body()

    print(json.loads(data))

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        return {"status": "Error", "message": f"Invalid JSON format: {str(e)}"}

    if user_message := json_data.get("message", "").strip():
        payload = {"user_id": 1, "message": user_message}

        # Estou com alguns problemas com meu seguro.

        url = "http://127.0.0.1:8000/api/v1/chat"

        return 200

        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post(url, json=payload, timeout=10)
        #         response.raise_for_status()
        #         data = response.json()

        #         return {"status": "OK", "message": "Ok!"}, 200
        #     except httpx.HTTPError as e:
        #         return {"status": "Error", "message": str(e)}, response.status_code

    return {"status": "Message received successfully", "messages": chat_messages}


# Rota para exibir a página inicial do chat (GET)
@router.get("/")
async def read_index(request: Request):
    # messages = message_collection.find({})
    # chat_messages = [
    #     [
    #         {
    #             "step": 1,
    #             "user_message": "Estou com alguns problemas com meu seguro. o",
    #             "bot_response": "Olá! Bem-vindo ao nosso suporte. Como posso ajudar você hoje?",
    #         },
    #         {
    #             "step": 2,
    #             "user_message": "e agora?",
    #             "bot_response": "Entendo que você está buscando ajuda para automatizar um processo de atendimento ao cliente no front office. Podemos orientar você nessa questão.",
    #         },
    #         {
    #             "step": 3,
    #             "user_message": "testando",
    #             "bot_response": "Você poderia fornecer mais detalhes sobre o processo que deseja automatizar? Quais são as etapas envolvidas e quais são os principais desafios que você está enfrentando em relação à eficiência?",
    #         },
    #     ]
    # ]

    chat_messages = []
    # chat_messages = [message["message"] for message in messages]
    return templates.TemplateResponse(
        "index.html", {"request": request, "chat_messages": chat_messages}
    )
