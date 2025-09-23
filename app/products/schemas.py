from pydantic import BaseModel


class SProductSchemas(BaseModel):
    name: str
    price: int
    description:str
    catalog_id:int
    product_images:str