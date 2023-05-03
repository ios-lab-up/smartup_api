from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, session
from school.scrapper.utils import *
from school.user.utils import *
import traceback
import logging

user = Blueprint('user', __name__)

@user.route('/getUsers', methods=['GET'])

def get_Users() -> dict:
    '''This endpoint returns a list of users from the database if filter: all or a user if filter: id'''
    jsonData = request.get_json()
    response: dict[str, str] = {}
    error, code = None, None
    keys = ['filter', 'id']
    if request.method == 'GET':
        if not jsonData:
            error, code = 'Empty Request', 400
        elif not any(key in jsonData for key in keys):
            error, code = f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 400
        elif 'filter' or 'id' in jsonData.keys():
            data = filter_User(jsonData)
            message,code= f'Users found', 1
    else:
        error, code = 'Invalid method', 4


    response.update({'sucess': True, 'message': message, 'User': data, 'status_code': 200, 'amount': len(data), 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)