from flask_restful.reqparse import RequestParser
from ..schedule.utils import *
from ..groups.utils import *
from ..security import tokenRequired
from flask import Blueprint, jsonify
from flask_restful import reqparse

schedule = Blueprint('schedule', __name__)

@tokenRequired
def createSchedules() -> dict[str:str]:
    """This endpoint returns a group """
    # Request parsing
    parser: RequestParser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("subjects", type=list, location='json', required=True)
    parser.add_argument("teachers", type=list, location='json', required=False, default=[])
    parser.add_argument("minimum", type=int, location='json', required=False, default=3)
    args = parser.parse_args(strict=True)

    # Default values
    teachers = args.get("teachers")
    minimum = args.get("minimum")

    status_code: int | None = 200
    try:
        data,message,status_code, error = createCompatibleSchedules(
            [getGroup(group.id, 2) for group in Group.query.filter(Group.subject.in_(args['subjects']),Group.schedule.any(),Group.status == True).all()], teachers, minimum)
        return jsonify({
            'success': True,
            'message': f'{message}',
            'compatible_schedules': data,
            'status_code': status_code,
            'error': error,
            'code':1
        }), status_code

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'message',
            'status_code': status_code,
            'error': str(e),
            'code': 2
        }), status_code

@schedule.route('/excelSchedules', methods=['POST'])
@tokenRequired
def schedules_with_excel() -> dict[str:str]:
    """This endpoint returns a group """
    # Request parsing
    parser: RequestParser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("subjects", type=list, location='json', required=True)
    parser.add_argument("teachers", type=list, location='json', required=False, default=[])
    parser.add_argument("minimum", type=int, location='json', required=False, default=3)
    args = parser.parse_args(strict=True)

    # Default values
    teachers = args.get("teachers")
    minimum = args.get("minimum")

    status_code: int | None = 200
    try:
        data,message,status_code, error = createCompatibleSchedules(
            [getGroup(group.id, 2) for group in Group.query.filter(Group.subject.in_(args['subjects']),Group.schedule.any(),Group.status == True).all()], teachers, minimum)
        cleanSchedulesOutput(data)
        return jsonify({
            'success': True,
            'message': f'{message}',
            'compatible_schedules': data,
            'status_code': status_code,
            'error': error,
            'code':1
        }), status_code

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'message',
            'status_code': status_code,
            'error': str(e),
            'code': 2
        }), status_code
