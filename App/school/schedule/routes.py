from school.schedule.utils import *
from school.groups.utils import *
from flask import Blueprint, request, jsonify, render_template, session

schedule = Blueprint('schedule', __name__)

@schedule.route('/createSchedules', methods=['GET', 'POST'])
def createSchedules() -> None:
    jsonData = request.get_json()
    data: list = []
    response: dict[str, str] = {}
    error, code = None, None
    keys = ['ids', 'subject']
    if request.method == 'GET':

        if not jsonData:
            error, code = 'Empty Request', 400
        elif not any(key in jsonData for key in keys):
            error, code = f'Missing key: {", ".join(key for key in keys if key not in jsonData)}', 400
        else:
            if 'subject' in jsonData:
                data = filterGroups(jsonData)
                data = [group for group in data if group['Schedules'] != []]
                data = [group for group in data if group['students'].split('/')[0] != group['students'].split('/')[1]]
                data = [group for group in data if group['status'] != False]
                data = cleanData(data)
                data = combinations_of_courses(data)
                
            elif 'ids' in jsonData:
                data = jsonData['ids']
                combinations = combinations_of_courses(data)
                data = combinations
            message, code = f'Schedules generated', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message, 'Combinations': data, 'status_code': 200, 'error': error, 'code': code, 'combinations': len(data)} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)

# {
#   "ids": [
#     [
#       "fisica1",
#       "fisica2",
#       "fisica3"
#     ],
#     [
#       "matematicas1",
#       "matematicas2",
#       "matematicas3"
#     ],
#     [
#       "quimica1",
#       "quimica2",
#       "quimica3",
#       "quimica4",
#       "quimica5",
#       "quimica6",
#       "quimica7",
#       "quimica8",
#       "quimica9"
#     ],
#     [
#       "ingles1",
#       "ingles2"
#     ]
#   ]
# }