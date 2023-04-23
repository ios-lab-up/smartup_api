from school.models import ChromeBrowser
from school.dashboard.utils import enterDashboard, enterUPSiteSubjects
from school.schedule.utils import *
from school.login.utils import *
from school.subjects.utils import fetchGroupData
from school.user.utils import getUser
from school.tools.utils import color, UserNotFoundError, ScheduleExtractionError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def extractUPSiteSchedule(studentId: str, password: str) -> list[Group]:
    '''Extracts the schedule of a user from the UP site'''
    data = []
    try:
        # Start the browser
        with ChromeBrowser().buildBrowser() as browser:
            # Go to the main page
            browser.get(
                "https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP&")
            
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                ( By.XPATH, "//input[@name='userid' and @id='userid']"))
        )

            

            # Login
            if loginUPSite(browser, studentId, password):
            # Enter the dashboard
                enterUPSiteSubjects(browser)

                data = fetchGroupData(browser)
            else:
                logging.error(f'{color(1,"Login failed")} ❌')
                data = []
            # Get the schedule content


    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule extraction failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        data = []

    return data


