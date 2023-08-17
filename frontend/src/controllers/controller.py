import os
import random
from uuid import UUID

import httpx
from dotenv import load_dotenv
from fastapi import Depends, Request, Response
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from ..config import root_path
from .route import router
from .sessions import cookie

load_dotenv()

templates = Jinja2Templates(directory=f"{root_path}/templates")


client = MongoClient("localhost", 27017)
database = client["customer-care-db"]
message_collection = database["messages"]


@router.post("/initial-message")
async def receive_inital_chat_message(request: Request, response: Response):
    """Receive the initial chat message and create a customer care session.

    Args:
        request (Request): The incoming request object.
        response (Response): The outgoing response object.

    Returns:
        dict: A dictionary containing the initial response message, customer name, and session ID.

    Raises:
        httpx.HTTPError: If an error occurs while communicating with external services.

    Note:
        This endpoint handles the initial chat message from the customer. It creates a
        customer care session by calling an external service to generate a session ID.
        The session ID is attached to the response as a cookie.

        The customer's name is extracted from the request JSON and used to initiate
        the session creation process.

        If successful, the endpoint returns an initial response message and relevant session details.

        In case of any error during session creation, an error message is returned.

    Examples:
        Example usage of the endpoint:
        >>> payload = {"message": "John Doe"}
        >>> response = await httpx.post("http://127.0.0.1:8000/initial-message", json=payload)
        >>> print(response.json())
        {
            "answer": "Please provide a brief overview of how I can assist you today.",
            "Name": "John Doe",
            "Session": "a5e8d3c4-7d88-4356-88f9-ff8c8d3bfb45"
        }
    """
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

            id = random.randint(1, 500)

            cookie.attach_to_response(response, session_id)

            return {
                "answer": "Por favor, informe em poucas palavras como posso ser útil para você hoje.",
                "Name": name,
                "Session": id,
            }

        except httpx.HTTPError as e:
            return {"status": "Error", "message": str(e)}, response.status_code


@router.post("/chat")
async def receive_chat_message_chat(
    request: Request,
    # , session_id: UUID = Depends(cookie)
):
    """Receive chat messages and provide responses using the chat service.

    Args:
        request (Request): The incoming request object.
        session_id (UUID): The session ID retrieved from the cookie.

    Returns:
        dict: A dictionary containing the AI response message and conversation details.

    Raises:
        httpx.HTTPError: If an error occurs while communicating with external services.

    Note:
        This endpoint handles incoming chat messages from the customer during an active session.
        It communicates with an external chat service to generate an AI response based on the
        customer's message and maintains a conversation history.

        The conversation history includes user messages, AI responses, and conversation steps.

        If the communication with the chat service fails, an error message is returned.

    Examples:
        Example usage of the endpoint:
        >>> payload = {"message": "How can I track my order?"}
        >>> response = await httpx.post("http://127.0.0.1:8000/chat", json=payload, headers={"session_id": "a5e8d3c4-7d88-4356-88f9-ff8c8d3bfb45"})
        >>> print(response.json())
        {
            "answer": "Your order is currently being processed and will be shipped within 2 business days.",
            "steps": ["Step 1", "Step 2"],
            "is_final_step": "False"
        }
    """
    data = await request.json()
    print("entrou aqui")

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    if user_message := data.get("message", "").strip():
        payload = {"user_id": str(data.get("session_id", "")), "message": user_message}

        if os.getenv("ENV") == "dev":
            url = "http://localhost:8000/api/v1/chat"
        else:
            url = "http://localhost:8000/api/v1/chat"

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
    request: Request,
    # , session_id: UUID = Depends(cookie)
):
    """Receive chat messages and generate AI responses.

    Args:
        request (Request): The incoming request object.
        session_id (UUID): The session ID retrieved from the cookie.

    Returns:
        dict: A dictionary containing the AI response message.

    Raises:
        httpx.HTTPError: If an error occurs while communicating with external services.

    Note:
        This endpoint handles incoming chat messages from the customer and generates an AI
        response using an external AI chatbot service.

        The AI response is based on the customer's message and may include suggestions
        for further actions.

        If the communication with the AI chatbot service fails, an error message is returned.

    Examples:
        Example usage of the endpoint:
        >>> payload = {"message": "Tell me a joke!"}
        >>> response = await httpx.post("http://127.0.0.1:8000/chat_ai", json=payload, headers={"session_id": "a5e8d3c4-7d88-4356-88f9-ff8c8d3bfb45"})
        >>> print(response.json())
        {
            "answer": "Sure, here's a joke for you: Why don't scientists trust atoms? Because they make up everything!"
        }
    """
    data = await request.json()

    if not data:
        return {"status": "Error", "message": "Empty request body"}

    if user_message := data.get("message", "").strip():
        # payload = {"user_id": str(session_id.hex), "message": user_message}
        payload = {"user_id": str(data.get("session_id", "")), "message": user_message}

        if os.getenv("ENV") == "dev":
            url = "http://localhost:8000/api/v1/chat_ai"
        else:
            url = "http://localhost:8000/api/v1/chat_ai"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=60)

                response = response.json()

                return {"answer": response}

            except httpx.HTTPError as e:
                return {"status": "Error", "message": str(e)}


@router.get("/")
async def read_index(request: Request):
    """Retrieve the index page of the customer care system.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: The rendered index HTML page.

    Note:
        This endpoint serves as the index page of the customer care system. It renders an HTML
        template for user interaction.

    Examples:
        Example usage of the endpoint:
        >>> response = await httpx.get("http://127.0.0.1:8000/")
        >>> print(response.content)
        (Rendered HTML content)
    """
    return templates.TemplateResponse("index.html", {"request": request})
