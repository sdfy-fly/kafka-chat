import pytest
from punq import Container

from app.infra.repositories.chat import BaseChatRepository
from app.logic.mediator import Mediator
from app.tests.fixtures import init_test_container


@pytest.fixture()
def container() -> Container:
    return init_test_container()


@pytest.fixture()
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@pytest.fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
