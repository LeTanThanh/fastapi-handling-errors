from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path

from typing import Annotated

app = FastAPI()

# Use HTTPException
@app.get("/items/{id}")
async def read_item(id: Annotated[str, Path()]):
  items = { "foo": "The Foo Wrestlers" }

  if id not in items:
    raise HTTPException(status_code = 404, detail = "Item not found")

  return { "item": items[id] }
