from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from school.config import Config
from flask_cors import CORS
from flask_session import Session
import logging
import json
from datetime import datetime
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)


# Configure logging
logging.basicConfig(level=logging.INFO,)
formatter = logging.Formatter(
    '%(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)


@ login_manager.user_loader
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config.from_object(Config)
    Session(app)
    CORS(app)

    # CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.app_context().push()

    from school.scrapper.routes import scrapper
    from school.tools.routes import tools
    from school.student.routes import student
    from school.groups.routes import groups

    app.config.from_object(Config)
    app.register_blueprint(scrapper)
    app.register_blueprint(tools)
    app.register_blueprint(student)
    app.register_blueprint(groups)

    return app
