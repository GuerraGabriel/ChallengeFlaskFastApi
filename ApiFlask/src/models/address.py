import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from src.models.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    cep = sa.Column(sa.String(8))
    number = sa.Column(sa.String)
    street = sa.Column(sa.String)
    neighborhood = sa.Column(sa.String)
    city = sa.Column(sa.String)
    state = sa.Column(sa.String)
    country = sa.Column(sa.String)

    user = relationship("User", back_populates="address", uselist=False)

    @validates("cep")
    def validate_cep(self, key, value):
        if not value.isdigit() or len(value) != 8:
            raise ValueError("CEP must contains exactly 8 digits")
        return value
