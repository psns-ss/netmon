from app.core.config import settings
from app.tests.utils.machines import create_random_machine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient


def test_create_machine(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"host": "localhost:3000", "name": "my_machine"}
    response = client.post(
        f"{settings.API_V1_STR}/machines/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["host"] == data["host"]
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_machine(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    machine = create_random_machine(db)
    response = client.get(
        f"{settings.API_V1_STR}/machines/{machine.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content["host"] == machine.host
    assert content["name"] == machine.name
    assert content["id"] == machine.id
