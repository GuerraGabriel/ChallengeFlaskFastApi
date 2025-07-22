from dependency_injector import providers, containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.controllers.user_controller import UserAddressController
from settings import settings


class Container(containers.DeclarativeContainer):
    sa_engine = providers.Singleton(create_engine, url=settings.DATABASE_URL)
    sa_session = providers.Singleton(sessionmaker, bind=sa_engine)

    user_address_controller = providers.Singleton(UserAddressController)
