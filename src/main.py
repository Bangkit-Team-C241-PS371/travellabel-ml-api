import os

from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from model import fake_answer_to_everything_ml_model

# load env vars
load_dotenv()

# store models here (so that it will be loaded upon the lifespan of the app)
ml_models = {}

# lifespan function helps create code that will be run once on startup and once on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root(req: Request):
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(req: Request, item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# runner script for deployment (uses listen port from env)
if __name__ == "__main__":
    import uvicorn
    server_port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=server_port, proxy_headers=True, log_level="warning")
