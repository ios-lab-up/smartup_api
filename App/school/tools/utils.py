from flask import session
from contextlib import contextmanager
from datetime import datetime
from school import db
from school.models import Group
import psutil
import logging
import traceback


def server_status() -> str:
    '''
    Check if the server is up and running
    OK: memory usage < 80% and cpu usage < 80%
    SLOW: memory usage < 80% and cpu usage > 80%
    CRITICAL: memory usage > 80% and cpu usage > 80%
    '''
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



def schedulesOverlap(group_1: Group, group_2: Group) -> bool:
    '''
    Returns true in case they overlap in time and day else it returns false
    it takes into consideration the following criteria:
    - If the startTime or endTime of both groups somehow overlaps = True
    - If the startTime or endTime of one group is in between the startTime and endTime of the other group = True

    This criteria is applied for each day of the group, if its not achieved return True, else False
    '''
    try:
        # Get the schedules of each group
        group_1_schedules = group_1.schedule
        group_2_schedules = group_2.schedule

        # Iterate over each schedule in group 1
        for schedule_1 in group_1_schedules:
            # Iterate over each schedule in group 2
            for schedule_2 in group_2_schedules:
                # Check if the days are the same
                if schedule_1.day == schedule_2.day:
                    # Check if the times overlap
                    if (schedule_1.startTime <= schedule_2.endTime and schedule_1.endTime >= schedule_2.startTime):
                        return True

        # If no overlap was found, return False
        return False

    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule comparison failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        return False


def createCompatibleSchedules(groups: list[Group]) -> list[list[Group]]:
    '''
    Returns a list of lists containing groups whose schedules don't overlap given a list groups
    '''
    
    # Get the groups of the subject



# Then in your main function:


    compatible_schedules = []

    # Iterate over each group
    for i in range(len(groups)):
        compatible_group = [groups[i]]
        # Iterate over each other group
        for j in range(i + 1, len(groups)):
            # Check if the schedules of the two groups overlap
            if not schedulesOverlap(groups[i], groups[j]):
                compatible_group.append(groups[j])


        # Add the compatible group to the list of compatible schedules
        compatible_schedules.append(compatible_group)
        print(compatible_schedules)

    return compatible_schedules
