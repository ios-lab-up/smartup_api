from school.models import Teacher
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, session
from school.scrapper.utils import *
from school.teacher.utils import *

teacher= Blueprint('teacher', __name__)

@teacher.route('/getTeachers', methods=['GET'])

def get_Teachers() -> dict:
    '''
    Returns a list of teachers that match the filter parameters
    Filter can be: all or id of the class
    Id can be: id of the teacher
    '''
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
            data = filter_Teacher(jsonData)
            message,code= f'Teachers found', 1
    else:
        error, code = 'Invalid method', 4
    
    response.update({'success': True, 'message': message, 'Teacher': data, 'status_code': 200, 'amount': len(data), 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'success': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)