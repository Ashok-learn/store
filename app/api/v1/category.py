from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.api.models import Location, Department, Category, SubCategory, SKU
from pydantic import BaseModel
import logging
logger = logging.getLogger('app')
category_router = APIRouter()


class CategoryCreate(BaseModel):
    name: str


@category_router.post("/location/{location_id}/department/{department_id}/category", status_code=status.HTTP_201_CREATED)
async def create_category(location_id:int, department_id: int,category: CategoryCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating category under location: {location_id}, department: {department_id}")
    try:
        location =  db.query(Location).filter(Location.id==location_id).first()
        if not location:
            logger.error(f'Location not found Location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id==location_id, Department.id==department_id).first()
        if not department:
            logger.error(f'Department:{department.name} not found for Location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not given for the given loaction')
        new_category = Category(name=category.name, department_id=department_id, location_id=location_id)
        db.add(new_category)
        try:
            db.commit()
            db.refresh(new_category)
            logger.info(f'Category created successfuly: {new_category.id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error while creating category : {category.name} error is: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return new_category
    except Exception as err_msg:
        logger.error(f'Error while creating category : {category.name} error is: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@category_router.get("/location/{location_id}/department/{department_id}/category")
async def get_categories_by_location_and_department(location_id:int, department_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f'Category data is fetching for location: {location_id} and department: {department_id}')
        location =  db.query(Location).filter(Location.id==location_id).first()
        if not location:
            logger.error(f'Location not found location :{location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id==location_id, Department.id==department_id).first()
        if not department:
            logger.error(f'Department {department_id} not found for location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found for the specified loaction')
        category =  db.query(Category).filter(Category.department_id==department_id, Category.location_id==location_id).all()
        logger.info(f'Fetched {len(category)} categories')
        return category
    except Exception as err_msg:
        logger.error(f'Error in fetching category data: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@category_router.put("/api/v1/location/{location_id}/department/{department_id}/category/{category_id}", response_model=CategoryCreate)
async def update_category(location_id: int, department_id: int, category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f'Updating category : {category_id}')
        category_obj =  db.query(Category).filter(Category.id == category_id, Category.department_id == department_id, Category.location_id == location_id).first()
        if not category_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        category_obj.name = category.name
        try:
            db.commit()
            db.refresh(category_obj)
            logger.info(f'Category information updated successfully: {category_id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in updating category: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return category_obj
    except Exception as err_msg:
        logger.error(f'Error in updating category data: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@category_router.delete("/api/v1/location/{location_id}/department/{department_id}/category/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(location_id: int, department_id: int, category_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f'Deleting Category: {category_id}')
        category_obj =  db.query(Category).filter(Category.id == category_id, Category.department_id == department_id, Category.location_id == location_id).first()
        if not category_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        try:
            db.delete(category_obj)
            db.commit()
            logger.info(f'Category deleted successfully: {category_id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in deleting category: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return {"message": "Category deleted successfully"}
    except Exception as err_msg:
        logger.error(f'Error in deleting category: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


