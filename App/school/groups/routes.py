from flask import Blueprint, Response
from ..groups.utils import *
from ..security import *

groups = Blueprint('groups', __name__)

@groups.route('/getGroup', methods=['GET', 'POST'])
@tokenRequired
def get_group_db() -> Response:
    """This endpoint returns a group from the database"""

    json_data = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    message: str | None = None
    keys = ['filter']
    if request.method == 'GET':
        if not json_data:
            error, code = 'Empty Request', 400
        elif not all(key in json_data for key in keys):
            error, code = f'Missing key: {", ".join(key for key in keys if key not in json_data)}', 400
        else:
            data, message = filterGroups(json_data['filter'])
            code = 1
    else:
        error, code = 'Invalid method', 4

    response.update({'success': True, 'message': message, 'Group': data, 'status_code': 200, 'amount': len(data), 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'success': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
