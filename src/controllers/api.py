from fastapi import APIRouter, Depends
from langchain.memory import MongoDBChatMessageHistory
from starlette.responses import RedirectResponse

from database import DB_URL

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


class Bot:
    @router.post("/bot")
    async def message(connection_string: Depends(DB_URL)):
        message_history = MongoDBChatMessageHistory(
            connection_string=connection_string, session_id="test-session"
        )

        message_history.add_user_message("hi!")

        message_history.add_ai_message("whats up?")
