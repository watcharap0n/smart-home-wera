from fastapi import FastAPI
from routes import callback
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://portfolio-watcharapon.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    callback.router,
    prefix="/callback",
    tags=["callback"],
    responses={418: {"description": "I'm a teapot"}},
)

if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, debug=True)

