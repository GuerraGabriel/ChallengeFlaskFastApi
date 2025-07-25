from container import Container
from src.models.address import Address
from src.models.user import User
from src.models.base import Base
from src.repositories.user_address_repository import UserAddressRepository


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def repository(session):
    return UserAddressRepository(session)


def test_create_user(repository):
    user = User(
        name="John Doe",
        preferred_name="Johnny",
        email="john@example.com",
        age=30,
        occupation="Engineer",
    )

    repository.create(user)
    result = repository.get_by_email("john@example.com")

    assert result.email == "john@example.com"
    assert result.name == "John Doe"


def test_get_by_email_not_found(repository):
    with pytest.raises(ValueError, match="User not found"):
        repository.get_by_email("notfound@example.com")


def test_update_user(repository):
    user = User(
        name="Jane Doe",
        preferred_name="Janie",
        email="jane@example.com",
        age=25,
        occupation="Designer",
    )
    repository.create(user)

    rows = repository.update(user.id, {"name": "Jane Smith"})
    assert rows == 1

    updated_user = repository.get_by_email("jane@example.com")
    assert updated_user.name == "Jane Smith"


def test_delete_user(repository):
    user = User(
        name="Mark Spencer",
        preferred_name="Mark",
        email="mark@example.com",
        age=40,
        occupation="Manager",
    )
    repository.create(user)

    repository.delete(user.id)

    with pytest.raises(ValueError):
        repository.get_by_email("mark@example.com")


def test_delete_user_not_found(repository):
    with pytest.raises(ValueError, match="User not found"):
        repository.delete(999)


def test_get_users_paginated(repository):
    user1 = User(
        name="Alice",
        preferred_name="Ali",
        email="alice@example.com",
        age=28,
        occupation="Analyst",
        address=Address(
            cep="00000000",
            number=123,
            street="rua",
            neighborhood="bairro",
            city="cidade",
            state="estado",
            country="pais",
        ),
    )
    user2 = User(
        name="Bob",
        preferred_name="Bobby",
        email="bob@example.com",
        age=32,
        occupation="Dev",
        address=Address(
            cep="00000000",
            number=123,
            street="rua",
            neighborhood="bairro",
            city="cidade",
            state="estado",
            country="pais",
        ),
    )
    repository.create(user1)
    repository.create(user2)

    users, total_pages = repository.get_users_paginated(page_size=2, page_number=1)
    assert len(users) == 2
    assert users[0] == user1
    assert users[1] == user2
    assert total_pages == 1