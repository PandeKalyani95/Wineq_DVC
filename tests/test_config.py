import json
import os
import joblib
import logging
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service


input_data = {
    # input data for incorrect range for independent variables

    "incorrect_range":
    {"fixed_acidity": 7897897,
    "volatile_acidity": 555,
    "citric_acid": 99,
    "residual_sugar": 99,
    "chlorides": 12,
    "free_sulfur_dioxide": 789,
    "total_sulfur_dioxide": 75,
    "density": 2,
    "pH": 33,
    "sulphates": 9,
    "alcohol": 9
    },

    # input data for correct range for independent variables

    "correct_range":
    {"fixed_acidity": 5,
    "volatile_acidity": 1,
    "citric_acid": 0.5,
    "residual_sugar": 10,
    "chlorides": 0.5,
    "free_sulfur_dioxide": 3,
    "total_sulfur_dioxide": 75,
    "density": 1,
    "pH": 3,
    "sulphates": 1,
    "alcohol": 9
    },

   # input data for incorrect range for independent variables

    "incorrect_col":
    {"fixed acidity": 5,
    "volatile acidity": 1,
    "citric acid": 0.5,
    "residual sugar": 10,
    "chlorides": 0.5,
    "free sulfur dioxide": 3,
    "total_sulfur dioxide": 75,
    "density": 1,
    "pH": 3,
    "sulphates": 1,
    "alcohol": 9
    }
}

# now input range for dependent(target) variable

TARGET_range = {
    "min": 3.0,
    "max": 8.0
}
# we have to copy "schema_in.json file from "/prediction_service" dir to in "/tests" dir
# now we are performing some test so we can restrict range of input/output range

# here we were testing TARGET value is in range or not
# now test for form_response (prediction_service.prediction)
# for testing it's passed or not use "pytest -v" command
def test_form_response_correct_range(data = input_data["correct_range"]):
    res = form_response(data)
    # assert means i have a condition and that must be true
    assert TARGET_range["min"] <= res <= TARGET_range["max"]


# here we were testing TARGET value is in range or not
# now test for api_response (prediction_service.prediction)
# for testing it's passed or not use "pytest -v" command
def test_api_response_correct_range(data = input_data["correct_range"]):
    res = api_response(data)
    # assert means i have a condition and that must be true
    assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]

# here we were testing independent values are in range or not
# now test for form_response (prediction_service.prediction)
# for testing it's passed or not use "pytest -v" command
def test_form_response_incorrect_range(data = input_data["incorrect_range"]):
    # whenever i am in "form_responses" and whenever i push the data in incorrect range
    # incorrect range for independent variables so at that time raise error (not in range)
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

# here we were testing independent values are in range or not
# now test for api_response (prediction_service.prediction)
# for testing it's passed or not use "pytest -v" command
def test_api_response_incorrect_range(data = input_data["incorrect_range"]):
    # whenever i am in "api_responses" and whenever i push the data in incorrect range
    # incorrect range for independent variables so at that time raise error (not in range)

    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message

# test for incorrct columns it will raise error(not in columns)
def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message
