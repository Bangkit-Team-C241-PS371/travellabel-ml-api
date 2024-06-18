import os

from typing import Annotated, Union
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request, Response, status
from dotenv import load_dotenv
from pydantic import BaseModel

import model
from auth import TokenData, get_current_user

# load env vars
load_dotenv()

# store models here (so that it will be loaded upon the lifespan of the app)
ml_models = {}

# lifespan function helps create code that will be run once on startup and once on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    model.init()
    ml_models["recsys_collab"] = model.collab_recommend

    yield

    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root(req: Request):
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(
        req: Request,
        current_user: Annotated[TokenData, Depends(get_current_user)],
        item_id: int,
        q: Union[str, None] = None
    ):
    return {"item_id": item_id, "q": q, "req_user": current_user}

class PredictionRequest(BaseModel):
    place_name: str

@app.post("/predict")
def predict(
    res: Response,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    req_data: PredictionRequest
):
    try:
        predictions = ml_models["recsys_collab"](req_data.place_name)
    except LookupError as e:
        res.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "Not Found", "message": "Place not found"}
    return {"status": "OK", "predictions": predictions}

# runner script for deployment (uses listen port from env)
if __name__ == "__main__":
    import uvicorn
    server_port = int(os.environ.get('PORT', 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=server_port, proxy_headers=True, log_level="warning")
