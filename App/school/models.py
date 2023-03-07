from school import db
from school.relations import *
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os.path


@dataclass
class ChromeBrowser:
    """Class to create a Chrome browser instance"""

    def __init__(self):
        """Constructor method to initialize the Chrome browser instance"""
        self.chromeOptions = Options()
        self.chromeOptions.add_argument("--headless")  # Ensure GUI is off
        self.chromeOptions.add_argument("--no-sandbox")
        self.chromeOptions.add_argument("--disable-dev-shm-usage")

    def buildBrowser(self) -> webdriver:
        """Method to build a Chrome browser instance"""
        webdriverService = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(
            service=webdriverService, options=self.chromeOptions)
        return browser


@dataclass
class Group(db.Model):
    '''Model to represent a group for storing groups in the database'''

    __tablename__ = 'Group'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    classNumber: int = db.Column(db.Integer, nullable=False)
    group: str = db.Column(db.String(280), nullable=False)
    language: str = db.Column(db.String(280), nullable=False)
    students: str = db.Column(db.String(280), nullable=True)
    modality: str = db.Column(db.String(280), nullable=False)
    description: str = db.Column(db.String(280), nullable=True)
    startDate: datetime = db.Column(
        db.Date, nullable=True)
    endDate: datetime = db.Column(
        db.Date, nullable=True)
    options: int = db.Column(db.Integer, nullable=False, default=0)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Backref
    subject: int = db.Column(db.Integer, db.ForeignKey(
        'Subject.id'), nullable=False)
    teacher: int = db.Column(db.Integer, db.ForeignKey(
        'Teacher.id'), nullable=False)

    # Secondary table

    schedule: list = db.relationship(
        'Schedule', secondary=RelationGroupSchedule, backref=db.backref('groups', lazy='dynamic'))

    def toDict(self) -> dict:
        return {
            column.name: getattr(self, column.name).strftime(
                '%Y-%m-%d %H:%M:%S')
            if isinstance(getattr(self, column.name), datetime)
            else getattr(self, column.name)
            for column in self.__table__.columns
        }


@dataclass
class Subject(db.Model):
    '''Model to represent a subject for storing subjects in the database'''

    __tablename__ = 'Subject'

    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    option: int = db.Column(db.Integer, nullable=False, default=0)

    # Relationships

    # Secondary table

    def __repr__(self) -> str:
        '''Convert the subject to a string'''
        return f'Subject:{" ".join([f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns])}'

    def to_dict(self) -> dict:
        '''Convert the subject to a dictionary'''
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@dataclass
class Student(db.Model):
    '''Model to represent a student for storing students in the database'''

    __tablename__ = 'Student'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    studentID: str = db.Column(db.String(280), nullable=False)
    password: str = db.Column(db.String(280), nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    lastName: str = db.Column(db.String(280), nullable=False)
    email: str = db.Column(db.String(280), nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    options: int = db.Column(db.Integer, nullable=False, default=0)

    # Relationships

    # Secondary table

    def __repr__(self) -> str:
        '''Convert the student to a string'''
        return f'Student:{" ".join([f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns])}'

    def toDict(self) -> dict:
        return {
            column.name: getattr(self, column.name).strftime(
                '%Y-%m-%d %H:%M:%S')
            if isinstance(getattr(self, column.name), datetime)
            else getattr(self, column.name)
            for column in self.__table__.columns
        }


@dataclass
class Classroom(db.Model):
    '''Model to represent a classroom '''
    __tablename__ = 'Classroom'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    options: int = db.Column(db.Integer, nullable=False, default=0)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships


@dataclass
class Teacher(db.Model):
    '''Model to represent a teacher '''
    __tablename__ = 'Teacher'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    name: str = db.Column(db.String(280), nullable=False)
    options: int = db.Column(db.Integer, nullable=False, default=0)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: str = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Relationships


@dataclass
class Days(db.Model):
    '''Model to represent a day '''
    __tablename__ = 'Days'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    day: str = db.Column(db.String(280), nullable=False)


@dataclass
class Hours(db.Model):
    '''Model to represent a hour '''
    __tablename__ = 'Hours'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    hour: str = db.Column(db.String(280), nullable=False)


@dataclass
class Schedule(db.Model):
    '''Model to represent the junction table between groups and days and hours'''

    __tablename__ = 'Schedule'
    id: int = db.Column(db.Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    classroomID: int = db.Column(db.Integer, db.ForeignKey(
        'Classroom.id'), nullable=False)
    day: str = db.Column(db.String(280), nullable=False)
    startTime: datetime = db.Column(db.Time, nullable=False)
    endTime: datetime = db.Column(db.Time, nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False, default=True)
    creationDate: datetime = db.Column(
        db.Date, nullable=False, default=datetime.now)
    lastupDate: datetime = db.Column(
        db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)

    def toDict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
