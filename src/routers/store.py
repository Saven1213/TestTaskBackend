from fastapi.params import Depends

from src.db.models.user import User
from fastapi import APIRouter
from typing import List

from src.schemas.store import ProductsOut
from src.security.oauth2 import get_current_user

router = APIRouter(prefix='/store', tags=['Store'])






@router.get('/products', response_model=List[ProductsOut])
async def get_products(
        current_user: User = Depends(get_current_user)
):
    products_data = [
        ProductsOut(id=1, name="Футболка", description="Легкая и удобная, 100% хлопок"),
        ProductsOut(id=2, name="Джинсы", description="Классические синие джинсы"),
        ProductsOut(id=3, name="Кроссовки", description="Спортивные кроссовки для бега"),
        ProductsOut(id=4, name="Рюкзак", description="Водонепроницаемый рюкзак для ноутбука"),
        ProductsOut(id=5, name="Наушники", description="Беспроводные наушники с шумоподавлением"),
        ProductsOut(id=6, name="Часы", description="Умные часы с пульсометром"),
        ProductsOut(id=7, name="Кружка", description="Керамическая кружка с принтом"),
        ProductsOut(id=8, name="Книга", description="Бестселлер 'Мастер и Маргарита'"),
        ProductsOut(id=9, name="Зарядное устройство", description="Быстрая зарядка для телефона"),
        ProductsOut(id=10, name="Кепка", description="Бейсболка с вышивкой"),
    ]

    return products_data

