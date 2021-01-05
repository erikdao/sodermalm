from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy_utils import TSVectorType

# from sodermalm.models import TimeStampMixin


# class Team(TimeStampMixin):
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)
#     search_vector = Column(TSVectorType('name'))

class Team(BaseModel):
    id: int
    name: str
    description: Optional[str]
