from fastapi import FastAPI
from pydantic import BaseModel
from dev_template_py.example import add_numbers
import logging


class BelowErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


logger = logging.getLogger(__name__)


class AddParameters(BaseModel):
    left: float
    right: float


app = FastAPI(title="MyApp API", version="1.0")


@app.post("/add")
async def perform_action(params: AddParameters):
    logger.error("/add endpoint accessed")
    result = add_numbers(params.left, params.right)
    return {"result": result}
