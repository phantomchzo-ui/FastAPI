import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, name, password, status_code", [
    ("kot@pes.com", "Swaga", "ElamaN200409@", 200),
    ("kot@pes.com", "Swaga", "ElamaN200409@", 409)
])
async def test_register(email, name, password, status_code, ac: AsyncClient):
    response = await ac.post('/user/register', json={
        "email": email,
        "name": name,
        "hashed_password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "ElamaN200409@", 200),
])
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/user/login', json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


