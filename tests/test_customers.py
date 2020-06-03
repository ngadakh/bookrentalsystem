from .conftest import test_data


def test_add_customer(client, auth):
    auth.login()

    response = client.post('/add_customer', data=test_data['customer']['add_customer'], follow_redirects=True)
    assert response.status_code == 200
    response_data = str(response.data.decode('utf-8'))
    assert test_data['customer']['add_customer']['name'] in response_data
    assert test_data['customer']['add_customer']['email'] in response_data


def test_customer_listing(client, auth):
    auth.login()

    response = client.get('/customers/', follow_redirects=True)
    assert response.status_code == 200
    response_data = str(response.data.decode('utf-8'))
    assert test_data['customer']['add_customer']['name'] in response_data
    assert test_data['customer']['add_customer']['email'] in response_data
