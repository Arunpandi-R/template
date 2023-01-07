import uuid

from flask_restful import Resource
from pymongo import MongoClient
from request_handler import get_meta_data_json
import config
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity


class template(Resource):
    @jwt_required()
    def __init__(self):
        client = MongoClient(
            "mongodb+srv://arun:Template34@cluster0.aiz6c35.mongodb.net/?retryWrites=true&w=majority")
        self.database = client.data_template

        self.data_base = None
        self.collections_data = None
        self.database_connection()

    def get(self, template_id=None):
        try:
            if template_id is None:
                template_data = self.collections_data.find({"_id": 0})
                return make_response(
                    jsonify({"message": "get all template", "result": template_data, "status_code": 200}), 200)

            else:
                template_data = self.collections_data.find_one({"template_id": template_id})
                return make_response(
                    jsonify({"message": "get all template", "result": [template_data], "status_code": 200}), 200)
        except Exception as e:
            return make_response(jsonify({"message": "database connection error", "result": [], "status_code": 400}),
                                 400)

    def post(self):
        try:
            meta_data = get_meta_data_json()
            data = dict()
            data["template_id"] = uuid.uuid4().hex
            data["template_name"] = meta_data.get("template_name", "")
            data["subject"] = meta_data.get("subject", "")
            data["body"] = meta_data.get("body", "")
            if data["template_name"] != "" or data["subject"] != "" or data["body"] != "":
                insert_data = self.collections_data.insert_one(data)
                if insert_data is not None:
                    del data["_id"]
                    return make_response(
                        jsonify({"message": "template create successfully", "result": [data], "status_code": 200}), 200)
                else:
                    pass

        except Exception as e:
            return make_response(jsonify({"message": "database connection error", "result": [], "status_code": 400}),
                                 400)

    def put(self, template_id=None):

        try:
            meta_data = get_meta_data_json()
            if template_id is not None:
                data = dict()
                find_data = self.collections_data.find_one({"template_id": template_id})
                data["template_name"] = meta_data.get("template_name", "")
                data["subject"] = meta_data.get("subject", "")
                data["body"] = meta_data.get("body", "")

                if find_data is not None:
                    if data["template_name"] != "" or data["subject"] != "" or data["body"] != "":
                        update_data = self.collections_data.update_one({"template_id": template_id},
                            {"$set": {"template_name": data["template_name"], "subject": data["subject"], "body": data["body"]}})
                        return make_response(jsonify({"message": "update successfully", "result": [data],
                                                      "status_code": 200}))

        except Exception as e:
            return make_response(jsonify({"message": "database connection error", "result": [], "status_code": 400}),
                                 400)

    def delete(self, template_id=None):
        try:
            find_data = self.collections_data.find_one({"template_id": template_id})
            if find_data is not None:
                delete_data = self.collections_data.delete_one({"template_id": template_id})
                return make_response(jsonify({"message": "delete successfully"}))
        except Exception as e:
            return make_response(jsonify({"message": "database connection error", "result": [], "status_code": 400}),
                                 400)

    def database_connection(self):

        if True:
            student_data_base = self.database[config.collection_name_2]
            self.collections_data = student_data_base
