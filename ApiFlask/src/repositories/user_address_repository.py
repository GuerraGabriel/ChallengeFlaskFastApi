from typing import List
from src.models.user import User
from sqlalchemy.orm import Session


class UserAddressRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, user_data: User) -> None:
        self.session.add(user_data)
        self.session.commit()

    def get_by_email(self, email: str) -> User:
        result = self.session.query(User).filter_by(email=email).first()
        if not result:
            raise ValueError("User not found")

        return result

    def update(self, user_id: int, updated_data: dict) -> int:
        rows_affected = self.session.query(User).filter_by(id=user_id).update(updated_data)
        self.session.commit()
        return rows_affected

    def delete(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("User not found")

        self.session.delete(user)
        self.session.commit()

    def list(self) -> List[User]:
        return self.session.query(User).all()
