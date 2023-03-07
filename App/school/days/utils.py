from school import db
from school.models import Days
from school.tools.utils import color
import logging
import traceback


def getDays() -> list[Days]:
    '''Returns the days of the week stored in the database'''
    days = Days.query.all()
    if days:
        return days
    else:
        logging.warning(f'{color(3,"No days found in database")}')
        return []


def abreviatonToDay(abv: str) -> int:
    """Given an abbreviation, it returns the day name and its corresponding ID"""
    days = {
        'Lun': 1,
        'Mart': 2,
        'Miérc': 3,
        'Jue': 4,
        'V': 5,
        'S': 6,
        'D':  7
    }
    return days[abv]
