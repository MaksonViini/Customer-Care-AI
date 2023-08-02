from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .config import root_path
from .controllers import controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.mount("/static", StaticFiles(directory=f"{root_path}/static"), name="static")
app.include_router(controller.router)
