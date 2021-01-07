import re
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from .config import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

engine = create_engine(str(SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(bind=engine)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.plit("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)
