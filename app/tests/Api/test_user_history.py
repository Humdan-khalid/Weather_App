from app.services.user_history import get_user_history
from unittest.mock import patch, AsyncMock
from app.tests.Services.test_history import user_history
from app.core.exceptions import InvalidCredentials, HistoryNotFound
from app.core.jwt import user_token
from app.main import app

def fake_user():
    return {
        "id": 4,
        "email": "hamdan@gmail.com"
    }

async def test_server_error(client):
    app.dependency_overrides[user_token] = fake_user
    with patch(
        "app.services.user_history.get_user_history",
        new = AsyncMock( 
            side_effect = InvalidCredentials(
                "Internal Server error"
            )
        ) 
    ):
        response = client.get(
            "/user-history"
        )
        assert response.status_code == 401

    app.dependency_overrides.clear()

async def test_history_not_found(client):
    app.dependency_overrides[user_token] = fake_user

    with patch(
        "app.api.history.user_history.get_user_history",
        new = AsyncMock(
            side_effect = HistoryNotFound(
                "user history not found!"
            )
        )
    ):
        response = client.get(
            "/user-history"
        )

        assert response.status_code == 404
        app.dependency_overrides.clear()


async def test_history_successfully_found(client):
    app.dependency_overrides[user_token] = fake_user

    with patch(
        "app.api.history.user_history.get_user_history",
        new = AsyncMock(
            return_value = None
    )
    ):
        response = client.get(
            "user-history"
        )

        assert response.status_code == 200
        app.dependency_overrides.clear()