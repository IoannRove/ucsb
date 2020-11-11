from http import HTTPStatus


async def test_merge(api_client):
    payload = {'currencies': {'USD': 98.23, 'RUR': 1}}
    response = await api_client.post('/database?merge=1', data=payload)
    assert response.status == HTTPStatus.CREATED
    payload = {'currencies': {'EUR': 72}}
    response = await api_client.post('/database?merge=1', data=payload)
    assert response.status == HTTPStatus.CREATED

    response = await api_client.get('/convert?from=USD&to=RUR&amount=200')
    converted = await response.json()
    assert converted['data']['amount'] == 19646
    response = await api_client.get('/convert?from=EUR&to=RUR&amount=2')
    converted = await response.json()
    assert converted['data']['amount'] == 144


async def test_no_merge(api_client):
    payload = {'currencies': {'USD': 98.23, 'RUR': 1}}
    response = await api_client.post('/database?merge=0', data=payload)
    assert response.status == HTTPStatus.CREATED
    payload = {'currencies': {'EUR': 72}}
    response = await api_client.post('/database?merge=0', data=payload)
    assert response.status == HTTPStatus.CREATED

    response = await api_client.get('/convert?from=USD&to=EUR&amount=200')
    assert response.status == 404
