

def test__login__200_when_auth(client, token):
    r = client.get('/login', query_string={'token': token.value})
    assert r.status_code == 200
    result = r.get_json()
    assert result.get('Authentication')


def test__login__401_when_incorrect_token(client):
    r = client.get('/login', query_string={'token': 'some_incorrect_token'})
    assert r.status_code == 401


def test__login__401_when_no_params(client):
    r = client.get('/login')
    assert r.status_code == 401
