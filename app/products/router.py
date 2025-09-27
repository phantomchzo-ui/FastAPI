from fastapi import APIRouter, Depends, HTTPException

from app.products.dao import ProductDAO
from app.products.payment import purchase_product
from app.products.schemas import SProductSchemas, ProductSchemasEmail
from app.tasks.tasks import send_message_access_order
from app.users.dependencies import require_role, get_current_user
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

@router.post('/{product_id}/buy')
async def buy_product(product_id:int,
                      user: User = Depends(get_current_user)):
    res = await purchase_product(user.id, product_id)

    product = await ProductDAO.find_by_id(product_id)

    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["message"])

    email = 'Phantomchzo@gmail.com'

    product_data = ProductSchemasEmail(
        name=product.name,
        price=product.price,
        description=product.description
    )

    send_message_access_order.delay(email, product_data.model_dump())

    return res

