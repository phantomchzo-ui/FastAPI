import pytest

from app.users.dao import UserDAO

@pytest.mark.parametrize("user_id, email", [
    (1, "kot@pes.com")

])
async def test_find_user_by_id(user_id, email):
    user = await UserDAO.find_by_id(user_id)

    assert user.email == email

