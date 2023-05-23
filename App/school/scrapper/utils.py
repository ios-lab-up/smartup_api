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
from bs4 import BeautifulSoup


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

                # Scrap the grades from the user grades
                soup = BeautifulSoup(user_data['grades'], 'html.parser')
                rows = soup.select('#contenido-tabla .row')
                grades = []
                for row in rows:
                    # Create a list to store the current info
                    current_info = {}

                    # We search for the columns in the current row by class
                    # There could be an empty row, so we check if the row has columns
                    cols = row.find_all('div', class_='col-md-2')
                    class_num = cols[0].text.strip() if cols else None

                    cols = row.find_all('div', class_='col-md-1')
                    grade = [col.text.strip() for col in cols][0:3]

                    current_info[class_num] = grade
                    grades.append(current_info)
                
                #Scrap the schedule from the user schedule
                soup = BeautifulSoup(user_data['schedule'], 'html.parser')
                rows = soup.select('#contenido-tabla .row')
                groups = []
                for row in rows:
                    cols = row.find_all('div', class_='col-md-1')
                    class_num = cols[0].text.strip() if cols else None
                    groups.append(class_num)
                groups = list(set(groups))

                # At this point we have the grades and the groups of the user

                message, status_code, error = f'User: {user.userID} was succesfully created', 201, None

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


