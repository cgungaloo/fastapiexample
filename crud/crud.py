import uuid
from sqlalchemy.orm import Session

from models.models import User, Item
from schemas.schemas import UserCreate, ItemCreate
from security.verify import verify_password

def authenticate_user(db: Session, user_email: str, password: str):
    user = get_user_by_email(db, user_email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return User

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    print(email)
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    print(item)
    
    id = str(uuid.uuid4())
    item_dict = item.model_dump()
    item_dict['owner_id'] = user_id
    item_dict['id'] = id
    # db_item = Item(**item.model_dump(), owner_id=user_id, id=id)
    db_item = Item(**item_dict)
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item