# Book Rental Store - Models

import datetime
import json

from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


class Book(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    book_type = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "<Name of Book: {}>".format(self.name)

#
# class BookTypes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     types = db.Column(db.String(100), unique=True, nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<Name of Customer: {}>".format(self.name)


class ReserveBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.serial_no'), nullable=False)
    book = relationship("Book", backref=backref("book"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer", backref=backref("customer"))
    issue_date = db.Column(db.DateTime, default=datetime.datetime.now())


class ReturnBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.serial_no'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    issue_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, default=datetime.datetime.now())
    rent_amount = db.Column(db.Integer)


class BookHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_reserve_id = db.Column(db.Integer, db.ForeignKey('reserve_book.id'), nullable=False)
    return_date = db.Column(db.DateTime, default=datetime.datetime.now())
    rent_amount = db.Column(db.Integer)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_rental_charges = db.Column(db.String(120), unique=True, nullable=False)

#
# @event.listens_for(BookTypes.__table__, 'after_create')
# def insert_initial_values(*args, **kwargs):
#     db.session.add(BookTypes(types=json.dumps([{"types": ["Regular", "Fiction", "Novel"]}])))
#     db.session.commit()


@event.listens_for(Settings.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Settings(book_rental_charges=json.dumps([{"types": {"Regular": 1.5, "Fiction": 3, "Novel": 1.5}}])))
    db.session.commit()
