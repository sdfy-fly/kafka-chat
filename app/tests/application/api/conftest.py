import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.api.main import create_app
from app.logic.init import init_container
from app.tests.fixtures import init_test_container


@pytest.fixture(scope='session')
def app() -> FastAPI:
    application = create_app()
    application.dependency_overrides[init_container] = init_test_container

    return application


@pytest.fixture(scope='session')
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
