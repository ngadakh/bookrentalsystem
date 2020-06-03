# This module has Book related routes

import datetime

import flask
from dateutil import parser
from flask import render_template, jsonify, request, redirect, url_for

from brs import login_required, BRSModule
from brs.models import db, Book, Customer, Settings, ReserveBook, ReturnBook
from .utils import calculate_book_rent, get_rental_settings, get_duration

MODULE_NAME = 'book'

book_blueprint = BRSModule(MODULE_NAME, __name__)


@book_blueprint.route('/books/', methods=['GET', 'POST'])
@login_required
def book_listing():
    """
    This route get the book listing from Book model.
    :return: render HTML page
    """
    message = flask.request.args.get('message', None)
    books = Book.query.filter(Book.quantity > 0).all()
    if books and len(books) < 1:
        return render_template('/books/list.html', error="No books found!")

    return render_template("/books/list.html", books=books, message=message)


@book_blueprint.route('/add_new_book', methods=['GET', 'POST'])
@login_required
def add_new_book():
    """
    This route use to add new book
    :return: render book listing HTML page after adding the book
    """
    if flask.request.method == 'GET':
        return render_template("/books/add.html")
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        author = flask.request.form['author']
        quantity = flask.request.form['quantity']
        book = Book(name=name, author=author, quantity=quantity)
        db.session.add(book)
        db.session.commit()

        books = Book.query.all()
        return render_template("/books/list.html", books=books)


@book_blueprint.route('/reserve_book', methods=['GET', 'POST'])
@login_required
def reserve_book():
    """
    This route is use to reserve book, it uses book serial no and customer id to reserve book
    :return: render HTML page for reserve book / book listing
    """
    if flask.request.method == 'GET':
        books = Book.query.all()
        customers = Customer.query.all()
        return render_template("/books/reserve_book.html", books=books, customers=customers)
    if flask.request.method == 'POST':
        book_serial_no = int(flask.request.form['book_serial_no'])
        customer_id = int(flask.request.form['customer_id'])

        # Check if book is already reserved
        res_book = ReserveBook.query.filter_by(book_id=book_serial_no, customer_id=customer_id).all()
        if len(res_book) > 0:
            message = "This book is already reserved."
        else:
            # Reserve Book
            res_book = ReserveBook(book_id=book_serial_no, customer_id=customer_id)
            db.session.add(res_book)
            db.session.commit()
            message = "Book reserved successfully."

            # Decrease the book quantity from store
            book = Book.query.filter_by(serial_no=book_serial_no).first()
            book.quantity = book.quantity - 1
            db.session.commit()

        return redirect(url_for("book.book_listing", message=message))


@book_blueprint.route('/return_book', methods=['GET', 'POST'])
@login_required
def return_book():
    """
     This route is use to return a book, it uses book serial no and customer id to reserve book
    :return: render HTML page for return book / book listing
    """
    if flask.request.method == 'GET':
        message = flask.request.args.get('message', None)
        books = ReserveBook.query.join(Book).all()
        for book in books:
            rent_amount = calculate_book_rent(book.issue_date)
            book.rent_amount = rent_amount
        return render_template("/books/return_book.html", books=books, message=message)
    if flask.request.method == 'POST':
        book_serial_no = int(flask.request.form['book_serial_no'])
        customer_id = int(flask.request.form['customer_id'])
        issue_date = parser.parse(flask.request.form['issue_date'])
        rent_amt = int(flask.request.form['amount'])

        # Add record to ReturnBook table
        res_book = ReturnBook(book_id=book_serial_no, customer_id=customer_id, issue_date=issue_date,
                              return_date=datetime.datetime.now(),
                              rent_amount=rent_amt)
        db.session.add(res_book)
        db.session.commit()

        # Remove book from ReserveBook as it's successfully returned
        db.session.query(ReserveBook).filter(ReserveBook.book_id == book_serial_no,
                                             ReserveBook.customer_id == customer_id).delete()
        db.session.commit()

        # Increase the book quantity in the store as book is returned
        book = Book.query.filter_by(serial_no=book_serial_no).first()
        book.quantity = book.quantity + 1
        db.session.commit()

        return jsonify("SUCCESS")


@book_blueprint.route('/get_book_rental_and_issue_date', methods=['GET'])
@login_required
def get_book_rental_and_issue_date():
    """
    This route is use to get book rental and issue date for book
    :return: JSON response to front end with issue date and rent amount
    """
    if flask.request.method == 'GET':
        book_serial_no = int(flask.request.args['book_serial_no'])
        customer_id = int(flask.request.args['customer_id'])

        reserv_book = ReserveBook.query.filter_by(book_id=book_serial_no, customer_id=customer_id).first()
        issue_date, rent_amount = calculate_book_rent(reserv_book)

        return jsonify(issue_date, rent_amount)


@book_blueprint.route('/get_book_history', methods=['GET'])
@login_required
def get_book_history():
    """
    This route is use to get reserve book history
    :return: render HTML page
    """
    if flask.request.method == 'GET':
        res_books = ReserveBook.query.join(Book, Customer).all()
        return render_template("/books/reserved_book_history.html", books=res_books)


@book_blueprint.route('/get_rent_statement', methods=['GET', 'POST'])
@login_required
def get_rent_statement():
    """
    This route is use to get rent statement for a customer
    :return: render HTML page for statement report
    """
    if flask.request.method == 'GET':
        customers = Customer.query.all()
        return render_template("/books/rent_statement.html", customers=customers)
    if flask.request.method == 'POST':
        customer_id = int(flask.request.form['customer_id'])
        books = ReserveBook.query.filter_by(customer_id=customer_id).all()
        total_rent_amount = 0
        for book in books:
            book.duration = get_duration(book.issue_date)
            book.rent_amount = calculate_book_rent(book.issue_date)
            total_rent_amount += book.rent_amount
        return render_template("/customers/report.html", books=books, total_rent_amount=total_rent_amount,
                               now_date=datetime.datetime.now())


@book_blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    This route is use to set the settings for rent amount
    :return: render/ redirect HTML page
    """
    if flask.request.method == 'GET':
        message = flask.request.args.get('message', None)
        rent = get_rental_settings()
        return render_template("/books/settings.html", settings=rent, message=message)
    if flask.request.method == 'POST':
        rent = flask.request.form['rent']
        setting = Settings.query.all()
        if len(setting) > 0:
            setting[0].book_rental_charges = rent
        else:
            setting = Settings(book_rental_charges=rent)
            db.session.add(setting)
        db.session.commit()

        return redirect(url_for("book.settings", message="Rent setting saved successfully"))
