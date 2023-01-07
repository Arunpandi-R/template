import json
import sys

from flask import current_app as app, make_response, jsonify

from flask import request




def get_meta_data_json() -> dict:
    if 'json' in request.form:
        json_of_metadata = request.form.to_dict(flat=False)
        try:
            meta_data_from_json = json_of_metadata['json']
            meta_data_from_json_0 = meta_data_from_json[0]
            str_meta_data_from_json_0 = str(meta_data_from_json_0)
            meta_data_dict = json.loads(str_meta_data_from_json_0)
            app.logger.info('JSON Extracted')
        except Exception as e:
            tb = sys.exc_info()[2]

            return make_response(jsonify((
                'JSON data error',
                'Error in json request',
                400
            )), 400)
    else:
        if request.data is not None:
            try:
                my_json = request.data.decode('utf8').replace("'", '"')
                meta_data_dict = json.loads(my_json)
            except:
                app.logger.info('No JSON data passed')
                return make_response(jsonify((
                    'JSON data error',
                    'No JSON data passed',
                    400
                )), 400)
        else:
            app.logger.info('No JSON data passed')
            return make_response(jsonify((
                'JSON data error',
                'No JSON data passed',
                400
            )), 400)
    return meta_data_dict
