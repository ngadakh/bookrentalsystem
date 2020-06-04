# Utility file for book module

import datetime
import json

from brs.models import Settings


def calculate_book_rent(issue_date, book_type):
    """
    This function use to calculate book rent
    :param issue_date: issue date / datetime object
    :return: rent amount / integer
    """
    days_duration = get_duration(issue_date)
    amount = get_rental_settings()[book_type]

    if book_type == 'Regular':
        if days_duration < 2:
            amount = 2
            rent_amount = days_duration * amount
        else:
            days_duration = days_duration - 2
            amount = days_duration * amount
            # For first 2 days charge will be Rs. 1
            rent_amount = amount + 1
    elif book_type == 'Novel':
        if days_duration < 3:
            amount = 4.5
            rent_amount = days_duration * amount
        else:
            rent_amount = days_duration * amount
    else:
        rent_amount = days_duration * amount

    return rent_amount


def get_duration(issue_date):
    """
    This function use to calculate duration between issue date and return date
    :param issue_date: issue date / datetime object
    :return: duration in days / integer
    """
    return_date = datetime.datetime.now().date()
    duration = return_date - issue_date.date()
    days_duration = duration.days

    # Check if days == 0
    # Assume - if customer return the book on the same day we will charge him for one day duration
    if days_duration == 0:
        days_duration = 1
    else:
        days_duration += 1

    return days_duration


def get_rental_settings():
    """
    This function is use to get current rent amount from the settings table
    :return: rent_charges / integer
    """
    rent_charges = Settings.query.all()
    rent_charges = json.loads(rent_charges[0].book_rental_charges)[0]['types']
    return rent_charges
