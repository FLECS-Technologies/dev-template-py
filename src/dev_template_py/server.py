"""A small example server that handles post requests on /add."""
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from dev_template_py.example import add_numbers

class BelowErrorFilter(logging.Filter):
    """A logging filter that only allows loggings below level ERROR."""

    def filter(self, record):
        """Filter everything with loggings below level ERROR."""
        return record.levelno < logging.ERROR


logger = logging.getLogger(__name__)


class AddParameters(BaseModel):
    """The parameters required in the body on /add."""

    left: float
    right: float


app = FastAPI(title="MyApp API", version="1.0")


@app.post("/add")
async def handle_post_add(params: AddParameters):
    """Handles a request on /add by adding the two number from the body."""
    logger.error("/add endpoint accessed")
    result = add_numbers(params.left, params.right)
    return {"result": result}
