# read the data from data source
# save it in the data/raw for further process

import os
from get_data import read_params, get_data
import argparse

def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)

    # there are some gaps between columns in dataset
    # that maybe create some issues that's why we chance col name

    new_cols = [col.replace(" ","_") for col in df.columns]
    # as we know there are space in beteen thw column name
    # we simply replace that space with "_"
    # Ex:- "first name" ---> "first_name"
    # print(new_cols)
    # path form patams.yaml for do changes in original file
    raw_data_path = config["load_data"]["raw_dataset_csv"]

    # now save that changes in new csv file
    df.to_csv(raw_data_path, sep = ",",index = False, header = new_cols)
    #print(df.head())

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="E:/Data Science/INeuron/PROJECTS/Wineq_Sample_Project/params.yaml")
    parsed_args = args.parse_args()
    path = parsed_args.config
    load_and_save(config_path=path)
