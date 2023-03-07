from school.models import ChromeBrowser
from school.dashboard.utils import enterDashboard, enterDashboardUPSite
from school.schedule.utils import *
from school.login.utils import *
from school.subjects.utils import fetchGroupData
from school.tools.utils import color, StudentNotFoundError, ScheduleExtractionError
from school.groups.utils import *
import traceback
import logging


def extractUP4USchedule(studentId: str, password: str) -> list[Subject]:
    '''Extracts the schedule of a student from the UP4U platform'''
    scheduleContent: list[Subject] = []

    # Try to get the student from the database
    try:
        student = Student.query.filter_by(studentID=studentId).first()
        if student:
            scheduleContent = getStudentSubjects(student)
        else:
            raise StudentNotFoundError
    except StudentNotFoundError as e:
        logging.warning(e.message)
        # Try to get the schedule from the UP4U platform
        try:
            with ChromeBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                login(browser, studentId, password)
                enterDashboard(browser)
                # fetchScheduleContent(browser)
                # scheduleContent = getStudentSubjects(Student.query.filter_by(studentID=session['student']['studentID']
                #                                                              ).first())
        except ScheduleExtractionError as e:
            logging.critical(e.message)
            scheduleContent = []
    return scheduleContent


def extractUPSiteSchedule(studentId: str, password: str) -> list[Group]:
    '''Extracts the schedule of a student from the UP site'''
    try:
        # Start the browser
        with ChromeBrowser().buildBrowser() as browser:
            # Go to the main page
            browser.get(
                "https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP&")
            # Login
            loginUPSite(browser, studentId, password)
            # Enter the dashboard
            enterDashboardUPSite(browser)
            # Get the schedule content
            groupData = fetchGroupData(browser)

            # get all group info

            data = [getGroup(group.id, 2) for group in groupData]

    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule extraction failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        data = []

    return data
