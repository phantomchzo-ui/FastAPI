from pydantic import BaseModel


class SCatalogSchemas(BaseModel):
    name: str
    catalog_images: str