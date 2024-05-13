from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from typing import Annotated

from exceptions.uniconrn_exception import UnicornException

app = FastAPI()

ITEMS = { "foo": "The Foo Wrestlers" }

# Use HTTPException
"""
@app.get("/items/{id}")
async def read_item(id: Annotated[str, Path()]):
  if id not in ITEMS:
    raise HTTPException(status_code = 404, detail = "Item not found")

  return { "item": ITEMS[id] }
"""

# Add custom headers
@app.get("/items/{id}")
async def read_item(id: Annotated[str, Path()]):
  if id not in ITEMS:
    raise HTTPException(
      status_code = 404,
      detail = "Item not found",
      headers = {"X-Error": "There goes my error"}
    )

  return { "item": ITEMS[id] }

# Install custom exception handlers
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exception: UnicornException):
  return JSONResponse(
    status_code = status.HTTP_418_IM_A_TEAPOT,
    content = {
      "message": f"Oops! {exception.name} did something. There goes a rainbow..."
    }
  )

@app.get("/unicorns/{name}")
async def read_unicorns(name: Annotated[str, Path()]):
  if name == "yolo":
    raise UnicornException(name = name)

  return {"name": name}
