from fastapi import APIRouter, Depends
from app.catalog.dao import CatalogDAO
from app.catalog.schemas import SCatalogSchemas
from app.users.dependencies import require_role
from app.users.models import User

router = APIRouter(prefix='/catalog',
    tags=['Catalog'])

@router.get('')
async def get_catalog():
    return await CatalogDAO.find_all(limit=10, offset=3)


@router.post('/add_catalog')
async def add_catalog(catalog_data: SCatalogSchemas, user: User = Depends(require_role("admin", "manager"))):
    await CatalogDAO.add(name=catalog_data.name, catalog_images=catalog_data.catalog_images)
    return catalog_data


@router.delete('/remove_catalog/{catalog_id}')
async def remove_catalog(catalog_id:int, user: User = Depends(require_role("admin", "manager"))):
    await CatalogDAO.remove(catalog_id)
    return {True: catalog_id}

@router.put('/put_catalog')
async def put_catalog(catalog_id: int, catalog_data: SCatalogSchemas, user: User = Depends(require_role("admin", "manager"))):
    await CatalogDAO.update(catalog_id, catalog_data.dict())
    return catalog_data