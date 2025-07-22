from dependency_injector import providers, containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


class Container(containers.DeclarativeContainer):
    sa_engine = providers.Singleton(create_engine, url=settings.DATABASE_URL)
    sa_session = providers.Singleton(sessionmaker, bind=sa_engine)
