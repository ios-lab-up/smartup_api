from school.user.utils import createUser
from school.login.utils import *
from school.models import ChromeBrowser
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from school.tools.utils import color
from selenium.webdriver.common.keys import Keys

from school.security import *
import logging
import traceback
import time
from bs4 import BeautifulSoup


def enterDashboard(browser: ChromeBrowser) -> str:
    '''Extracts the schedule link from the main page'''
    try:
        try:
            userName = browser.find_element(
                By.XPATH, "//div[@class='user-title pull-left hidden-xs']").find_element(By.XPATH, "//strong").text

        except NoSuchElementException:
            logging.error(
                f'{color(1,"Couldnt create user")} ❌ {traceback.format_exc().splitlines()[-3]}')

        # browser.find_element(By.LINK_TEXT, "Horarios").click()
        # time.sleep(3)
        # logging.info(f'{color(2,"Loading schedule...")} ✅')
    except NoSuchElementException:
        logging.error(f'{color(1,"Schedule link not found")} ❌')

    return userName


def enterUPSiteSubjects(browser) -> str:
    '''Fetches the subjects from the UPSite page'''
        # sleep 10 seconds and print it

    browser.get(
        "https://upsite.up.edu.mx/psp/CAMPUS/EMPLOYEE/SA/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL")
    logging.info(
        f'{color(2,"Enter Carrito de Inscripción...")} ✅')
    # print the html
    
    browser.switch_to.frame(0)

    # button = browser.find_element(By.ID, "DERIVED_SSS_SCT_SSS_TERM_LINK")
    if WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "DERIVED_SSS_SCT_SSS_TERM_LINK"))):
        button = browser.find_element(By.ID, "DERIVED_SSS_SCT_SSS_TERM_LINK")
        button.click()
        print("Element clicked")
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "SSR_DUMMY_RECV1")))
        button= browser.find_element(By.ID, "SSR_DUMMY_RECV1$sels$1$$0")
        button.click()
        print("Element 2 clicked")
        continue_button = browser.find_element(By.XPATH, '//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]')
        continue_button.click()
        sleep(2)
        buscar_button = browser.find_element(By.XPATH, '//*[@id="DERIVED_REGFRM1_SSR_PB_SRCH"]')
        buscar_button.click()
        sleep(2)
    else:
        print(False)

    # browser.find_element(By.ID, "DERIVED_SSS_SCT_SSR_PB_GO").click()
        '''
        #ADDITION --------------------------------------
        dropdown =browser.find_elements(by=By.TAG_NAME, value="Option")
        for element in dropdown:
            if element.text == "Otoño 2023":
                element.click()
                break
        browser.switch_to.default_content()
        #ADDITION --------------------------------------
        '''

        # Switch to the first frame

    #     # Click on the element
    #     dropdown = WebDriverWait(c, 10).until(
    # EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_STRM$35$"))
    #     )

    #     # Create a Select object
    #     select = Select(dropdown)

    #     # Select the option by its index
    #     select.select_by_index(127)

    #     # Click on the element

        # Switch to the first frame

        # Find the dropdown element
        # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_STRM$35$")))
        # select = Select(browser.find_element(By.ID, "CLASS_SRCH_WRK2_STRM$35$"))
        # select.select_by_value("1238")


        # WebDriverWait(browser, 20).until(
        #     EC.presence_of_element_located(( By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH")))
        # browser.find_element(
        #     By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()

        # WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="ptModFrame_0"]')))
        # browser.switch_to.frame(
        #     browser.find_elements(By.TAG_NAME, 'iframe')[0])
        # browser.find_element(By.ID, "#ICSave").click()
        # WebDriverWait(browser, 30).until(
        #     EC.presence_of_element_located((By.ID, 'win0div$ICField94')))


    


def getGrades(studentId: str, password: str):
    '''Extracts the grades of a user from the UP4U platform'''
    try:
        user_data = {
            'grades': [],
        }

        user = User.query.filter_by(userID=studentId).first()
        if user:
            with ChromeBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                loginUP4U(browser, studentId, password)
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
                    cols = row.find_all('div', class_='col-md-12')
                    class_name = cols[0].text.strip() if cols else None

                    cols = row.find_all('div', class_='col-md-1')
                    grade = [col.text.strip() for col in cols] if cols else None

                    cols = row.find_all('div', class_='col-md-2')
                    class_num = cols[0].text.strip() if cols else None

                    # if len(cols) >= 8:
                    #     final_grade = cols[7].text.strip() if cols else None
                    #     official_grade = cols[8].text.strip() if cols else None
                    current_info['Grades'] = grade
                    current_info['Group'] = class_num
                    current_info['Subject'] = class_name

                    # current_info['Final Grade'] = final_grade
                    # current_info['Official Grade'] = official_grade
                    grades.append(current_info)
                print(grades)

                user, message, status_code, error = grades, f'Grades scraped', 200, None
        else:
            user, message, status_code, error = {}, 'User not found', 404, 'User not found'

    except WrongCredentialsError as e:
        logging.warning(e.message)
        user, message, status_code, error ={}, 'Wrong credentials or grades extraction failed', 401, e.message
    return user, message, status_code, error


def getSchedule(studentId: str, password: str):
    '''Extracts the grades of a user from the UP4U platform'''
    try:
        user_data = {
            'schedule': [],
        }
        current_schedule = []

        user = User.query.filter_by(userID=studentId).first()
        if user:
            with ChromeBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                loginUP4U(browser, studentId, password)
                user_data['schedule'] = fetch_schedule_content(browser) #TODO: Create a relation table user-group
                
                #Scrap the schedule from the user schedule
                soup = BeautifulSoup(user_data['schedule'], 'html.parser')
                rows = soup.select('#contenido-tabla .row')
                groups = []
                current_day = ''
                for row in rows:
                    group = []

                    # Scrap the day and room
                    cols = row.find_all('div', class_='col-md-2')
                    tmp_day = cols[0].text.strip() if cols else None
                    if tmp_day != '' and tmp_day != current_day:
                        current_day = tmp_day
                    room = cols[3].text.strip() if cols else None
                    group.append(current_day)
                    group.append(room.split('/')[1].strip() if room else None)
                    
                    # Scrap the class number
                    cols = row.find_all('div', class_='col-md-1')
                    class_num = cols[0].text.strip() if cols else None
                    if class_num not in group:
                        group.append(class_num)

                    # Scrap the time and teacher
                    cols = row.find_all('div', class_='col-md-3')
                    start_time = cols[0].text.strip() if cols else None
                    end_time = cols[1].text.strip() if cols else None
                    teacher = cols[2].text.strip() if cols else None
                    group.append([start_time, end_time])
                    group.append(teacher)

                    # Scrap the subject
                    cols = row.find_all('div', class_='col-md-4')
                    subject = cols[0].text.strip() if cols else None
                    group.append(subject)
                    
                    groups.append(group)

                # Remove duplicates
                # groups = [dict(t) for t in {tuple(d.items()) for d in groups}]

                user, message, status_code, error = groups, f'Grades scraped', 200, None
        else:
            user, message, status_code, error = {}, 'User not found', 404, 'User not found'

    except WrongCredentialsError as e:
        logging.warning(e.message)
        user, message, status_code, error ={}, 'Wrong credentials or grades extraction failed', 401, e.message
    return user, message, status_code, error
