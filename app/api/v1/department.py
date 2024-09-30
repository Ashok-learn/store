from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.api.models import Location, Department, Category, SubCategory, SKU
from pydantic import BaseModel
import logging
logger = logging.getLogger('app')
department_router = APIRouter()


class DepartmentCreate(BaseModel):
    name: str


@department_router.post("/location/{location_id}/department", status_code=status.HTTP_201_CREATED)
async def create_department(location_id:int, department: DepartmentCreate , db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating department: {department.name} for location ID: {location_id}")
        location =  db.query(Location).filter(Location.id==location_id).first()
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department_obj = Department(name = department.name, location_id=location_id)
        try:
            db.add(department_obj)
            db.commit()
            db.refresh(department_obj)
            logger.info(f"Department created successfully: {department_obj.id}")
        except Exception as err_msg:
            db.rollback()
            logger.error(f"Error creating department: {err_msg}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return department_obj
    except Exception as err_msg:
        logger.error(f"Error creating department: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@department_router.get("/location/{location_id}/department")
async def get_departments_by_location(location_id:int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all departments")
        location =  db.query(Location).filter(Location.id==location_id).first()
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Location not found')
        department =  db.query(Department).filter(Department.location_id==location_id).all()

        if not department:
            logger.error(f"Department not found for location: {location_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Departments found for this location")
        logger.info(f"Fetched {len(department)} departments")
        return department
    except Exception as err_msg:
        logger.error(f"Error while fetching departments: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@department_router.put("/api/v1/location/{location_id}/department/{department_id}", response_model=DepartmentCreate)
async def update_department(location_id: int, department_id: int, department: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f'updating the department: {department_id}')
        department_obj =  db.query(Department).filter(Department.id == department_id,
                                                     Department.location_id == location_id).first()
        if not department_obj:
            logger.error(f'Department not found f: {department_id}')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        try:
            department_obj.name = department.name
            db.commit()
            db.refresh(department_obj)
            logger.info(f"Department updated successfully: {department_obj.id}")
        except Exception as err_msg:
            db.rollback()
            logger.error(f"Error updating department: {err_msg}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return department_obj
    except Exception as err_msg:
        logger.error(f"Error updating department: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@department_router.delete("/api/v1/location/{location_id}/department/{department_id}")
async def delete_department(location_id: int, department_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting department: {department_id}")
        department_obj =  db.query(Department).filter(Department.id == department_id,
                                                     Department.location_id == location_id).first()
        if not department_obj:
            logger.warning(f"Department not found for deletion: {department_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        try:
            db.delete(department_obj)
            db.commit()
            logger.info(f"Department deleted successfully: {department_id}")
        except Exception as err_msg:
            db.rollback()
            logger.error(f"Error deleting department: {err_msg}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return {"message": "Department deleted successfully"}
    except Exception as err_msg:
        logger.error(f"Error deleting department: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


