from school.models import Student
# from school.schedule.utils import getSubject, getStudentSubjects
from flask import Blueprint, request, jsonify, render_template, session
from school.scrapper.utils import *

login = Blueprint('login', __name__)


@login.route('/login/<string:studentID>', methods=['GET', 'POST'])
def getStudentSchedule(studentID: str) -> dict[str, str]:
    '''
    This endpoint returns the schedule of a student in a json format
    '''
    if request.method == 'GET':
        json_data = request.get_json()
        data: list[dict[str, str]] = []
        response: dict[str, str] = {}
        error, code = None, None
        if not json_data or not all(json_data.values()):
            error, code = 'No data received', 3
        elif 'password' not in json_data:
            error, code = 'Missing fields', 2
        else:
            extractUP4USchedule(studentID, json_data['password'])
            data = Student.query.filter_by(
                studentID=studentID).first()
            message, code = f'Data extracted', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'Student': data, 'status_code': 200, 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)