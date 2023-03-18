from flask import Blueprint, request, jsonify, render_template, session
from school.schedule.utils import *

schedule = Blueprint('schedule', __name__)

@schedule.route('/createSchedule', methods=['GET', 'POST'])
def createSchedule() -> None:
    error, code = None, None
    if request.method == 'GET':
        pass
    else:
        error, code = 'Invalid method', 4

    response = {'error': error, 'code': code} if error and code else f'Schedule created ✅'
    return jsonify(response)
