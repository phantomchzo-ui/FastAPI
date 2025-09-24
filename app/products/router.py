from fastapi import APIRouter, Depends

from app.pagination import PaginationParams
from app.products.dao import ProductDAO
from app.products.schemas import SProductSchemas
from app.users.dependencies import require_role
from app.users.models import User
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/products',
                   tags=['Products'])

@router.get('/')
@cache(expire=900)
async def get_products():
    return await ProductDAO.find_all()



@router.get('/by_{catalog_id}')
async def get_products_by_catalog_id(catalog_id:int):
    return await ProductDAO.find_by_category(catalog_id)


@router.post('/add_product')
async def add_product(
    product_data: SProductSchemas,
    user: User = Depends(require_role("admin", "manager"))
):
    return await ProductDAO.add(
        name=product_data.name,
        price=product_data.price,
        description=product_data.description,
        catalog_id=product_data.catalog_id,
        product_images=product_data.product_images
    )

@router.delete('/delete_product/{product_id}')
async def remove_product(product_id:int, user: User = Depends(require_role("admin", "manager"))):
    return await ProductDAO.remove(product_id)

@router.put('/put_products/{product_id}')
async def put_products(product_id:int, product_data: SProductSchemas,
                       user: User = Depends(require_role("admin", "manager"))):
    await ProductDAO.update(product_id, product_data.dict())
    return {"status": "updated"}
