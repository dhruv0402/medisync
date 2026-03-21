from backend.utils.db import get_db_session
from sqlalchemy.exc import SQLAlchemyError


# -----------------------------------
# Generic Fetch All
# -----------------------------------
def fetch_all(model):
    session = get_db_session()
    try:
        return session.query(model).all()
    except SQLAlchemyError as e:
        print("DB Error:", e)
        return []
    finally:
        session.close()


# -----------------------------------
# Fetch By ID
# -----------------------------------
def fetch_by_id(model, record_id):
    session = get_db_session()
    try:
        return session.query(model).get(record_id)
    except SQLAlchemyError as e:
        print("DB Error:", e)
        return None
    finally:
        session.close()


# -----------------------------------
# Create Record
# -----------------------------------
def create_record(obj):
    session = get_db_session()
    try:
        session.add(obj)
        session.commit()
        return obj
    except SQLAlchemyError as e:
        session.rollback()
        print("DB Error:", e)
        return None
    finally:
        session.close()


# -----------------------------------
# Delete Record
# -----------------------------------
def delete_record(obj):
    session = get_db_session()
    try:
        session.delete(obj)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print("DB Error:", e)
        return False
    finally:
        session.close()
