from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path

from typing import Annotated

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
