from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from utils.db import get_db_session


# ----------------------------------------
# Create New User
# ----------------------------------------
def create_user(name, email, password, role):
    session = get_db_session()
    try:
        new_user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user

    except SQLAlchemyError as e:
        session.rollback()
        raise e

    finally:
        session.close()


# ----------------------------------------
# Get User By Email
# ----------------------------------------
def get_user_by_email(email):
    session = get_db_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        return user

    except SQLAlchemyError as e:
        raise e

    finally:
        session.close()