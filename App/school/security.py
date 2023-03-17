from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from flask import Flask, request, jsonify
from school import db, bcrypt
import logging
import uuid
import jwt
