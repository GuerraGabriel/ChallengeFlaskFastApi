import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    preferred_name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    age = sa.Column(sa.Integer)
    occupation = sa.Column(sa.String)

    address_id = sa.Column(sa.Integer, sa.ForeignKey("addresses.id"), unique=True)
    address = relationship("Address", back_populates="user", uselist=False)
