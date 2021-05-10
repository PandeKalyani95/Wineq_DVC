# whichever perform will molde
# or we can say that whichever model/experiment have less orror term
# so once we get the model with less error values so we will put that model into production
# so that we can log that model and copy that model in
# "/prediction_service/model" dir
# so what will happen so whenever we will productionize our model
# or whenever we push ouw changes so that model which was very better
# or the model which was choosen by the us for production
# so that model will replace with model which is present inside the folder "/prediction_service/model"
# and it will happen when we run this py file

from src.get_data import read_params
import argparse
import mlflow
from mlflow.tracking import MlflowClient

# if we want to print something in specific way so we use pprint()
# The pprint module provides a capability to “pretty-print” arbitrary Python
# data structures in a form which can be used as input to the interpreter.
from pprint import pprint
import joblib
import os


def log_production_model(config_path):
    config = read_params(config_path)

    mlflow_config = config["mlflow_config"]
    model_name = mlflow_config["registered_model_name"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_registry_uri(remote_server_uri)
    runs = mlflow.search_runs(experiment_ids=1)

    # here we are sort the "mae" metrics and store lowest mae in lowest variable
    lowest = runs["metrics.mae"].sort_values(ascending=True)[0]

    # we need lowest mae id also so we check here that for corresponding lowest mae
    lowest_run_id = runs[runs["metrics.mae"] == lowest]["run_id"][0]

    client = MlflowClient()
    for mv in client.search_model_versions(f"name='{model_name}'"):
        mv = dict(mv)

        if mv["run_id"] == lowest_run_id:
            current_version = mv["version"]
            logged_model = mv["source"]
            print(mv, indent=4)
            client.transition_model_version_stage(
                name=model_name,
                version=current_version,
                stage="Production"
            )
        else:
            current_version = mv["version"]
            client.transition_model_version_stage(
                name=model_name,
                version=current_version,
                stage="Staging"
            )

    loaded_model = mlflow.pyfunc.log_model(logged_model)
    model_path = config["webapp_model_dir"]  # /prediction_service/model
    joblib.dump(loaded_model, model_path)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/Data Science/INeuron/PROJECTS/Wineq_Sample_Project/params.yaml")
    parsed_args = args.parse_args()
    path = parsed_args.config
    data = log_production_model(config_path=path)