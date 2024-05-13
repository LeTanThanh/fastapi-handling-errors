from pydantic import BaseModel

class Item(BaseModel):
  title: str
  size: int
