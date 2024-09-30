from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.api.models import Location, Department, Category, SubCategory, SKU
from pydantic import BaseModel
import logging
logger = logging.getLogger('app')
subcategory_router = APIRouter()


class SubCategoryCreate(BaseModel):
    name: str


@subcategory_router.post("/location/{location_id}/department/{department_id}/category/{category_id}/subcategory", status_code=status.HTTP_201_CREATED)
async def create_subcategory(location_id:int, department_id:int, category_id:int, subcategory: SubCategoryCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f'Creating the subcategory under category: {category_id} department: {department_id} and location: {location_id}')
        location =  db.query(Location).filter(Location.id == location_id).first()
        if not location:
            logger.error(f'Location not found: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id == location_id,
                                                 Department.id == department_id).first()
        if not department:
            logger.error(f'Department not found: {department_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found for given loaction')
        category =  db.query(Category).filter(Category.location_id == location_id,Category.department_id==department_id,
                                                 Category.id == category_id).first()
        if not category:
            logger.error(f'Category not found : {category_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found for given department')
        new_subcategory = SubCategory(name=subcategory.name, department_id=department_id, location_id=location_id, category_id=category_id)
        db.add(new_subcategory)
        try:
            db.commit()
            db.refresh(new_subcategory)
            logger.info(f'Subcategory created successfully: {new_subcategory.id}')
            return new_subcategory
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in creating sub category: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))

    except Exception as err_msg:
        logger.error(f'Error in creating sub category: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@subcategory_router.get("/location/{location_id}/department/{department_id}/category/{category_id}/subcategory")
async def get_subcategories(location_id:int, department_id:int, category_id:int, db: Session = Depends(get_db)):
    try:
        logger.info(f'Fetching all subcategories')
        location =  db.query(Location).filter(Location.id == location_id).first()
        if not location:
            logger.error(f'Location not found: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id == location_id,
                                                 Department.id == department_id).first()
        if not department:
            logger.error(f'Department: {department_id} not found for location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not found for given loaction')
        category =  db.query(Category).filter(Category.location_id == location_id,Category.department_id==department_id,
                                             Category.id == category_id).first()
        if not category:
            logger.error(f'Category: {category_id} not found for given department: {department_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found for given department')
        subcategory  =  db.query(SubCategory).filter(SubCategory.location_id == location_id,
                                             Category.id == category_id, SubCategory.department_id==department_id).all()
        if not subcategory:
            logger.error(f'Subcategories not found for given category: {category_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subcategory not given for the given category')
        logger.info(f'Fetched {len(subcategory)} subcategories')
        return subcategory
    except Exception as err_msg:
        logger.error(f'Error in fetching subcategories: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@subcategory_router.put("/api/v1/location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id}", response_model=SubCategoryCreate)
async def update_subcategory(location_id: int, department_id: int, category_id: int, subcategory_id: int, subcategory: SubCategoryCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f'updating subcategory: {subcategory_id}')
        subcategory_obj =  db.query(SubCategory).filter(SubCategory.id == subcategory_id, SubCategory.category_id == category_id, SubCategory.department_id == department_id, SubCategory.location_id == location_id).first()
        if not subcategory_obj:
            logger.error(f'Subcategory not found: {subcategory_id}')
            raise HTTPException(status_code=404, detail="SubCategory not found")

        subcategory_obj.name = subcategory.name
        try:
            db.commit()
            db.refresh(subcategory_obj)
            logger.info(f'Subcategory updated successfully')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in updating subcategory: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return subcategory_obj
    except Exception as err_msg:
        logger.error(f'Error in updating subcategory: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@subcategory_router.delete("/api/v1/location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(location_id: int, department_id: int, category_id: int, subcategory_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f'Deleting subcategory: {subcategory_id}')
        subcategory_obj =  db.query(SubCategory).filter(SubCategory.id == subcategory_id, SubCategory.category_id == category_id, SubCategory.department_id == department_id, SubCategory.location_id == location_id).first()
        if not subcategory_obj:
            logger.error(f'Subcategory not found for deletion: {subcategory_id}')
            raise HTTPException(status_code=404, detail="SubCategory not found")
        try:
            db.delete(subcategory_obj)
            db.commit()
            logger.info(f'Subcategory deleted successfully: {subcategory_id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in deleting subcategory: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return {"message": "SubCategory deleted successfully"}
    except Exception as err_msg:
        logger.error(f'Error in deleting subcategory: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@subcategory_router.get("/location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id}")
async def get_subcategory_details_by_location_department_and_category(location_id:int, department_id:int, category_id:int,sub_category_id:int, db: Session = Depends(get_db)):
    try:
        logger.info(f'Fetching dubcategory information : {sub_category_id}')
        location =  db.query(Location).filter(Location.id == location_id).first()
        if not location:
            logger.error(f'Location not found: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id == location_id,
                                                 Department.id == department_id).first()
        if not department:
            logger.error(f'Department: {department_id} not found for location : {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Department not given for the given loaction')
        category =  db.query(Category).filter(Category.location_id == location_id,
                                             Category.id == category_id).first()
        if not category:
            logger.error(f'Category: {category_id} not found for department: {department_id} and location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not given for the given department')
        subcategory =   db.query(SubCategory).filter(SubCategory.location_id == location_id,
                                                              SubCategory.category_id == category_id,
                                                              SubCategory.department_id == department_id, SubCategory.id==sub_category_id).first()
        if not subcategory:
            logger.error(f'Subcategory: {sub_category_id} not found for category: {category_id} department: {department_id} and location: {location_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Subcategory not given for the given category')
        logger.info(f'Subcategory information fetched successfully: {sub_category_id}')
        return subcategory
    except Exception as err_msg:
        logger.error(f'Error in fetching subcategory: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))