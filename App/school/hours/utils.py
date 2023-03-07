from school import db
from school.models import Hours
from school.tools.utils import color
import logging
import traceback


def getHours() -> list[Hours]:
    '''Returns the hours of the day stored in the database'''
    hours = Hours.query.all()
    if hours:
        return hours
    else:
        logging.warning(f'{color(3,"No hours found in database")}')
        return []
