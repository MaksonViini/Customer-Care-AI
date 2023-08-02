from uuid import UUID

import httpx
from fastapi import Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from ..config import root_path
from .route import router
from .sessions import cookie

templates = Jinja2Templates(directory=f"{root_path}/templates")


client = MongoClient("localhost", 27017)
database = client["customer-care-db"]
message_collection = database["messages"]


@router.post("/initial-message")
async def receive_chat_message(request: Request, response: Response):
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    name = data.get("message", "").strip()

    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:8080/create_session/{name}"

        try:
            response_create_session = await client.post(url, timeout=60)

            session_id_str = response_create_session.json()["session_id"]

            session_id = UUID(session_id_str)

            print(name)
            print(session_id)

            cookie.attach_to_response(response, session_id)

            return {
                "answer": "Por favor, informe em poucas palavras como posso ser útil para você hoje.",
                "Name": name,
                "Session": session_id,
            }

        except httpx.HTTPError as e:
            return {"status": "Error", "message": str(e)}, response.status_code


@router.post("/chat")
async def receive_chat_message_chat(
    request: Request, session_id: UUID = Depends(cookie)
):
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    if user_message := data.get("message", "").strip():
        payload = {"user_id": str(session_id.hex), "message": user_message}

        url = "http://127.0.0.1:8000/api/v1/chat"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=60)

                response = response.json()

                if response["message"] != True:
                    return {
                        "answer": response["message"].get("bot_response"),
                        "steps": response["steps"],
                        "is_final_step": str(response["is_final_step"]),
                    }

            except httpx.HTTPError as e:
                return {"status": "Error", "message": str(e)}


@router.post("/chat_ai")
async def receive_chat_message_chat_ai(
    request: Request, session_id: UUID = Depends(cookie)
):
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    if user_message := data.get("message", "").strip():
        payload = {"user_id": str(session_id.hex), "message": user_message}

        url = "http://127.0.0.1:8000/api/v1/chat_ai"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=60)

                response = response.json()

                return {"answer": response}

            except httpx.HTTPError as e:
                return {"status": "Error", "message": str(e)}, response.status_code


@router.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
