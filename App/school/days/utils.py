from ..models import Days
from ..tools.utils import color
import logging


def get_days() -> list[Days]:
    """Returns the days of the week stored in the database"""
    days = Days.query.all()
    if days:
        return days
    else:
        logging.warning(f'{color(3,"No days found in database")}')
        return []


def abbreviation_to_day(abv: str) -> int:
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
