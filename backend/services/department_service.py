from sqlalchemy.exc import SQLAlchemyError
from models.department import Department
from utils.db import get_db_session


# -----------------------------------------
# Create Department
# -----------------------------------------
def create_department_service(name, description):
    session = get_db_session()
    try:
        existing = session.query(Department).filter(Department.name == name).first()
        if existing:
            raise ValueError("Department already exists")

        department = Department(
            name=name,
            description=description
        )

        session.add(department)
        session.commit()
        session.refresh(department)

        return {
            "id": department.id,
            "name": department.name,
            "description": department.description
        }

    except SQLAlchemyError:
        session.rollback()
        raise

    finally:
        session.close()


# -----------------------------------------
# Get All Departments
# -----------------------------------------
def get_all_departments_service():
    session = get_db_session()
    try:
        departments = session.query(Department).all()

        return [
            {
                "id": dept.id,
                "name": dept.name,
                "description": dept.description
            }
            for dept in departments
        ]

    finally:
        session.close()


# -----------------------------------------
# Get Department by ID
# -----------------------------------------
def get_department_by_id_service(department_id):
    session = get_db_session()
    try:
        dept = session.query(Department).filter(Department.id == department_id).first()

        if not dept:
            raise ValueError("Department not found")

        return {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description
        }

    finally:
        session.close()