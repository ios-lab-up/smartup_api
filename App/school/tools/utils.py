from flask import session
from contextlib import contextmanager
from datetime import datetime
from .. import db
import psutil


def server_status() -> str:
    """
    Check if the server is up and running
    OK: memory usage < 80% and cpu usage < 80%
    SLOW: memory usage < 80% and cpu usage > 80%
    CRITICAL: memory usage > 80% and cpu usage > 80%
    """
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    status = ""
    if memory.percent < 80 and cpu < 80:
        status = "OK"
    elif memory.percent < 80 and cpu > 80:
        status = "SLOW"
    else:
        status = "CRITICAL"
    return status

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



def color(color: int, text: str) -> str:
    '''
    1: Red
    2: Green
    3: Yellow
    4: Blue
    5: Purple
    6: Cyan
    '''

    match color:
        case 1:
            return f"\033[1;31;40m{text}\033[0m"
        case 2:
            return f"\033[1;32;40m{text}\033[0m"
        case 3:
            return f"\033[1;33;40m{text}\033[0m"
        case 4:
            return f"\033[1;34;40m{text}\033[0m"
        case 5:
            return f"\033[1;35;40m{text}\033[0m"
        case 6:
            return f"\033[1;36;40m{text}\033[0m"
        case _:
            raise ValueError("Invalid color")


def deleteUserSession() -> None:
    '''Deletes the user session'''
    session.pop('user', None)
    session.pop('logged_in', None)


def writeHTMLFile(rows: list) -> None:
    with open('App/school/dashboard/upsite.html', 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n")
        source_codes = [row.get_attribute('innerHTML') for row in rows]
        f.write('\n'.join(source_codes))
        f.write("\n</body>\n</html>")


def parseTime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, '%A %I:%M%p - %I:%M%p')

class UserNotFoundError(Exception):
    """Error raised when user not found in DB"""

    def __init__(self, message=None) -> str:
        self.message: str = f'{color(3,"User not found in DB, creating profile...")} 🔍' if message is None else message


class ScheduleExtractionError(Exception):
    """Error raised when the schedule extraction from UP4U platform fails"""

    def __init__(self, message=None) -> str:
        self.message: str = f'{color(5,"Schedule extraction failed")} 🔍' if message is None else message

class WrongCredentialsError(Exception):
    '''Error raised when the user enters wrong credentials'''

    def __init__(self, message=None) -> None:
        self.message: str = f'{color(5,"Wrong User Credentials")} 🔍' if message is None else message

