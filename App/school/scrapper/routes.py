from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, render_template, session
from school.scrapper.utils import *

scrapper = Blueprint('scrapper', __name__)


# @scrapper.route('/createCompatibleSchedule/<string:studentID>', methods=['GET', 'POST'])
# def createStudentCompatibleSchedule(studentID: str) -> dict[str, str]:
#     '''This endpoint returns a compatible schedule for a student'''
#     if request.method == 'POST':
#         data: list[dict[str, str]] = []
#         response: dict[str, str] = {}
#         error, code = None, None

#         if User.query.filter_by(userID=userID).first():
#             data = createCompatibleSchedule(Subject.query.all())
#             message, code = f'Compatible schedule created for {session["user"]["userID"]}', 1
#         else:
#             error, code = 'User not found', 2
#     else:
#         error, code = 'Invalid method', 3

#     response.update({'sucess': True, 'message': message, 'Compatible Schedule': data, 'status_code': 200, 'error': None, 'code': code} if data and data != [] and data != [None] else {
#         'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
#     return jsonify(response)


@scrapper.route('/FetchGroupDataUPSite/<string:userID>', methods=['GET', 'POST'])
@tokenRequired
def fetchUPSite(userID: str) -> dict[str, str]:
    '''
    This endpoint returns the schedule of a user in a json format
    '''
    json_data = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    if request.method == 'POST':
        if not json_data or not all(json_data.values()):
            error, code = 'No data received', 3
        elif 'password' not in json_data:
            error, code = 'Missing fields', 2
        else:
            user = User.query.filter_by(userID=userID).first()
            if user:
                data = extractUPSiteSchedule(userID, json_data['password'])
            message, code = f'Data extracted ', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'Schedule': data, 'status_code': 200, 'error': None, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
