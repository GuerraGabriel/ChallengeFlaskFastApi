import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = sa.Column(sa.Integer, primary_key=True)
    cep = sa.Column(sa.String)
    number = sa.Column(sa.String)
    street = sa.Column(sa.String)
    neighborhood = sa.Column(sa.String)
    city = sa.Column(sa.String)
    state = sa.Column(sa.String)
    country = sa.Column(sa.String)

    # Relacionamento com usuário
    user = relationship("User", back_populates="address", uselist=False)
