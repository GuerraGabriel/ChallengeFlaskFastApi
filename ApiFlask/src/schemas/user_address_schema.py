import marshmallow_dataclass

from src.dtos.user_address_dto import UserAddressDTO

UserAddressSchema = marshmallow_dataclass.class_schema(UserAddressDTO)()
