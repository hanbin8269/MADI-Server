from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash,
    verify_password,
)
import uuid
from app.crud.base import CRUDBase
from app.model.user import User
from app.schema.user import UserCreate, UserUpdate
from app.api import dependencies


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            uuid=uuid.uuid4(),
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            std_no=obj_in.std_no,
            name=obj_in.name,
            gender=obj_in.gender.value,
            profile_image=obj_in.profile_image,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, obj: User) -> Any:
        db.delete(obj)
        db.commit()
        return obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
