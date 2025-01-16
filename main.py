from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings
from core.models import Base, db
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db.dispose()
    # async with db.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    # yield


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
main_app.include_router(items_router)
main_app.include_router(users_router)


@main_app.get("/")
def home():
    return {"message": f"http://127.0.0.1:8000/docs"}


@main_app.get("/hello")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello, {name}!!!1122"}


@main_app.post("/calc/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


if __name__ == "__main__":
    uvicorn.run("main:main_app", reload=True)
