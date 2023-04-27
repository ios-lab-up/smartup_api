from flask import Flask, jsonify, request
from school.models import User, Subject
from school import db
from school.tools.utils import color
from school.config import Config
import logging
import traceback
import qrcode

app = Flask(__name__)

@app.route('/user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('id')
    filter_param = request.args.get('filter')
    
    if filter_param == 'all':
        users = User.query.all()
        user_data = [user.toDict() for user in users]
        return jsonify(user_data)
    else:
        user_data = getUser(user_id, 2)
        return jsonify(user_data)

if __name__ == '__main__':
    app.run()

def getUser(userID: User, type: int) -> User:
    '''Returns a list with the group data by passing an ID
       type: 1 = list
             2 = dict
    '''
    
    try:
        user = User.query.filter_by(id=userID).first()
        match type:
            case 1:
                userData = user
            case 2:
                userData = user.toDict()

    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt get user")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        userData = None
    return userData