from datetime import datetime, timedelta
from school import Config
from school.models import User
from functools import wraps
from typing import Callable
from flask import Flask, request, jsonify
from school.tools.utils import color
import logging
import jwt
import traceback


def tokenRequired(func) -> Callable:
    '''Decorator to check if the user has a valid token'''
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token,
                       Config.SECRET_KEY,
                       algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(*args, **kwargs)

    return decorator


def encodeJwtToken(user: dict[str, str]) -> dict[str, str]:
    '''Encodes a user object into a JWT token'''
    try:
        if user:
            token = jwt.encode({
                'public_id': user['id'],
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'lastName': user['lastName'],
                    'email': user['email'],
                    'profileID': user['profileID'],
                    'exp': str(datetime.utcnow() + timedelta(days=50))
                }
            },
                Config.SECRET_KEY,
                algorithm='HS256')
        else:
            raise ValueError(f'{color(3,"User object is empty")}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt encode token")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        token = None

    return token
