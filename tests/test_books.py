from . import utils
from .conftest import test_data


def test_add_book(client, auth):
    auth.login()

    response = client.post('/add_new_book', data=test_data['book']['add_book'], follow_redirects=True)
    assert response.status_code == 200
    assert b'TEST BOOK' in response.data
    assert b'TEST AUTHOR' in response.data


def test_book_listing(client, auth):
    auth.login()

    response = client.get('/books/', follow_redirects=True)
    assert response.status_code == 200
    assert b'TEST BOOK' in response.data
    assert b'TEST AUTHOR' in response.data


def test_reserve_book(client, auth):
    auth.login()

    book_serial_no = utils.add_book()
    customer_id = utils.add_customer()

    data = {'book_serial_no': book_serial_no, 'customer_id': customer_id}
    response = client.post('/reserve_book', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Book reserved successfully.' in response.data

    # utils.delete_book(book_serial_no)
    utils.delete_customer(customer_id)
