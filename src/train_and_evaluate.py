# load train and test files
# train the algo
# save the metrices, params

import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_params
import argparse
import joblib
import json
import mlflow
from urllib.parse import urlparse

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    # get path from params.yaml file
    # here we need the path for load the data so we can do process on it and create a model
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    random_state =  config["base"]["random_state"]
    model_dir = config["model_dir"]

    # hyper-parameters
    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]

    target = config["base"]["target_col"]

    # load train and test data
    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    # separating dependent and independent variables

    #dependent variable
    train_y = train[target]
    test_y = test[target]

    #independent variable
    train_x = train.drop(columns=[target], axis=1)
    test_x = test.drop(columns=[target], axis=1)

############################ MLFLOW ##########################

    # getting path from params.yaml
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)

    # we already set a experiment name in params.yaml
    # if we not set experiment name so mlflow will create default name
    mlflow.set_experiment(mlflow_config["experiment_name"])

    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:

        # creating model
        eln = ElasticNet(alpha=alpha, l1_ratio = l1_ratio, random_state=random_state)
        eln.fit(train_x, train_y)

        # prediction
        pred_y = eln.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, pred_y)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # we need this for tracking uri it will check whether this server on or not
        # if it is on then it will login into database
        # if it it not on so it will create a folder for you by default
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                eln,
                "model",
                registered_model_name=mlflow_config["registered_model_name"])
        else:
            mlflow.sklearn.load_model(eln, "model")

    # print("ElasticNet Model (alpha=%f, l1_ratio=%f): " %(alpha, l1_ratio))
    # print(" RMSE : %s" % rmse)
    # print(" MAE  : %s" % mae)
    # print(" R2   : %a" %r2)

    # getting path from params.yaml file
    # scores_file = config["reports"]["scores"]
    # params_file = config["reports"]["params"]


    # with open(scores_file, "w") as f:
    #     scores = {"rmse":rmse, "mae":mae, "r2": r2}
    #     # dump data into scores_files
    #     json.dump(scores, f, indent=4)
    #
    # with open(params_file, "w") as f:
    #     params = {"alpha":alpha, "l1_ratio":l1_ratio}
    #     # dump data into params_files
    #     json.dump(params, f, indent=4)

##########################################################################
##########################################################################

    # os.makedirs(model_dir, exist_ok=True)
    # model_path = os.path.join(model_dir, "model.joblib")
    #
    # # dump file into model_dir
    # joblib.dump(eln, model_path)
    # #print("model saved !")


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/Data Science/INeuron/PROJECTS/Wineq_Sample_Project/params.yaml")
    parsed_args = args.parse_args()
    path = parsed_args.config
    train_and_evaluate(config_path=path)