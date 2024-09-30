# Department Store API
This is a FastAPI project that provides a set of RESTful APIs for managing a department store, including operations for locations, departments, categories, subcategories, and SKUs (Stock Keeping Units). The API is built with an asynchronous architecture using SQLAlchemy and PostgreSQL.


## Features
- Create, read, update, and delete (CRUD) operations for:
  - Locations
  - Departments
  - Categories
  - Subcategories
  - SKUs
- database operations using SQLAlchemy
- Error handling and logging

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [uvicorn](https://www.uvicorn.org/)

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <your-repository-name>

2. python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. pip install -r requirements.txt
4. uvicorn app.app:app --reload

## Endpoints

# Location
  1. POST - /location
  2. GET - /location
  3. PUT - /location/{location_id}
  4. DELETE - /api/v1/location/{location_id}
# Department
  1. POST - /location/{location_id}/department
  2. GET - /location/{location_id}/department
  3. PUT - /api/v1/location/{location_id}/department/{department_id}
  4. DELETE - api/v1/location/{location_id}/department/{department_id}
# Category
  1. POST - /location/{location_id}/department/{department_id}/category
  2. GET - /location/{location_id}/department/{department_id}/category
  3. PUT - /api/v1/location/{location_id}/department/{department_id}/category/{category_id}
  4. DELETE - /api/v1/location/{location_id}/department/{department_id}/category/{category_id}
# Subcategory
  1. POST - /location/{location_id}/department/{department_id}/category/{category_id}/subcategory
  2. GET - /location/{location_id}/department/{department_id}/category/{category_id}/subcategory
  3. PUT - /api/v1/location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id}
  4. DELETE - /api/v1/location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id}
  5. GET - /location/{location_id}/department/{department_id}/category/{category_id}/subcategory/{subcategory_id} 
# SKU
  1. POST - /skus/search
  2. POST - /skus
