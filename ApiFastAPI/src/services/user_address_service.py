from typing import List, Tuple
from src.exceptions.external_service_exception import UnkownErrorFromExternalService
from src.schemas.user_address_schema import UserAddressExternalSchema
import httpx


class UserAddressService:

    def __init__(self, http_client: httpx.AsyncClient, external_source_url: str):
        self.http_client = http_client
        self.external_source_url = external_source_url

    async def get_users_addresses(self) -> list[UserAddressExternalSchema]:
        page_size = 100
        current_page = 1

        first_page, total_pages = await self._get_users_from_external_service(
            page_size=page_size,
            page_number=current_page,
        )

        all_users = first_page

        if total_pages == 1:
            return all_users

        # TODO: Use semaphore and TaskGroup to better perfomance
        for page in range(2, total_pages +1 ):
            page_data, _ = await self._get_users_from_external_service(
                page_size=page_size,
                page_number=page,
            )
            all_users.extend(page_data)

        return all_users

    async def _get_users_from_external_service(
        self,
        page_size: int,
        page_number: int,
    ) -> Tuple[List[UserAddressExternalSchema], int]:
        # TODO : create external service isolated for external reference
        try:
            response = await self.http_client.get(
                self.external_source_url,
                params={
                    "page_size": page_size,
                    "page_number": page_number,
                },
                timeout=5,
            )
        except httpx.TimeoutException as e:
            raise e
        except Exception as e:
            raise UnkownErrorFromExternalService(
                "An error occurred while fetching data from the external service. Please try again later."
            ) from e
        response.raise_for_status()
        response_json = response.json()

        total_pages = response_json["pagination"]["total_pages"]
        users_addresses = [UserAddressExternalSchema(**user) for user in response_json["data"]]

        return users_addresses, total_pages
