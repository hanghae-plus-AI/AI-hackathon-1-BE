from sqlalchemy.orm import Session

from models import User
from user.user_schema import NewUser

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(user_id: str, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(new_user: NewUser, db: Session):
    new_user = User(
        user_id=new_user.user_id,
        password=password_context.hash(new_user.password),
        name=new_user.name,
        age=new_user.age,
        gender=new_user.gender,
        job=new_user.job,
        further_details=new_user.further_details
    )
    db.add(new_user)
    db.commit()

    