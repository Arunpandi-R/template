from flask_restful import Resource
from pymongo import MongoClient
from request_handler import get_meta_data_json
import config
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


class Login(Resource):

    def __init__(self):
        self.user_email_id = ""
        self.password = ""
        client = MongoClient(
            "mongodb+srv://arun:Template34@cluster0.aiz6c35.mongodb.net/?retryWrites=true&w=majority")
        self.database = client.data_template
    def post(self):
        try:
            meta_data = get_meta_data_json()
            if True:
                student_data_base = self.database[config.collection_name_1]
                student_collections_data = student_data_base
            self.user_email_id = meta_data.get("email", "")
            self.password = meta_data.get("password", "")
            if self.user_email_id != "" and self.password != "":
                result = student_collections_data.find_one({"email": self.user_email_id, "password": self.password}, {"_id": 0})
                if result is not None:
                    ret = {
                        'access_token': create_access_token(identity=self.user_email_id),
                        'refresh_token': create_refresh_token(identity=self.user_email_id),
                        'status_code': 200
                    }
                    return make_response(jsonify(ret), 200)
                else:
                    return make_response(jsonify({"message": "please register for your details", "result": [],
                                                  "status_code": 400}), 400)
            else:
                return make_response(jsonify({"message": "please enter user mail id and password", "result":[],
                                              "status_code": 400}), 400)
        except Exception as e:
            return make_response(jsonify({"message": "database connection error", "result": [], "status_code": 400}), 400)