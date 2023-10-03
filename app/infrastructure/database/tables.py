from typing import TypeVar

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class UsersTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    report = Column(String, nullable=False)
    update_date = Column(DateTime, nullable=False)
