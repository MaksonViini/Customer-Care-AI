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
from ..resources.similarity_model import similarity_model

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


# Chave secreta para assinar os JWTs
SECRET_KEY = "mysecretkey"

# Configurando o esquema de autenticação com OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para decodificar o JWT e obter o ID do usuário
# def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return payload.get("sub")
#     except jwt.ExpiredSignatureError as e:
#         raise HTTPException(status_code=401, detail="Token expirado") from e
#     except jwt.InvalidTokenError as e:
#         raise HTTPException(status_code=401, detail="Token inválido") from e


# Rota para o endpoint "/v1/chat"
@router.post("/v1/chat")
async def chat(
    details: MessageModel,
    # user_id: str = Depends(get_user_id_from_token)
):
    """_summary_

    Returns:
        Message: _description_
    """

    data = dict(details)

    user_id_to_find = data.get("user_id")

    # Check if the document with the "user_id" already exists in the collection

    if existing_document := conversations_collection.find_one(
        {"user_id": user_id_to_find}
    ):
        last_step = existing_document["conversation"][-1]["step"]

        most_similar_index = int(existing_document["dialog_id"])

        dados_script = script_collection.find_one({"script_id": most_similar_index})

        new_document = {
            "step": last_step + 1,
            "user_message": data.get("message"),
            "bot_response": dados_script["script"][last_step]["message"],
        }

        existing_document["conversation"].append(new_document)

        conversations_collection.update_one(
            {"user_id": str(user_id_to_find)}, {"$set": existing_document}
        )
    else:
        # Insert the document into the collection, as the "user_id" doesn't exist yet

        most_similar_index = int(similarity_model(data.get("message")))

        dados_script = script_collection.find_one({"script_id": most_similar_index})

        bot_response = dados_script["script"][0]["message"]

        # Create the document to insert into the collection (if you don't have it already)
        user_dialog = {
            "dialog_id": most_similar_index,
            "user_id": 1,
            "conversation": [
                {
                    "step": 1,
                    "user_message": data.get("message"),
                    "bot_response": bot_response,
                }
            ],
        }
        conversations_collection.insert_one(user_dialog)
        return {"Status": "Document inserted successfully!"}

    return dict(existing_document["conversation"][-1]), 200
