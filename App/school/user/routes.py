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
    keys = ['filter', 'userID']
    if request.method == 'GET':
        if not jsonData:
            response.update({'sucess': False, 'message': 'Empty Request', 'status_code': 400, 'error': 'Empty Request', 'code': 400})
        elif not all(key in jsonData for key in keys):
            response.update({'sucess': False, 'message': f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 'status_code': 400, 'error': f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 'code': 400})
        else:
            data = getUsers({'filter': jsonData['filter'], 'userID': jsonData['userID']})
            response.update({'sucess': True, 'message': 'Users found', 'Users': data, 'status_code': 200, 'error': None, 'code': None} if data else {'sucess': False, 'message': 'Could not get content', 'status_code': 400, 'error': 'Could not get content', 'code': 400})
    else:
        response.update({'sucess': False, 'message': 'Invalid method', 'status_code': 405, 'error': 'Invalid method', 'code': 405})
    return jsonify(response)