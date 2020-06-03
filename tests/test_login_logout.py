def test_login(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Books Section' in response.data
    assert b'Customer Section' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data


def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'login page' in response.data
    assert b'Book Rental Store' in response.data
    assert b'Please login' in response.data
