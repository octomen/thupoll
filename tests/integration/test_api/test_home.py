def test_ping(client):
    r = client.get('/ping')
    assert r.status_code == 200, r.context
    assert r.data == b'pong'
