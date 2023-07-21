import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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

    return {"statis": data}
    # if not data:
    #     return {"status": "Error", "message": "Empty request body"}

    # try:
    #     json_data = json.loads(data)
    # except json.JSONDecodeError as e:
    #     return {"status": "Error", "message": f"Invalid JSON format: {str(e)}"}

    # if user_message := json_data.get("message", "").strip():
    #     chat_messages.append(user_message)

    # return {"status": "Message received successfully", "messages": chat_messages}


# Rota para exibir a página inicial do chat (GET)
@router.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "chat_messages": chat_messages}
    )
