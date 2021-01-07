from typing import List, Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import TSVectorType

from sodermalm.database import Base
from sodermalm.enums import UserRoles
from sodermalm.models import ORMBase, TimeStampMixin


class User(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    # For now, a user has a single role - this will likely be refactored later
    role = Column(String, default=UserRoles.user)
    firebase_id = Column(String, nullable=True)

    search_vector = Column(TSVectorType('email', weights={'email': 'A'}))

    def principals(self):
        return [f'user:{self.email}', f'role:{self.role}']


# Pydantic schemas
class UserBase(ORMBase):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRoles = UserRoles.user


class UserRead(UserBase):
    id: int
    firebase_id: Optional[str]


class UserPagination(ORMBase):
    total: int
    items: List[UserRead] = []
