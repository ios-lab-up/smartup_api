from flask import Blueprint, request, jsonify
from school.config import Config
from school.scrapper.utils import *

scrapper = Blueprint('scrapper', __name__)



@scrapper.route('/FetchGroupDataUPSite', methods=['GET'])
def fetchUPSite() -> dict[str, str]:
    '''
    This endpoint returns the schedule of a user in a json format
    '''
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    if request.method == 'GET':
        data = extractUPSiteSchedule(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        
        message, code = f'Data extracted ', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'sucess': True, 'message': message,  'status_code': 200, 'error': None, 'code': code} if data and data != [] and data != [None] else {
        'sucess': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response), response['status_code']
