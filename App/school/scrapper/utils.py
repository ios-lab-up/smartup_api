from school.models import ChromeBrowser
from school.dashboard.utils import enterDashboard, enterUPSiteSubjects
from school.schedule.utils import *
from school.login.utils import *
from school.subjects.utils import fetchGroupData
from school.user.utils import getUser
from school.tools.utils import color, UserNotFoundError, ScheduleExtractionError
from school.groups.utils import *
from school.user.utils import createUser
from school.security import *
from flask import session
import traceback
import logging


def extractUP4UContent(studentId: str, password: str) -> User:
    '''Extracts the schedule of a user from the UP4U platform'''
    scheduleContent: list[Subject] = []

    # Try to get the user from the database
    try:
        user = User.query.filter_by(userID=studentId).first()
        if user:
            scheduleContent = getUser(user.id, 2)
        else:
            raise UserNotFoundError
    except UserNotFoundError as e:
        logging.warning(e.message)
        # Try to get the schedule from the UP4U platform
        try:
            with ChromeBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                login(browser, studentId, password)
                user = createUser(
                    **session['user'], name=enterDashboard(browser))

                # fetchScheduleContent(browser)
                scheduleContent = getUser(user.id, 2)
        except ScheduleExtractionError as e:
            logging.critical(e.message)
            scheduleContent = []
    return scheduleContent


def extractUPSiteSchedule(studentId: str, password: str, maxtries: int = 3) -> list[Group]:
    '''Extracts the schedule of a user from the UP site if it fails, try again (up to 3 times)'''
    try:
        # Start the browser
        with ChromeBrowser().buildBrowser() as browser:
            # Go to the main page
            browser.get(
                "https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP&")
            # Login
            loginUPSite(browser, studentId, password)
            # Enter the dashboard
            enterUPSiteSubjects(browser)
            # Get the schedule content
            groupData = fetchGroupData(browser)

            # get all group info

            data = [getGroup(group.id, 2) for group in groupData]

    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule extraction failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')

        if maxtries > 0:
            logging.warning(
                f'{color(5,"Trying again...")} 🔄 {color(5,maxtries)} attempts left')
            return extractUPSiteSchedule(studentId, password, maxtries-1)
        else:
            logging.critical(f'{color(5,"Schedule extraction failed")} ❌')
            data = []

    return data
