from flask import Blueprint, Response
from ..config import Config
from ..scrapper.utils import *

scrapper = Blueprint('scrapper', __name__)


@scrapper.route('/FetchGroupDataUPSite', methods=['GET'])
def fetchUPSite() -> tuple[Response, int]:
    """
    This endpoint returns the schedule of a user in a json format
    """
    if request.method == 'GET':
        data = extractUPSiteContent(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        if data:
            response = {
                'success': True,
                'message': 'Successfully fetched data',
                'code': 1
            }
        else:
            response = {
                'success': False,
                'message': 'Failed to fetch data',
                'code': 2
            }
    else:
        response = {
            'success': False,
            'message': 'Method not allowed',
            'code': 3
        }
    return jsonify(response), 200 if response['success'] else 400
