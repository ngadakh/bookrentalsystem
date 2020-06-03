# This module has Customer related routes

import flask
from flask import render_template

from brs import login_required, BRSModule
from brs.models import Customer, db

MODULE_NAME = 'customer'

book_blueprint = BRSModule(MODULE_NAME, __name__)


@book_blueprint.route('/customers/', methods=['GET'])
@login_required
def customer_listing():
    """
    This route is use to list the customers
    :return: render HTML page
    """
    customers = Customer.query.all()
    return render_template("/customers/list.html", customers=customers)


@book_blueprint.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    """
    This route is use to add a customer
    :return: render HTML page
    """
    if flask.request.method == 'GET':
        return render_template("/customers/add.html")
    if flask.request.method == 'POST':
        name = flask.request.form['name']
        email = flask.request.form['email']
        customer = Customer(name=name, email=email)
        db.session.add(customer)
        db.session.commit()

        customers = Customer.query.all()
        return render_template("/customers/list.html", customers=customers)
