from school.schedule.utils import *
from school.groups.utils import *
from flask import Blueprint, request, jsonify
from school.security import tokenRequired

schedule = Blueprint('schedule', __name__)

@schedule.route('/createSchedules', methods=['GET', 'POST'])
@tokenRequired
def createSchedules() -> None:
    '''This endpoint returns a group '''

    jsonData = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    keys = ['subjects']
    if request.method == 'POST':
        if not jsonData:
            error, code = 'Empty Request', 400
        elif not all(key in jsonData for key in keys):
            error, code = f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 400
        else:
            data  = createCompatibleSchedules([getGroup(group.id, 2) for group in  Group.query.filter(Group.subject.in_(jsonData['subjects'])).filter(Group.schedule.any()).all()])
            message = f'{len(data)} schedules created'
            code = 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'compatible_schedules': data, 'status_code': 200, 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
