from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.params import Query
from dependency_injector.wiring import inject, Provide

from container import Container
from src.schemas.user_address_schema import UserAddressResponseSchema
from src.exceptions.external_service_exception import UnkownErrorFromExternalService
from src.services.user_address_service import UserAddressService

router = APIRouter()


@router.get(
    "/user-addresses", tags=["User Address"], response_model=UserAddressResponseSchema
)
@inject
async def get_user_address(
    user_address_service: Annotated[
        UserAddressService, Depends(Provide[Container.user_address_service])
    ],
):
    try:
        users = await user_address_service.get_users_addresses()
    except UnkownErrorFromExternalService as e:
        return {"error": str(e)}, 500

    if not users:
        return {"message": "No users found", "data": []}
    return {"message": "Users found", "data": users}
