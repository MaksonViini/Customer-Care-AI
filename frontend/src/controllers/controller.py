import json
from uuid import UUID

import httpx
from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from frontend.src.controllers.route import router

from ..schemas.session import SessionData
from .sessions import cookie

client = MongoClient("localhost", 27017)
database = client["customer-care-db"]
message_collection = database["messages"]


templates = Jinja2Templates(directory="frontend/src/templates")


@router.post("/initial-message")
async def receive_chat_message(request: Request):
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    name = data.get("message", "").strip()

    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:8080/create_session/{name}"
        try:
            response = await client.post(url, timeout=10)

            session_id = response.json()["uuid"]

            print(name)
            print(session_id)

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
        payload = {"user_id": session_id, "message": user_message}

        url = "http://127.0.0.1:8000/api/v1/chat"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=10)

                response = response.json()

                return {"answer": response["message"].get("bot_response")}

            except httpx.HTTPError as e:
                return {"status": "Error", "message": str(e)}, response.status_code


@router.post("/chat_ai", dependencies=[Depends(cookie)])
async def receive_chat_message_chat_ai(
    request: Request, session_id: UUID = Depends(cookie)
):
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    if user_message := data.get("message", "").strip():
        payload = {"user_id": session_id, "message": user_message}

        url = "http://127.0.0.1:8000/api/v1/chat_ai"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=10)

                response = response.json()

                return {"answer": response}

            except httpx.HTTPError as e:
                return {"status": "Error", "message": str(e)}, response.status_code


@router.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
