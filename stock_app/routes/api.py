from fastapi import APIRouter
from src.user import views as user_view
from src.inventory import views as inventory_views






router = APIRouter()
router.include_router(user_view.router)

router.include_router(inventory_views.router)



