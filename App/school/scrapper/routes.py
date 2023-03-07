from school.models import Student
# from school.schedule.utils import getSubject, getStudentSubjects
from flask import Blueprint, request, jsonify, render_template, session
from school.scrapper.utils import *

scrapper = Blueprint('scrapper', __name__)


@scrapper.route('/login/<string:studentID>', methods=['GET', 'POST'])
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


@scrapper.route('/createCompatibleSchedule/<string:studentID>', methods=['GET', 'POST'])
def createStudentCompatibleSchedule(studentID: str) -> dict[str, str]:
    '''This endpoint returns a compatible schedule for a student'''
    if request.method == 'POST':
        data: list[dict[str, str]] = []
        response: dict[str, str] = {}
        error, code = None, None

        if Student.query.filter_by(studentID=studentID).first():
            data = createCompatibleSchedule(Subject.query.all())
            message, code = f'Compatible schedule created for {session["student"]["studentID"]}', 1
        else:
            error, code = 'Student not found', 2
    else:
        error, code = 'Invalid method', 3

    response.update({'sucess': True, 'message': message, 'Compatible Schedule': data, 'status_code': 200, 'error': None, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)


@scrapper.route('/FetchGroupDataUPSite/<string:studentID>', methods=['GET', 'POST'])
def fetchUPSite(studentID: str) -> dict[str, str]:
    '''
    This endpoint returns the schedule of a student in a json format
    '''
    if request.method == 'POST':
        json_data = request.get_json()
        data: list[dict[str, str]] = []
        response: dict[str, str] = {}
        error, code = None, None
        if not json_data or not all(json_data.values()):
            error, code = 'No data received', 3
        elif 'password' not in json_data:
            error, code = 'Missing fields', 2
        else:
            student = Student.query.filter_by(studentID=studentID).first()
            if student:
                data = extractUPSiteSchedule(studentID, json_data['password'])
            message, code = f'Data extracted for {session["student"]["studentID"]}', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'Schedule': data, 'status_code': 200, 'error': None, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
