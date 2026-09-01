import pytest


@pytest.mark.parametrize('login, password, status_code', [
    ('ivan_petrov', 'strongpassword123', 200),
    ('ivan_petrov', 'strongpassword123', 400),
    ('admin', 'adminpass456', 200)
])
async def test_register_flow(
        login: str, 
        password: str,
        status_code: int,
        ac
):
    
    response_register = await ac.post(
        "/auth/register",
        json={
            "login": login,
            "password": password,
        },
    )

    assert response_register.status_code == status_code
    if status_code != 200:
        return

    response_login = await ac.post(
        "/auth/login",
        json={
            "login": login,
            "password": password,
        },
    )

    assert response_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    response_me = await ac.get(
        "/auth/me",
    )

    # /me
    user = response_me.json()
    assert response_me.status_code == status_code
    assert login == user["login"]
    assert "password" not in user
    assert "hashed_password" not in user

    response_logout = await ac.post(
        "/auth/logout",
    )

    # logout
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies
