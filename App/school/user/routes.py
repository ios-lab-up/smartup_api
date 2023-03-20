from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, session
from school.scrapper.utils import *


user = Blueprint('user', __name__)


@user.route('/user/login', methods=['GET', 'POST'])
def login() -> dict[str, str]:
    '''
    This endpoint returns the schedule of a user in a json format
    '''
    json_data = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    fields = ['password', 'userID']
    if request.method == 'POST':
        if not json_data or not all(json_data.values()):
            error, code = 'No data received', 3
        elif not all(field in json_data for field in fields):
            error, code = f'Missing key: {", ".join(field for field in fields if field not in json_data)}', 400
        else:
            data = extractUP4UContent(
                json_data['userID'], json_data['password'])

            message, code = f'Data extracted', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'User': data, 'status_code': 200, 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
