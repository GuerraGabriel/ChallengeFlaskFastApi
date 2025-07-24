from dependency_injector import providers, containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.repositories.user_address_repository import UserAddressRepository
from src.services.user_address_service import UserAddressService
from src.controllers.user_controller import UserAddressController
from settings import settings


class Container(containers.DeclarativeContainer):
    sa_engine = providers.Singleton(create_engine, url=settings.DATABASE_URL)
    session_maker = providers.Singleton(sessionmaker, bind=sa_engine)
    session = providers.Factory(
        lambda session_maker: session_maker(), session_maker=session_maker
    )

    user_address_repository = providers.Factory(UserAddressRepository, session=session)
    user_address_service = providers.Singleton(
        UserAddressService, user_address_repository=user_address_repository
    )

    user_address_controller = providers.Singleton(
        UserAddressController, user_address_service=user_address_service
    )
