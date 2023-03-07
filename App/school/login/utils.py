from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from flask_bcrypt import generate_password_hash
from school.models import *
from school.tools.utils import color
import time
import logging
from flask import session


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
def fillUsernameInput(inputUsername: str, studentId: str) -> str:
    '''Fills the username input with the username'''
    inputUsername.send_keys(studentId)
    input_value = inputUsername.get_attribute("value")
    return input_value


# Fill inputs with username and password
def fillPassswordInput(inputPassword: str, password: str) -> str:
    '''Fills the password input with the password'''
    inputPassword.send_keys(password)
    input_value = inputPassword.get_attribute("value")
    return input_value

# Click on login button


def clickLoginButton(browser: ChromeBrowser) -> None:
    '''Clicks on the login button'''
    try:
        loginButton = browser.find_element(By.ID, "login-button")
        loginButton.click()
    except NoSuchElementException:
        logging.error(f'{color(1,"Login button not found")} ❌')


def login(browser: ChromeBrowser, studentId: str, password: str) -> str:
    '''Logs in to the UP4U page'''
    try:
        Id = fillUsernameInput(findUsernameInput(browser), studentId)
        psw = fillPassswordInput(findPasswordInput(browser), password)
        clickLoginButton(browser)
        if browser.find_element(By.CLASS_NAME, "help-block").text:
            logging.error(f"{color(1,'Error message found, login failed')} ❌")
        else:
            logging.info(f"{color(2,'Login successful')} ✅")
            logging.info(f'{color(6,"Im going to sleep now 😴 ZzZzZ...")}')
            session['logged_in'] = True
            session['student'] = {'studentID': Id, 'password': generate_password_hash(
                psw).decode('utf-8')}
            time.sleep(3)
            logging.info(f'{color(6,"Im awake now 🤓")}')
    except Exception as e:
        logging.critical(f"{color(5,'Login failed')} ❌\n{e}")
    return f'Current URL after login: \033[94m{browser.current_url}\033[0m'


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
def fillUsernameInputUPSite(inputUsername: str, studentId: str) -> str:
    '''Fills the username input with the username'''
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


def loginUPSite(browser: ChromeBrowser, studentId: str, password: str) -> str:
    '''Logs in to the UPSite page'''
    try:
        Id = fillUsernameInputUPSite(
            findUsernameInputUPSite(browser), studentId)
        pwd = fillPassswordInputUPSite(
            findPasswordInputUPSite(browser), password)
        clickLoginButtonUPSite(browser)
        # if current url is not the same as the login url, login was successful
        if browser.current_url == "https://upsite.up.edu.mx/psp/CAMPUS/?&cmd=login&errorCode=105&languageCd=ESP":
            logging.error(f"{color(1,'Error message found, login failed')} ❌")
        else:
            logging.info(f"{color(2,'UPSite Login successful')} ✅")
            logging.info(f'{color(6,"Im going to sleep now 😴 ZzZzZ...")}')
            session['logged_in'] = True
            session['student'] = {'studentID': Id, 'password': generate_password_hash(
                pwd).decode('utf-8')}
            time.sleep(3)
            logging.info(f'{color(6,"Im awake now 🤓")}')
    except Exception as e:
        logging.critical(f"{color(5,'UPSite Login failed')} ❌\n{e}")
    # color the url blue in the terminal
    return f'Current URL after login: \033[94m{browser.current_url}\033[0m'
