import os
import secrets


class Config:
    # SQL Credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    MYSQL_HOST = os.environ.get("MYSQL_HOST", 'db')
    MYSQL_USER = os.environ.get("MYSQL_USER", 'generic_operator')
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", 'school')
    MYSQL_DB = os.environ.get("MYSQL_DB", 'School_DB')
    MYSQL_PORT = os.environ.get("MYSQL_PORT", '3306')
    SQLALCHEMY_DATABASE_URI = "mysql://" + MYSQL_USER + ":" + \
        MYSQL_PASSWORD+"@"+MYSQL_HOST+"/"+MYSQL_DB+"?charset=utf8mb4"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Credentials
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", '0256158')
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", 'olypapamama123A@')

    # JWT Secret Key

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", secrets.token_hex(16))

    # URL for uploading pdfs
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", 'App/school/static/uploads')

    QR_PATH = os.environ.get(
        "QR_PATH", 'App/school/static/guests_qr_codes'
    )
    SCHEDULE_PATH = os.environ.get(
        "SCHEDULE_PATH", 'App/school/static/schedules')

    # check if the folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(QR_PATH):
        os.makedirs(QR_PATH)
    
    if not os.path.exists(SCHEDULE_PATH):
        os.makedirs(SCHEDULE_PATH)

    # # Flask-Mail SMTP server settings
    # MAIL_SERVER = os.environ.get("MAIL_SERVER", 'smtp.@gmail.com')
    # MAIL_PORT = os.environ.get("MAIL_PORT", '465')
    # MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", 'False')
    # MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", 'True')
    # MAIL_EMAIL = os.environ.get(
    #     "MAIL_EMAIL", 'namelessnoreply25@gmail.com')
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", 'dpivkcsjblqscusq')
