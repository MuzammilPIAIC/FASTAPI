from fastapi import APIRouter
from src.kpi_dashboard import views as kpi_dashboard_views






router = APIRouter()

router.include_router(kpi_dashboard_views.router)



