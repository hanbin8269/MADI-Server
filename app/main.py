from fastapi import FastAPI
from app.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def test():
    return {"message": "Hello FastAPI"}


app.include_router(api_router)
