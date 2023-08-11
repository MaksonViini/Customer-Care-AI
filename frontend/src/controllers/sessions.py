from datetime import datetime, timedelta
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie

from ..schemas.session import BasicVerifier, SessionData
from .route import router

cookie_params = CookieParameters(max_age=900)

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="YOUR_SECRET_KEY",
    cookie_params=cookie_params,
)


backend = InMemoryBackend[UUID, SessionData]()


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="Invalid session"),
)


@router.post("/create_session/{name}")
async def create_session(name: str):
    session_uuid = uuid4()

    expiration_time = datetime.now() + timedelta(minutes=15)
    data = SessionData(
        username=name, uuid=session_uuid, expiration_time=expiration_time
    )

    await backend.create(session_uuid, data)
    session_id_str = str(session_uuid.hex)
    return {"session_id": session_id_str}


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return f"Deleted session uuid: {session_id}"
