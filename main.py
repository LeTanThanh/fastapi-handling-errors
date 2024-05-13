from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Body
from fastapi import Request
from fastapi import status

from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from typing import Annotated

from exceptions.uniconrn_exception import UnicornException

from models.item import Item

app = FastAPI(debug = True)

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
"""
@app.get("/items/{id}")
async def read_item(id: Annotated[str, Path()]):
  if id not in ITEMS:
    raise HTTPException(
      status_code = 404,
      detail = "Item not found",
      headers = {"X-Error": "There goes my error"}
    )

  return { "item": ITEMS[id] }
"""

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

# Override the default exception handlers
"""
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exception: RequestValidationError):
  return PlainTextResponse(str(exception), status_code = status.HTTP_400_BAD_REQUEST)
"""

@app.exception_handler(StarletteHTTPException)
async def starlette_http_Exception_handler(request: Request, exception: StarletteHTTPException):
  return PlainTextResponse(str(exception.detail), status_code = exception.status_code)

@app.get("/items/{id}")
async def read_item(id: Annotated[int, Path()]):
  if id == 3:
    raise HTTPException(
      status_code = status.HTTP_418_IM_A_TEAPOT,
      detail = "Nope! I don't liek 3."
    )

  return {"id": id}

# Use the RequestValidationError body
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exception: RequestValidationError):
  return JSONResponse(
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
    content = jsonable_encoder({
      "errors": exception.errors(),
      "body": exception.body
    })
  )

@app.post("/items", status_code = status.HTTP_201_CREATED)
async def create_item(item: Annotated[Item, Body(embed = True)]):
  return item
