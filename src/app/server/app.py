import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.auth_user import router as AuthRouter
from starlette.middleware.sessions import SessionMiddleware
from decouple import config

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config('SECRET_KEY'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter, tags=['auth'], prefix="/auth")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
