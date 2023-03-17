from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from flask import Flask, request, jsonify
from school import db, bcrypt
import logging
import uuid
import jwt


def tokenRequired(arg) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(id=data['id']).first()
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            return func(current_user, *args, **kwargs)
        return wrapper
    if isinstance(arg, Callable):
        return decorator(arg)
    return decorator
