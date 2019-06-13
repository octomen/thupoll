

def test__delete__401_when_no_auth_headers(client):
    r = client.delete('/themes/1')
    assert r.status_code == 401, r.get_json()


def test__delete__401_when_incorrect_auth(client, faker):
    r = client.delete('/themes/1', headers={
        'Authentication': 'some_incorrect_token'})
    assert r.status_code == 401, r.get_json()

# TODO
# def test__delete__403_when_incorrect_role(client, faker):
#     r = client.delete('/themes/1', headers={
#         'Authentication': 'some_incorrect_token'})
#     assert r.status_code == 401, r.get_json()
