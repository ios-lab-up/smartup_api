# from school.schedule.utils import getSubject, getUserSubjects
from typing import Any
from flask import Blueprint, request, jsonify, Response
from flask_restful import reqparse
from ..scrapper.utils import *
from ..user.utils import *


login = Blueprint('login', __name__)


@login.route('/user/login', methods=['POST'])
def login_endpoint() -> tuple[Response, Any] | tuple[Response, int]:
    """This endpoint returns a group """
    # Request parsing
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("user_id", type=str, location='json', required=True)
    parser.add_argument("password", type=str, location='json', required=True)
    args = parser.parse_args(strict=True)

    user_id = args.get("user_id")
    password = args.get("password")

    try:
        data,message,status_code, error = extractUP4UContent(user_id,password)
        return jsonify({
            'success': True,
            'message': f'{message}',
            'user': data,
            'status_code': status_code,
            'error': error,
            'code':1
        }), status_code

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'message',
            'status_code': 400,
            'error': str(e),
            'code': 2
        }), 400


# @login.route('/user/login', methods=['GET', 'POST'])
# def loginFunc() -> dict[str, str]:
#     '''
#     This endpoint returns the schedule of a user in a json format
#     '''
#     json_data = request.get_json()
#     data: list[dict[str, str]] = []
#     response: dict[str, str] = {}
#     error, code = None, None
#     fields = ['password', 'userID']
#     if request.method == 'POST':
#         if not json_data or not all(json_data.values()):
#             error, code = 'No data received', 3
#         elif not all(field in json_data for field in fields):
#             error, code = f'Missing key: {", ".join(field for field in fields if field not in json_data)}', 400
#         else:
#             data = extractUP4UContent(
#                 json_data['userID'], json_data['password'])
#             # data['jwt_token'] = encodeJwtToken(data)
#             message, code = f'Data extracted', 1
#     else:
#         error, code = 'Invalid method', 4

#     response.update({'success': True, 'message': message, 'User': data, 'status_code': 200, 'error': error, 'code': code} if data and data != [] and data != [None] else {
#         'success': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
#     return jsonify(response)


@login.route('/user/registerGuest', methods=['GET', 'POST'])
def registerGuestDB() -> Response:
    """
    This endpoint returns the schedule of a user in a json format
    """
    json_data = request.get_json()
    data: list[dict[str, str]] = []
    response: dict[str, str] = {}
    error, code = None, None
    fields = ['name', 'lastName', 'email', 'visitDate']
    if request.method == 'POST':
        if not json_data or not all(json_data.values()):
            error, code = 'No data received', 3
        elif not all(field in json_data for field in fields):
            error, code = f'Missing key: {", ".join(field for field in fields if field not in json_data)}', 400
        else:
            data = createGuest(**json_data)
            message, code = f'User registered', 1
    else:
        error, code = 'Invalid method', 4

    response.update({'success': True, 'message': message, 'User': data, 'status_code': 200, 'error': error, 'code': code} if data and data != [] and data != [None] else {
        'success': False,  'message': 'Could not get content', 'status_code': 400, 'error': f'{error}', 'code': code})
    return jsonify(response)
