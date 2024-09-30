from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.api.models import Location, Department, Category, SubCategory, SKU
from pydantic import BaseModel
import logging
logger = logging.getLogger('app')
sku_router = APIRouter()


class MetaData(BaseModel):
    location_id: int
    department_id: int
    category_id: int
    subcategory_id: int

class CreateSku(BaseModel):
    name: str
    location_id: int
    department_id: int
    category_id: int
    subcategory_id: int

@sku_router.post('/skus/search')
async def get_sku_details(metadata:MetaData, db: Session = Depends(get_db)):
    try:
        logger.info(f'Fetching SKU details for location: {metadata.location_id} depatment: {metadata.department_id}, category: {metadata.category_id} and subcategory: {metadata.subcategory_id}')
        sku_data =  db.query(SKU).filter(
            SKU.location_id == metadata.location_id,
            SKU.department_id == metadata.department_id,
            SKU.category_id == metadata.category_id,
            SKU.subcategory_id == metadata.subcategory_id
        ).all()
        sku_data = [{'sku_id':sku.id,'sku_name': sku.name} for sku in sku_data]
        logger.info(f'Fetched {len(sku_data)} SKU data')
        return sku_data if sku_data else [{'message': 'No SKUs found for the given metadata'}]
    except Exception as err_msg:
        logger.error(f"Error in fetching sku details: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))

@sku_router.post('/skus', status_code=status.HTTP_201_CREATED)
async def get_sku_details(sku:CreateSku, db: Session = Depends(get_db)):
    try:
        logger.info(f'Creating the sku: {sku.name}')
        location =  db.query(Location).filter(Location.id==sku.location_id).first()
        if not location:
            logger.error(f'Location not found: {sku.location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id==sku.location_id, Department.id==sku.department_id).first()
        if not department:
            logger.error(f'Department: {sku.department_id} not found for location: {sku.location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found for given location')
        category =  db.query(Category).filter(Category.id==sku.category_id, Category.location_id==sku.location_id, Category.department_id==sku.department_id).first()
        if not category:
            logger.error(f'Category: {sku.category_id} not found for location : {sku.location_id}, department: {sku.department_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found for givel department and location')
        subcategory =  db.query(SubCategory).filter(SubCategory.id==sku.subcategory_id, SubCategory.category_id==sku.category_id, SubCategory.department_id==sku.department_id, SubCategory.location_id==sku.location_id).first()
        if not subcategory:
            logger.error(f'Subcategory: {sku.subcategory_id} not found for category: {sku.category_id}, department: {sku.department_id} and location: {sku.location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subcategory not found for given category')
        sku = SKU(name=sku.name, location_id=sku.location_id, department_id = sku.department_id, category_id=sku.category_id, subcategory_id=sku.subcategory_id)
        db.add(sku)
        try:
            db.commit()
            db.refresh(sku)
            logger.info(f'SKU created successfully: {sku.id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in creating SKU: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))

        return sku
    except Exception as err_msg:
        logger.error(f"Error in creatinng sku: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))