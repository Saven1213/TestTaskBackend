from pydantic import BaseModel




class ProductsOut(BaseModel):
    id: int
    name: str
    description: str