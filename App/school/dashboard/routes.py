from school.schedule.utils import *
from school.groups.utils import *
from school.security import tokenRequired
from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort

dashboard = Blueprint('dashboard', __name__)

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

