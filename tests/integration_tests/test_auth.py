from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {'user_id': 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    pay_load = AuthService().decode_token(jwt_token)
    assert pay_load
    assert pay_load['user_id'] == data['user_id']