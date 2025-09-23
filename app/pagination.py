from fastapi import Depends
from pydantic import BaseModel, Field
from sqlalchemy.sql.annotation import Annotated


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, description='s')
    offset: int = Field(0, ge=0)

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]