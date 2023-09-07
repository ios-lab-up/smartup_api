from time import sleep
from ..subjects.utils import CloseUnnecessaryTabs
from ..login.utils import *
from ..models import FirefoxBrowser
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver import Firefox
from ..tools.utils import color
from ..models import User
import logging
import traceback
from bs4 import BeautifulSoup


def enter_dashboard(browser: Firefox) -> str:
    """Extracts the schedule link from the main page"""
    user_name = None
    try:
        try:
            user_name = browser.find_element(
                By.XPATH, "//div[@class='user-title pull-left hidden-xs']").find_element(By.XPATH, "//strong").text

        except NoSuchElementException:
            logging.error(
                f'{color(1,"Couldnt create user")} ❌ {traceback.format_exc().splitlines()[-3]}')

    except NoSuchElementException:
        logging.error(f'{color(1,"Schedule link not found")} ❌')

    return user_name


def enter_up_site_subjects(browser: Firefox) -> bool:
    """Fetches the subjects from the UPSite page"""
    try:
        # sleep 10 seconds and print it

        # browser.get(
        #     "https://upsite.up.edu.mx/psc/CAMPUS/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?ICType=Panel&ICElementNum=0&ICStateNum=21&ICResubmit=1&ICAJAX=1&")

        # WebDriverWait(browser, 20).until(
        #     ec.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH")))


        # element = browser.find_element(value='CLASS_SRCH_WRK2_STRM$35$')
        # dropdown = Select(element)
        # dropdown.select_by_index(126)

        browser.get("https://upsite.up.edu.mx/psc/CAMPUS/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?ICType=Panel&ICElementNum=0&ICStateNum=21&ICResubmit=1&ICAJAX=1&/psp/CAMPUS/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?PORTALPARAM_PTCNAV=HC_CLASS_SEARCH&EOPP.SCNode=SA&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=PT_PTPP_PORTAL_ROOT&EOPP.SCLabel=Autoservicio&EOPP.SCFName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCSecondary=true&EOPP.SCPTfname=CO_EMPLOYEE_SELF_SERVICE&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_SS_CATALOG.HC_CLASS_SEARCH&IsFolder=false")
        browser.set_window_size(1062, 768)
        browser.execute_script("document.body.style.zoom='90%'")

        #browser.switch_to.frame(0)
        print("cambio pantalla y frame")
        browser.find_element(By.ID, "CLASS_SRCH_WRK2_STRM$35$").click()
        print("click en dropdown")
        browser.find_element(By.CSS_SELECTOR, "option:nth-child(127)").click()
        print("click en opcion")
        print("licenciatura maybe")
        # browser.find_element(By.ID, "SSR_CLSRCH_WRK_ACAD_CAREER$2").click()
        # dropdown = browser.find_element(By.ID, "SSR_CLSRCH_WRK_ACAD_CAREER$2")
        # dropdown.find_element(By.XPATH, "//option[. = 'Licenciatura']").click()
        browser.execute_script("document.body.style.zoom='90%'")
        browser.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()
        print("click en boton search 1st")
        browser.switch_to.default_content()
        browser.switch_to.frame(3)
        browser.find_element(By.CSS_SELECTOR, ".PSPUSHBUTTON:nth-child(1) > span").click()
        browser.find_element(By.ID, "#ICSave").click()
        print("click en boton search 2nd")

        # element = browser.find_element(value='CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')
        # print("search primero encontrado")
        # browser.execute_script("arguments[0].scrollIntoView();", element)
        # print("scrolled")
        # element.click()
        # print("clicked 1st button")

        # browser.find_element(value="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()
        # CloseUnnecessaryTabs(browser)
        # print("found and clicked search 1st button")
        # WebDriverWait(browser, 10).until(
        #     ec.presence_of_element_located((By.XPATH, '//*[@id="ptModFrame_0"]')))

        # browser.switch_to.frame(
        #     browser.find_elements(By.TAG_NAME, 'iframe')[0])

        # sleep(5)
        # browser.find_element(value="#ICSave").click()

        #WebDriverWait(browser, 30).until(ec.presence_of_element_located((By.ID, 'win0div$ICField94')))
        sleep(15)

        if ec.presence_of_element_located((By.ID, 'win0div$ICField94')):
            logging.info(
                f'{color(2,"Enter Carrito de Inscripción...")} ✅')
            browser.switch_to.default_content()
            return True
        else:
            raise NoSuchElementException
    except NoSuchElementException:
        logging.error(
            f'{color(1,"Carrito de Inscripción link not found")} ❌ {traceback.format_exc().splitlines()[-3]}')
        return False


def get_grades(student_id: str, password: str):
    """Extracts the grades of a user from the UP4U platform"""
    try:
        user_data = {
            'grades': [],
        }

        user = User.query.filter_by(userID=student_id).first()
        if user:
            with FirefoxBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                loginUP4U(browser, student_id, password)
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


def get_schedule(student_id: str, password: str):
    """Extracts the grades of a user from the UP4U platform"""
    try:
        user_data = {
            'schedule': [],
        }

        user = User.query.filter_by(userID=student_id).first()
        if user:
            with FirefoxBrowser().buildBrowser() as browser:
                browser.get("https://up4u.up.edu.mx/user/auth/login")
                loginUP4U(browser, student_id, password)
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
