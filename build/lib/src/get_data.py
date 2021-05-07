# read params
# process
# return dataframe
# import os
from argparse import Namespace

import yaml
import pandas as pd
import argparse


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def get_data(config_path):
    config = read_params(config_path)
    # print(config)
    data_path = config["data_source"]["s3_source"]
    #print(data_path)
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    return df


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/Data Science/INeuron/PROJECTS/Wineq_Sample_Project/params.yaml")
    parsed_args = args.parse_args()
    file_path = parsed_args.config
    #rint(file_path)
    data = get_data(config_path=file_path)

