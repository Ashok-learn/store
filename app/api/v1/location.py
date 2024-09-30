from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.api.models import Location, Department, Category, SubCategory, SKU
from pydantic import BaseModel
import logging

logger = logging.getLogger('app')
location_router = APIRouter()


class LocationCreate(BaseModel):
    name: str
    address: str | None = None


@location_router.post("/location", status_code=201)
async def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f'Creating location: {location.name}')
        location_obj = Location(name=location.name, address=location.address)
        db.add(location_obj)
        try:
            db.commit()
            db.refresh(location_obj)
            logger.info(f'Location created successfully: {location_obj.id}')
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in creating location: {err_msg}')
            raise HTTPException(status_code=500, detail=str(err_msg))
        return location_obj
    except Exception as err_msg:
        logger.error(f'Error in creating location: {err_msg}')
        raise HTTPException(status_code=500, detail=str(err_msg))


@location_router.get("/location")
async def get_locations(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all locations")
        location_data =  db.query(Location).with_entities(Location.id, Location.name, Location.address).order_by(Location.id).all()
        logger.info(f"Fetched {len(location_data)} locations")
        return {'data':location_data}
    except Exception as err_msg:
        logger.error(f"Error fetching locations: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@location_router.put("/location/{location_id}")
async def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating location: {location_id}")
        location_obj =  db.query(Location).filter(Location.id == location_id).first()
        if not location_obj:
            logger.warning(f"Location not found: {location_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

        location_obj.name = location.name
        location_obj.address = location.address
        try:
            db.commit()
            db.refresh(location_obj)
            logger.info(f"Location updated successfully: {location_obj.id}")
        except Exception as err_msg:
            db.rollback()
            logger.error(f'Error in updating location: {err_msg}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return location_obj
    except Exception as err_msg:
        logger.error(f'Error in updating location: {err_msg}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))


@location_router.delete("/api/v1/location/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting location: {location_id}")
        location_obj =  db.query(Location).filter(Location.id == location_id).first()
        if not location_obj:
            logger.warning(f"Location not found for deletion: {location_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        try:
            db.delete(location_obj)
            db.commit()
            logger.info(f"Location deleted successfully: {location_id}")
        except Exception as err_msg:
            db.rollback()
            logger.error(f"Error deleting location: {err_msg}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
        return {"message": "Location deleted successfully"}
    except Exception as err_msg:
        logger.error(f"Error deleting location: {err_msg}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err_msg))
