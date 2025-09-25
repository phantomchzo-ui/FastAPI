from sqlalchemy import select

from app.database import async_session
from app.products.model import Product
from app.users.models import User


async def purchase_product(user_id:int, product_id:int):
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.id==user_id))
            product = await session.scalar(select(Product).where(Product.id==product_id))

            if not user:
                return {"success": False, "message": "User not found"}

            if not product:
                return {"success": False, "message": "Product not found"}

            if product.count < 1:
                return {"success": False, "message": "Product out of stock"}

            if user.balance < product.price:
                return {"success": False, "message": "Insufficient balance"}

            user.balance = user.balance - product.price
            product.count = product.count - 1

            await session.commit()
            return {"success": True, "message": "Purchase successful"}


        except Exception as e:
            await session.rollback()
            return {"success": False, "message": f"Error: {str(e)}"}

