from src.dtos.user_address_dto import UserAddressDTO
from src.models.address import Address
from src.models.user import User
from src.repositories.user_address_repository import UserAddressRepository
from src.schemas.user_address_schema import UserAddressSchema


class UserAddressService:
    def __init__(self, user_address_repository: UserAddressRepository):
        self.user_address_repository = user_address_repository

    def create_user_address(self, user_address: UserAddressDTO) -> None:
        address = Address(
            cep=user_address.cep,
            number=user_address.numero,
            street=user_address.rua,
            neighborhood=user_address.bairro,
            city=user_address.cidade,
            state=user_address.estado,
            country=user_address.pais,
        )
        user = User(
            name=user_address.nome,
            preferred_name=user_address.nome_social,
            email=user_address.email,
            age=user_address.idade,
            occupation=user_address.profissao,
            address=address,
        )
        try:
            self.user_address_repository.create(user)
        except Exception as e:
            raise ValueError(f"Failed to create user address: {e}") from e
