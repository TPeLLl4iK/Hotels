async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )

    print(response.json())

    assert response.status_code == 200


async def test_create_facilities(ac):

    response = await ac.post(
        '/facilities',
        json={
            'title': 'wi-fi'
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "Added"
    assert "data" in res
