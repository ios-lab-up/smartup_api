from school.schedule.utils import *
from school.groups.utils import *
from school.dashboard.utils import *
from school.security import tokenRequired
from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard/self', methods=['GET'])
def dashboard_endpoint() -> dict[str,str]:
    '''This endpoint returns a group '''
    # Request parsing
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("user_id", type=str, location='json', required=True)
    parser.add_argument("password", type=str, location='json', required=True)
    parser.add_argument("info_requested", type=int, location='json', required=True)
    args = parser.parse_args(strict=True)

    user_id = args.get("user_id")
    password = args.get("password")
    info_requested = args.get("info_requested")
    
    # Info Requested stands by the following:
    # 1: Grades
    # 2: Schedule

    try:
        if info_requested == 1:
            data,message,status_code, error = getGrades(user_id,password)
        elif info_requested == 2:
            data,message,status_code, error = getSchedule(user_id,password)
        return jsonify({
            'success': True,
            'message': f'{message}',
            'info': data,
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

# @dashboard.route('/getCurrentGrades', methods=['GET'])
# @tokenRequired
# def getCurrentGrades() -> dict[str:str]:
#     '''This endpoint returns the current grades of the student'''
#     try:
#         data,message,status_code, error = someFunction()
#         return jsonify({
#             'success': True,
#             'message': f'{message}',
#             'compatible_schedules': data,
#             'status_code': status_code,
#             'error': error,
#             'code':1
#         }), status_code

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'message',
#             'status_code': status_code,
#             'error': str(e),
#             'code': 2
#         }), status_code


# @dashboard.route('/getCurrentSchedule', methods=['GET'])
# @tokenRequired
# def getCurrentSchedule() -> dict[str:str]:
#     '''This endpoint returns the current schedule of the student'''
#     try:
#         data,message,status_code, error = someFunction()
#         return jsonify({
#             'success': True,
#             'message': f'{message}',
#             'compatible_schedules': data,
#             'status_code': status_code,
#             'error': error,
#             'code':1
#         }), status_code

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'message',
#             'status_code': status_code,
#             'error': str(e),
#             'code': 2
#         }), status_code

