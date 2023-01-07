from flask_restful import Api
from flask import Flask
from flask_jwt_extended import JWTManager
import datetime
from register import register
from login import Login
from templte_create import template

application = Flask(__name__)
config = application.config
config.from_object('config')

api = Api(application)

jwt = JWTManager(application)

application.config['JWT_SECRET_KEY'] = 'template'
application.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=4)
application.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
application.config['PROPAGATE_EXCEPTIONS'] = True

api.add_resource(register, "/register")
api.add_resource(Login, "/login")
api.add_resource(template, "/template", "/template/<template_id>")

if __name__ == "__main__":
    application.run(debug=False)
