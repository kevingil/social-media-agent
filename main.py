from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.staticfiles import StaticFiles
from controllers import user, campaign, media, post
from database import Database
from utils.auth import AuthBackend

import asyncio
import uvicorn

app = FastAPI()

db = Database()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret")
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

app.include_router(user.router)
app.include_router(campaign.router)
app.include_router(media.router)
app.include_router(post.router)



if __name__ == "__main__":
    db.init()
    uvicorn.run("main:app", port=3000, log_level="info")
