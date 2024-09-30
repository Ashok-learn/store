from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Float
from app.core.database import Base

class Location(Base):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'test_schema'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {'schema': 'test_schema'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location_id = Column(Integer, ForeignKey("test_schema.locations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {'schema': 'test_schema'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department_id = Column(Integer, ForeignKey("test_schema.departments.id"))
    location_id = Column(Integer, ForeignKey("test_schema.locations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SubCategory(Base):
    __tablename__ = "subcategories"
    __table_args__ = {'schema': 'test_schema'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("test_schema.categories.id"))
    department_id = Column(Integer, ForeignKey("test_schema.departments.id"))
    location_id = Column(Integer, ForeignKey("test_schema.locations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SKU(Base):
    __tablename__ = "skus"
    __table_args__ = {'schema': 'test_schema'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    location_id = Column(Integer, ForeignKey("test_schema.locations.id"))
    department_id = Column(Integer, ForeignKey("test_schema.departments.id"))
    category_id = Column(Integer, ForeignKey("test_schema.categories.id"))
    subcategory_id = Column(Integer, ForeignKey("test_schema.subcategories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Testtab(Base):
    __tablename__ = 'testtable'
    __table_args__ = {'schema': 'test_schema'}
    id = Column(Integer, primary_key=True)
    name= Column(String)