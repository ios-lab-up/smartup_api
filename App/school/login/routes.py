from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, render_template, session
from school.scrapper.utils import *

login = Blueprint('login', __name__)
