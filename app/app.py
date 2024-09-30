from fastapi import FastAPI
from app.api.v1 import location, department, category, sub_category, sku
from app.core.database import Base, engine
from app.core.config import settings
from app.core.logging_config import setup_logging
setup_logging()
app = FastAPI(title="Department Store")

app.include_router(location.location_router, tags=['Location'], prefix=settings.API_PREFIX)
app.include_router(department.department_router, tags=['Department'], prefix=settings.API_PREFIX)
app.include_router(category.category_router, tags=['Category'], prefix=settings.API_PREFIX)
app.include_router(sub_category.subcategory_router,tags=['Sub Category'], prefix=settings.API_PREFIX)
app.include_router(sku.sku_router,tags=['SKU'], prefix=settings.API_PREFIX)


@app.on_event('startup')
async def startup():
    Base.metadata.create_all(bind=engine)