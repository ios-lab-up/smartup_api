from flask import Flask
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


app = Flask(__name__)


@app.route('/')
def hello_world():
    service = webdriver.firefox.service.Service('/usr/local/bin/geckodriver')
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://up4u.up.edu.mx/user/auth/login')
    html = driver.page_source
    return html


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_reloader=True, use_debugger=True, port=5555)
