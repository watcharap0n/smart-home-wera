from fastapi import FastAPI
from routes import callback
import uvicorn

app = FastAPI()

app.include_router(
    callback.router,
    prefix="/callback",
    tags=["callback"],
    responses={418: {"description": "I'm a teapot"}},
)

if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, debug=True)

