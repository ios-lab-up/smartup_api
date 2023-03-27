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
                # We store the request data in a variable, the data will be the courses that will be used to create the schedules
                data = filterGroups(jsonData)
                # We filter the groups that do not have either capacity or schedules
                data = [group for group in data if group['Schedules'] != []]
                data = [group for group in data if group['students'].split('/')[0] != group['students'].split('/')[1]]
                data = [group for group in data if group['status'] != False]
                # To create the schedules we need to have the courses in a list of lists, so we call the function that does that, and we pass the data as a parameter
                data = cleanData(data)
                # We call the function that creates all the possible combinations of courses
                data = combinations_of_courses(data)
                # We call the function that validates if the schedules are valid (do not have conflicts)
                data = validateSchedule(data)
                
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
