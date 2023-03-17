from jwt import encode, decode
from jwt import exceptions
from os import getenv
from datetime import datetime, timedelta
from school.tools.utils import *
import traceback
import logging


def expire_date(days: int) -> str:
    return datetime.utcnow() + timedelta(days=days)


def generate_token(data: dict) -> str:
    token = encode(payload={**data}, key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token: str, output: bool = False) -> str:
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        else:
            pass
    except exceptions.DecodeError as e:
        logging.error(
            f'{color(5,"Token validation failed")} ❌')

    except exceptions.ExpiredSignatureError as e:
        logging.error(
            f'{color(5,"Token expired")} ⌛')
