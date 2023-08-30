from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from school.config import Config
from flask_cors import CORS
from flask_session import Session
import logging
import json
from datetime import datetime
db = SQLAlchemy()
bcrypt = Bcrypt()


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


def create_app():
    """
    This function creates the app and returns it to the user,
    also it registers the blueprints to the app by calling the
    register_blueprint function
    """
    
    # Define the WSGI application object and initialize the app
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config.from_object(Config)
    Session(app)
    CORS(app)
    # csrf.init_app(app)

    # CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Define the database object which is imported
    db.init_app(app)
    bcrypt.init_app(app)

    app.app_context().push()

    # Import a module / component using its blueprint handler variable (mod_auth)
    from school.scrapper.routes import scrapper
    from school.tools.routes import tools
    from school.user.routes import user
    from school.groups.routes import groups
    from school.login.routes import login
    #from school.nodes.routes import nodes
    from school.schedule.routes import schedule
    from school.teacher.routes import teacher
    from school.dashboard.routes import dashboard

    # Here is where you register your blueprints to the app
    app.config.from_object(Config)
    app.register_blueprint(scrapper)
    app.register_blueprint(tools)
    app.register_blueprint(user)
    app.register_blueprint(groups)
    app.register_blueprint(login)
    #app.register_blueprint(nodes)
    app.register_blueprint(schedule)
    app.register_blueprint(teacher)
    app.register_blueprint(dashboard)

    return app
