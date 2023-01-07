from flask_restful import Resource
from pymongo import MongoClient
from request_handler import get_meta_data_json
import config
import re

import encodings
import uuid
from flask import jsonify, make_response


class register(Resource):

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.user_email_id = ""
        self.password = ""
        client = MongoClient(
            "mongodb+srv://arun:Template34@cluster0.aiz6c35.mongodb.net/?retryWrites=true&w=majority")
        self.database = client.data_template


        # self.database = self.client.test

    def post(self):

        if True:
            student_data_base = self.database[config.collection_name_1]
            student_collections_data = student_data_base
        result = student_collections_data.find({}, {"_id": 0})

        meta_data = get_meta_data_json()
        self.first_name = meta_data.get("first_name", "")
        self.last_name = meta_data.get("last_name", "")
        self.user_email_id = meta_data.get("email", "")
        self.password = meta_data.get("password", "")

        mail_match = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        pass_word_match = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?& ])[A-Za-z\d@$!#%*?&]{8,18}$")

        if re.match(mail_match, self.user_email_id) and re.split(pass_word_match, self.password):
            find_name = student_collections_data.find_one({"email": self.user_email_id})
            if find_name is None:
                data = dict()

                data["first_name"] = self.first_name
                data["last_name"] = self.last_name
                data["user_id"] = uuid.uuid4().hex
                data["email"] = self.user_email_id
                data["password"] = self.password

                student_collections_data.insert_one(data)
                return make_response(jsonify({"message": "Successfully create user", "result": [], "status_code": 200}))
            else:
                return make_response(jsonify({"message": "this email id is all ready exist"}))
        else:
            return make_response(jsonify({"message": ""}))

