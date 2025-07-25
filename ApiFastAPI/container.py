from dependency_injector import containers, providers
import httpx

from settings import Settings
from src.services.user_address_service import UserAddressService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.routes.user_address_route"])

    config = providers.Configuration()
    settings = providers.Singleton(Settings)

    httpx_client = providers.Resource(httpx.AsyncClient)

    user_address_service = providers.Factory(
        UserAddressService,
        http_client=httpx_client,
        external_source_url=providers.Callable(
            lambda settings: settings.external_source_url, settings
        ),
    )
