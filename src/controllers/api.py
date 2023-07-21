import datetime
from typing import List

import jwt
import pandas as pd
import requests
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from langchain.memory import MongoDBChatMessageHistory
from starlette.responses import RedirectResponse

from ..database import conversations_collection, script_collection, users_collection
from ..models.model import MessageModel
from ..resources.chatbot_lc import llm_ai_chatbot
from ..resources.similarity_model import similarity_model
from ..resources.utils import create_conversation, get_dialog_by_index, get_last_step

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)


class Initial:
    @router.get("/")
    async def main():
        """_summary_

        Returns:
            _type_: _description_
        """
        return RedirectResponse(url="/docs/")

    @router.get("/v1/health-checker")
    async def hello_world():
        """_summary_

        Returns:
            Message: _description_
        """
        return {"Ping": "Pong"}, 200


@router.post("/v1/chat")
async def chat(details: MessageModel) -> dict:
    """Process user chat messages and manage conversation history.

    Args:
        details (MessageModel): A data model representing the user message.

    Returns:
        dict: A dictionary containing the response message and conversation status.

    Raises:
        ValueError: If 'user_id' or 'message' keys are missing in the input data.

    Note:
        This function processes user chat messages and manages the conversation history
        for each user identified by 'user_id'.

        The input 'details' must be a valid MessageModel containing at least two keys:
        'user_id' and 'message'. If any of these keys are missing, a ValueError is raised.

        If a conversation exists in the 'conversations_collection' for the given 'user_id',
        the function retrieves the last step from the conversation history.

        If the conversation is not found, a new conversation is created based on the most
        similar index determined using the 'similarity_model' function.

        The function updates the conversation history with the user message and the bot's
        response. It also checks whether the current step is the final step based on the
        'steps' field from the script identified by the 'most_similar_index'.

        The updated conversation history is stored in the 'conversations_collection' with
        the 'user_id' as the identifier.

    Examples:
        Example usage of the function:
        >>> details = MessageModel(user_id="user123", message="Hello, AI!")
        >>> response = await chat(details)
        >>> print(response)
        {
            'message': {
                'step': 1,
                'user_message': 'Hello, AI!',
                'bot_response': 'Hi there! How can I assist you?'
            },
            'is_final_step': False
        }
    """

    data = dict(details)
    user_id_to_find = data.get("user_id")

    if not user_id_to_find or "message" not in data:
        return {"error": "Missing required keys: 'user_id' and 'message'"}

    existing_dialog = conversations_collection.find_one({"user_id": user_id_to_find})

    if existing_dialog:
        most_similar_index = existing_dialog.get("dialog_id")
        last_step = get_last_step(existing_dialog)

        if not last_step or not most_similar_index:
            return {
                "error": "Missing 'last_step' or 'most_similar_index' in the existing document."
            }

        dados_script = get_dialog_by_index(most_similar_index)
        new_document = {
            "step": last_step + 1,
            "user_message": data.get("message"),
            "bot_response": dados_script["script"][last_step]["message"],
        }
        conversations_collection.update_one(
            {"user_id": user_id_to_find}, {"$push": {"conversation": new_document}}
        )
    else:
        most_similar_index = similarity_model(data.get("message"))
        if not most_similar_index:
            return {"error": "Failed to find the most similar index."}

        new_document = create_conversation(data, most_similar_index, user_id_to_find)

    dados_script = get_dialog_by_index(most_similar_index)
    last_step = get_last_step(existing_dialog)

    return {
        "message": new_document,
        "is_final_step": last_step + 1 == dados_script["steps"]
        if last_step is not None
        else False,
    }


@router.post("/v1/chat_ai")
async def chat_ai(details: MessageModel) -> dict:
    """Process user chat messages and generate AI responses.

    Args:
        details (MessageModel): A data model representing the user message.

    Returns:
        dict: A dictionary containing the AI response message.

    Raises:
        ValueError: If 'user_id' or 'message' keys are missing in the input data.

    Raises:
        ValueError: If the last conversation entry is missing the 'step' field.

    Note:
        This function processes user chat messages and generates AI responses. It
        maintains a conversation history for each user identified by 'user_id'.

        The input 'details' must be a valid MessageModel containing at least two
        keys: 'user_id' and 'message'. If any of these keys are missing, a
        ValueError is raised.

        If a user conversation exists in the 'conversations_collection', the function
        retrieves the last step from the conversation history. If the 'step' field is
        missing, a ValueError is raised.

        If a conversation for the user does not exist, a new conversation is created.

        The function calls 'llm_ai_chatbot' to generate an AI response based on the
        user message and the conversation history.

        The AI response is appended to the conversation history with an incremented
        step number and updated in the 'conversations_collection'.

    Examples:
        Example usage of the function:
        >>> details = MessageModel(user_id="user123", message="Hello, AI!")
        >>> response = await chat_ai(details)
        >>> print(response)
        {'AI_MESSAGE': 'Hi there! How can I assist you?'}
    """

    try:
        data = dict(details)

        user_id_to_find = data.get("user_id")

        if not user_id_to_find or "message" not in data:
            raise ValueError("Missing required keys: 'user_id' and 'message'")

        existing_document = conversations_collection.find_one(
            {"user_id": user_id_to_find}
        )

        if existing_document:
            last_step = get_last_step(existing_document)
            if last_step is None:
                raise ValueError("Missing 'step' in the last conversation entry.")
        else:
            last_step = 0
            existing_document = {
                "user_id": user_id_to_find,
                "conversation": [],
            }

        ai_message = llm_ai_chatbot(
            input=data.get("message"),
            input_memory=existing_document.get("conversation", []),
        )

        new_document = {
            "step": last_step + 1,
            "user_message": data.get("message"),
            "bot_response": ai_message,
        }

        existing_document["conversation"].append(new_document)

        conversations_collection.update_one(
            {"user_id": user_id_to_find}, {"$set": existing_document}, upsert=True
        )

        return {"AI_MESSAGE": ai_message}

    except ValueError as ve:
        return {"error": str(ve)}

    except Exception as e:
        return {"error": "An unexpected error occurred."}
