# Utility file for book module

import datetime

from brs.models import Settings


def calculate_book_rent(issue_date):
    """
    This function use to calculate book rent
    :param issue_date: issue date / datetime object
    :return: rent amount / integer
    """
    days_duration = get_duration(issue_date)
    amount = get_rental_settings()
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
        days_duration = 1

    return days_duration


def get_rental_settings():
    """
    This function is use to get current rent amount from the settings table
    :return: rent_charges / integer
    """
    rent_charges = Settings.query.all()
    if len(rent_charges) > 0:
        rent_charges = rent_charges[0].book_rental_charges
    if not rent_charges:
        rent_charges = 0
    return rent_charges
