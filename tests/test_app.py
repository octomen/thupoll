import requests


def test_ping(service):
    r = requests.get(service)
    assert r.ok, r.text
