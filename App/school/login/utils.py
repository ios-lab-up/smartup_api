from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_bcrypt import generate_password_hash
from school.models import *
from flask import session
from school.tools.utils import color, WrongCredentialsError
import time
import requests
import logging


def findUsernameInput(browser: ChromeBrowser) -> str:
    '''Extracts the username input from the login page'''
    try:
        inputUsername = browser.find_element(
            By.XPATH, "//input[@name='Login[username]' and @id='login_username']")
    except NoSuchElementException:
        logging.error(f'{color(1,"Username field not found")} ❌')

    return inputUsername


def findPasswordInput(browser: ChromeBrowser) -> str:
    '''Extracts the password input from the login page'''
    try:
        inputPassword = browser.find_element(
            By.XPATH, "//input[@name='Login[password]'and @id='login_password'] ")
    except NoSuchElementException:
        logging.error(f'{color(1,"Password field not found")} ❌')
    return inputPassword


# define username and password
def fillUsernameInput(browser: ChromeBrowser, studentId: str) -> str:
    '''Fills the username input with the username'''
    browser.find_element(
            By.XPATH, "//input[@name='Login[username]' and @id='login_username']").send_keys(studentId)




# Fill inputs with username and password
def fillPassswordInput(browser: ChromeBrowser, password: str) -> str:
    '''Fills the password input with the password'''
    browser.find_element(By.XPATH, "//input[@name='Login[password]'and @id='login_password'] ").send_keys(password)

# Click on login button


def clickLoginButton(browser: ChromeBrowser) -> None:
    '''Clicks on the login button'''
    try:
        browser.find_element(By.ID, "login-button").click()
    except NoSuchElementException:
        logging.error(f'{color(1,"Login button not found")} ❌')


def login(browser: ChromeBrowser, studentId: str, password: str) -> str:
    '''Logs in to the UP4U page'''
    try:
        Id = fillUsernameInput(browser, studentId)
        psw = fillPassswordInput(findPasswordInput(browser), password)
        clickLoginButton(browser)
        if browser.find_element(By.CLASS_NAME, "help-block").text:
            logging.error(f"{color(1,'Error message found, login failed')} ❌")
        else:
            logging.info(f"{color(2,'Login successful')} ✅")
            logging.info(f'{color(6,"Im going to sleep now 😴 ZzZzZ...")}')
            session['logged_in'] = True
            session['user'] = {'userID': Id, 'password': generate_password_hash(
                psw).decode('utf-8')}
            time.sleep(3)
            logging.info(f'{color(6,"Im awake now 🤓")}')
    except Exception as e:
        logging.critical(f"{color(5,'Login failed')} ❌\n{e}")
    return f'Current URL after login: \033[94m{browser.current_url}\033[0m'

def loginUP4U(browser: ChromeBrowser, user_id: str, password: str) -> None:
    '''Logs is UP4U page given credentials'''
    try:
        fillUsernameInput(browser,user_id)
        fillPassswordInput(browser,password)
        clickLoginButton(browser)
        if WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='topbar-first']"))):
            logging.info(f"{color(2,'Login successful')} ✅")
            session['logged_in'] = True
            session['user'] = {'userID': user_id, 'password': generate_password_hash(password).decode('utf-8'), 'name':fetch_user_name(browser)}
        else:
            raise WrongCredentialsError("Wrong credentials")
    except Exception as e:
        logging.critical(f"{color(5,'Login failed')} ❌\n{e}")
           
def fetch_user_name(browser) -> str:
    '''Gets user name from UP4U'''
    return browser.find_element(By.XPATH, "//div[@class='user-title pull-left hidden-xs']").find_element(By.XPATH, "//strong").text



def fetch_schedule_content(browser: ChromeBrowser) -> str:
    '''Returns user schedule info'''
    try:
        browser.get('https://up4u.up.edu.mx/Horarios/index?_pjax=%23layout-content&_=1684804482802')
        return browser.page_source
    except Exception as e:
        logging.critical(f"{color(5,'Fetching schedule failed')} ❌\n{e}")

def fetch_grades_content(browser: ChromeBrowser) -> str:
    '''Returns user grades info'''
    try:
        browser.get('https://up4u.up.edu.mx/Calificaciones/index')
        return browser.page_source
    except Exception as e:
        logging.critical(f"{color(5,'Fetching grades failed')} ❌\n{e}")


def findUsernameInputUPSite(browser: ChromeBrowser) -> str:
    '''Extracts the username input from the login page'''
    try:
        inputUsername = browser.find_element(
            By.XPATH, "//input[@name='userid' and @id='userid']")
    except NoSuchElementException:
        logging.error(f'{color(1,"Username field not found")} ❌')

    return inputUsername


def findPasswordInputUPSite(browser: ChromeBrowser) -> str:
    '''Extracts the password input from the login page'''
    try:
        inputPassword = browser.find_element(
            By.XPATH, "//input[@name='pwd'and @id='pwd'] ")
    except NoSuchElementException:
        logging.error(f'{color(1,"Password field not found")} ❌')
    return inputPassword


# define username and password
def fillUsernameInputUPSite(browser: ChromeBrowser, studentId: str) -> str:
    '''Fills the username input with the username'''
    inputUsername =findUsernameInput(browser)
    print(inputUsername)
    inputUsername.send_keys(studentId)
    input_value = inputUsername.get_attribute("value")
    return input_value


# Fill inputs with username and password
def fillPassswordInputUPSite(inputPassword: str, password: str) -> str:
    '''Fills the password input with the password'''
    inputPassword.send_keys(password)
    input_value = inputPassword.get_attribute("value")
    return input_value


def clickLoginButtonUPSite(browser: ChromeBrowser) -> None:
    '''Clicks on the login button'''
    try:
        loginButton = browser.find_element(
            By.XPATH, "//input[@name='Submit']")
        loginButton.click()
    except NoSuchElementException:
        logging.error(f'{color(1,"Login button not found")} ❌')


def loginUPSite(browser: ChromeBrowser, studentId: str, password: str) -> bool:
    '''Logs in to the UPSite page'''
    Id = fillUsernameInputUPSite(
        findUsernameInputUPSite(browser), studentId)
    pwd = fillPassswordInputUPSite(
        findPasswordInputUPSite(browser), password)
    clickLoginButtonUPSite(browser)
    # if current url is not the same as the login url, login was successful
    if browser.current_url == "https://upsite.up.edu.mx/psp/CAMPUS/?&cmd=login&errorCode=105&languageCd=ESP":
        logging.error(f"{color(1,'Wrong Credentials for login')} ❌")
        return False
    else:
        logging.info(f"{color(2,'UPSite Login successful')} ✅")
        session['logged_in'] = True
        session['user'] = {'userID': Id, 'password': generate_password_hash(
            pwd).decode('utf-8')}

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="pthdr2logofluid"]'))
        )

        return True

