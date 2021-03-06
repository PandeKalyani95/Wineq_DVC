import yaml
import os
import json
import joblib
import numpy as np

params_path = "params.yaml"
schema_path = os.path.join("prediction_service","schema_in.json")

# "schema_in.json" which we stored in "/notebook dir"
# we will copy that model file into "/prediction_service/" dir

class NotInRange(Exception):
    def __init__(self, message = "Values entered are not in range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message = "Not in Columns"):
        self.message = message
        super().__init__(self.message)

def read_param(config_path = params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_param(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]

    try:
        # here we are using 3 and 8 because when we predict
        # so target variable have value range in between (min)3 to (max)8
        # that's why we check weather predicted output in between 3 and 8
        # if it is in betwen that range then it will work otherwise it will throw an error

        if 3<= prediction <=8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected Error"

def get_schema(schema_path = schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        # we were checking whether values in range or not
        # if it's not then raise and error
        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]):
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)

    return True

def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()

        # data in string formate we map into float
        data = [list(map(float, data))]
        response = predict(data)
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response":response}
            return response

    except NotInRange as e:
        response = {"the_expected_range":get_schema(), "response": str(e)}
        return response

    except NotInCols as e:
        response = {"the_expected_colls": get_schema().keys(), "response": str(e)}
        return response

    except Exception as e:
        response = {"response": str(e)}
        return response

