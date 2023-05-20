from school.schedule.utils import *
from school.groups.utils import *
from school.security import tokenRequired
from flask import Blueprint, request, jsonify
from flask_restful import reqparse, abort

schedule = Blueprint('schedule', __name__)

@schedule.route('/createSchedules', methods=['POST'])
@tokenRequired
def createSchedules() -> dict[str:str]:
    '''This endpoint returns a group '''
    # Request parsing
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("subjects", type=list, location='json', required=True)
    parser.add_argument("teachers", type=list, location='json', required=False, default=[])
    parser.add_argument("minimum", type=int, location='json', required=False, default=1)
    args = parser.parse_args(strict=True)

    # Default values
    teachers = args.get("teachers")
    minimum = args.get("minimum")

    try:
        print(teachers)
        data,message,status_code, error = createCompatibleSchedules(
            [getGroup(group.id, 2) for group in Group.query.filter(Group.subject.in_(args['subjects'])).filter(
                Group.schedule.any()).filter_by(status=True).all()], teachers, minimum)
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