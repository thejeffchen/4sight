from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from foresight.db.session import init_db
from foresight.api.chat import router as chat_router
from foresight.api.diff import router as diff_router
from foresight.api.settings import router as settings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="4sight Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(diff_router)
app.include_router(settings_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
