from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Firefox
from flask_bcrypt import generate_password_hash
from flask import session
from ..tools.utils import color, WrongCredentialsError
import logging


def findUsernameInput(browser: Firefox) -> WebElement:
    """Extracts the username input from the login page"""
    input_username = None
    try:
        input_username = browser.find_element(
            By.XPATH, "//input[@name='Login[username]' and @id='login_username']")

    except NoSuchElementException:
        logging.error(f'{color(1, "Username field not found")} ❌')

    return input_username


def findPasswordInput(browser: Firefox) -> WebElement | None:
    """Extracts the password input from the login page"""
    input_password = None
    try:
        input_password = browser.find_element(
            By.XPATH, "//input[@name='Login[password]'and @id='login_password'] ")

    except NoSuchElementException:
        logging.error(f'{color(1, "Password field not found")} ❌')
    return input_password


# define username and password
def fillUsernameInput(browser: Firefox, student_id: str) -> None:
    """Fills the username input with the username"""
    browser.find_element(By.ID, "login_username").send_keys(student_id)


# Fill inputs with username and password
def fillPasswordInput(browser: Firefox, password: str) -> None:
    """Fills the password input with the password"""
    browser.find_element(By.ID, "login_password").send_keys(password)


# Click on the login button


def clickLoginButton(browser: Firefox) -> None:
    """Clicks on the login button"""
    try:
        browser.find_element(By.ID, "login-button").click()
    except NoSuchElementException:
        logging.error(f'{color(1, "Login button not found")} ❌')


# def login(browser: ChromeBrowser, studentId: str, password: str) -> None:
#     '''Logs in to the UP4U page'''
#     try:
#         ID = fillUsernameInput(browser, studentId)
#         psw = fillPasswordInput(findPasswordInput(browser), password)
#         clickLoginButton(browser)
#         if browser.find_element(By.CLASS_NAME, "help-block").text:
#             logging.error(f"{color(1,'Error message found, login failed')} ❌")
#         else:
#             logging.info(f"{color(2,'Login successful')} ✅")
#             logging.info(f'{color(6,"I'm going to sleep now 😴 ZzZzZ...")}')
#             session['logged_in'] = True
#             session['user'] = {'userID': Id, 'password': generate_password_hash(
#                 psw).decode('utf-8')}
#             time.sleep(3)
#             logging.info(f'{color(6,"Im awake now 🤓")}')
#     except Exception as e:
#         logging.critical(f"{color(5,'Login failed')} ❌\n{e}")

def loginUP4U(browser: Firefox, user_id: str, password: str) -> None:
    """Logs is UP4U page given credentials"""
    try:
        fillUsernameInput(browser, user_id)
        fillPasswordInput(browser, password)
        clickLoginButton(browser)
        if WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, "//*[@id='topbar-first']"))):
            logging.info(f"{color(2, 'Login successful')} ✅")
            session['logged_in'] = True
            session['user'] = {'userID': user_id, 'password': generate_password_hash(password).decode('utf-8'),
                               'name': fetch_user_name(browser)}
        else:
            raise WrongCredentialsError("Wrong credentials")
    except Exception as e:
        logging.critical(f"{color(5, 'Login failed')} ❌\n{e}")


def fetch_user_name(browser: Firefox) -> str:
    """Gets username from UP4U"""
    return browser.find_element(By.XPATH, "//div[@class='user-title pull-left hidden-xs']").find_element(By.XPATH,
                                                                                                         "//strong").text


def fetch_schedule_content(browser: Firefox) -> str:
    """Returns user schedule info"""
    try:
        browser.get('https://up4u.up.edu.mx/Horarios/index?_pjax=%23layout-content&_=1684804482802')
        return browser.page_source
    except Exception as e:
        logging.critical(f"{color(5, 'Fetching schedule failed')} ❌\n{e}")


def fetch_grades_content(browser: Firefox) -> str:
    """Returns user grades info"""
    try:
        browser.get('https://up4u.up.edu.mx/Calificaciones/index')
        return browser.page_source
    except Exception as e:
        logging.critical(f"{color(5, 'Fetching grades failed')} ❌\n{e}")


def findUsernameInputUPSite(browser: Firefox) -> WebElement | None:
    """Extracts the username input from the login page"""
    input_username = None
    try:
        input_username = browser.find_element(
            By.XPATH, "//input[@name='userid' and @id='userid']")
    except NoSuchElementException:
        logging.error(f'{color(1, "Username field not found")} ❌')

    return input_username


def findPasswordInputUPSite(browser: Firefox) -> WebElement | None:
    """Extracts the password input from the login page"""
    input_password = None
    try:
        input_password = browser.find_element(
            By.XPATH, "//input[@name='pwd'and @id='pwd'] ")
    except NoSuchElementException:
        logging.error(f'{color(1, "Password field not found")} ❌')
    return input_password


# define username and password
def fillUsernameInputUPSite(browser: Firefox, student_id: str) -> None:
    """Fills the username input with the username"""

    browser.find_element(By.XPATH, "//*[@id='userid']").send_keys(student_id)


# Fill inputs with username and password
def fillPassswordInputUPSite(browser: Firefox, password: str) -> None:
    """Fills the password input with the password"""

    browser.find_element(By.XPATH, '//*[@id="pwd"]').send_keys(password)


def clickLoginButtonUPSite(browser: Firefox) -> None:
    """Clicks on the login button"""
    try:
        login_button = browser.find_element(
            By.XPATH, "//input[@name='Submit']")
        login_button.click()
    except NoSuchElementException:
        logging.error(f'{color(1, "Login button not found")} ❌')


def loginUPSite(browser: Firefox, student_id: str, password: str) -> None:
    """Logs in to the UPSite page"""
    try:
        fillUsernameInputUPSite(browser, student_id)
        fillPassswordInputUPSite(browser, password)
        clickLoginButtonUPSite(browser)
        WebDriverWait(browser, 10).until(
            ec.presence_of_element_located(
                (By.XPATH, '//*[@id="pthdr2logofluid"]'))
        )
        logging.info(f"{color(2, 'Login successful')} ✅")

    except Exception as e:
        logging.critical(f"{color(5, 'Login failed')} ❌\n{e}")
