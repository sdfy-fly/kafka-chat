import pytest
from faker import Faker
from fastapi import FastAPI, status
from httpx import Response
from starlette.testclient import TestClient


class TestChat:

    @pytest.mark.asyncio
    async def test_create_chat_success(self, app: FastAPI, client: TestClient, faker: Faker):
        url = app.url_path_for('create_chat_route')
        title = faker.text(max_nb_chars=30)

        response: Response = client.post(url=url, json={'title': title})
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data['title'] == title

    @pytest.mark.asyncio
    async def test_create_chat_title_too_long(self, app: FastAPI, client: TestClient, faker: Faker):
        url = app.url_path_for('create_chat_route')
        title = faker.text(max_nb_chars=300)

        response: Response = client.post(url=url, json={'title': title})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create_chat_empty_title(self, app: FastAPI, client: TestClient, faker: Faker):
        url = app.url_path_for('create_chat_route')
        response: Response = client.post(url=url, json={'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
