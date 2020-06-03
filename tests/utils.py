from brs.models import Book, Customer, db
from .conftest import test_data


def add_book():
    book = Book(name=test_data['book']['reserve_book']['name'], author=test_data['book']['reserve_book']['author'],
                quantity=test_data['book']['reserve_book']['quantity'])
    db.session.add(book)
    db.session.commit()

    return book.serial_no


def add_customer():
    customer = Customer(name=test_data['customer']['add_customer']['name'],
                        email=test_data['customer']['add_customer']['email'])
    db.session.add(customer)
    db.session.commit()

    return customer.id


def delete_customer(customer_id):
    db.session.query(Customer).filter(Customer.id == customer_id).delete()
    db.session.commit()
