from school.models import Group
from school.schedule.utils import cleanGroupQuery
from flask import Blueprint, request, jsonify, render_template, session
from school.groups.utils import *
from school.security import *

groups = Blueprint('groups', __name__)

@groups.route('/getGroup', methods=['GET', 'POST'])
@tokenRequired

def getGroupDB() -> dict[str, str]:
    '''This endpoint returns a group from the database'''

    jsonData = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    keys = ['filter']
    if request.method == 'GET':
        if not jsonData:
            error, code = 'Empty Request', 400
        elif not all(key in jsonData for key in keys):
            error, code = f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 400
        else:
            data, message = filterGroups(jsonData['filter'])
            code = 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'Group': data, 'status_code': 200, 'amount': len(data), 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
