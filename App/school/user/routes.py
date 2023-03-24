from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, session
from school.scrapper.utils import *


user = Blueprint('user', __name__)

