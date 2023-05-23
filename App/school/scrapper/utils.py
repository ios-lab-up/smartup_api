from school.models import ChromeBrowser
from school.dashboard.utils import  enterUPSiteSubjects
from school.schedule.utils import *
from school.login.utils import *
from school.subjects.utils import fetchGroupData
from school.tools.utils import color, WrongCredentialsError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from school.groups.utils import *
from school.user.utils import createUser, getUser
from school.security import *
from flask import session
from flask_bcrypt  import check_password_hash
import traceback
import logging


def extractUP4UContent(studentId: str, password: str) -> User:
    '''Extracts the schedule of a user from the UP4U platform'''

    try:
        user_data = {
            'schedule': [],
            'grades': [],
        }

        user = User.query.filter_by(userID=studentId).first()
        if not user:
            with ChromeBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                loginUP4U(browser, studentId, password)
                user = createUser(**session['user'])
                user_data['schedule'] = fetch_schedule_content(browser) #TODO: Create a relation table user-group
                user_data['grades'] = fetch_grades_content(browser) #TODO: Create a junction table user-group-grade-parcial
                user = getUser(user.id, 2)
                user['jwt_token'] = encodeJwtToken(user)

                # Código de mau:

                user, message, status_code, error = user, f'User: {user["userID"]} was succesfully created', 201, None

        else:
            if check_password_hash(user.password, password):
                user = getUser(user.id, 2)
                user['jwt_token'] = encodeJwtToken(user)
                message, status_code, error = f'User: {user["userID"]} was succesfully logged in', 200, None
            else:
                user, message, status_code, error  = {}, "Wrong Credentials!", 401, "Unauthorized"
    except WrongCredentialsError as e:
        logging.warning(e.message)
        user, message, status_code, error ={}, 'Wrong credentials or user creation failed', 401, e.message

    return user, message, status_code, error


        
    






    # # Try to get the user from the database
    # try:
    #     user = User.query.filter_by(userID=studentId).first()
    #     if user:
    #         scheduleContent = getUser(user.id, 2)
    #     else:
    #         raise UserNotFoundError
    # except UserNotFoundError as e:
    #     logging.warning(e.message)
    #     # Try to get the schedule from the UP4U platform
    #     try:
    #         with ChromeBrowser().buildBrowser() as browser:
    #             browser.get("https://up4u.up.edu.mx/user/auth/login")
    #             login(browser, studentId, password)
    #             user = createUser(
                    # **session['user'], name=enterDashboard(browser))

    #             # fetchScheduleContent(browser)
    #             scheduleContent = getUser(user.id, 2)
    #     except ScheduleExtractionError as e:
    #         logging.critical(e.message)
    #         scheduleContent = []
    # return scheduleContent


def extractUPSiteContent(studentId: str, password: str) -> bool:
    '''Extracts the schedule of a user from the UP site'''
    try:
        # Start the browser
        with ChromeBrowser().buildBrowser() as browser:
            # Go to the main page
            browser.get("https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP&")
            
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(( By.XPATH, "//input[@name='userid' and @id='userid']")))
        
            # Login
            loginUPSite(browser, studentId, password)
            # Enter the dashboard
            enterUPSiteSubjects(browser)

            fetchGroupData(browser)
            # Get the schedule content
            return True


    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule extraction failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        return False



