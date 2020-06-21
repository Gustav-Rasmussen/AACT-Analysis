"""
Run from terminal, prevent computer from sleeping (OSX):
cd /Users/gustavcollinrasmussen/PycharmProjects/aact_analysis
caffeinate -is python3 http_file_downloader.py
TODO: set up logging
"""

import glob
import io
import os
import requests
import shutil
from tqdm import tqdm
import zipfile

from analysis import get_filename_list, create_conditions_df, create_countries_df


def prepare_folders():
    # Create folders for analysis output
    if not os.path.isdir("etl_folder/conditions"):
        os.mkdir("etl_folder/conditions")
    if not os.path.isdir("etl_folder/countries"):
        os.mkdir("etl_folder/countries")
    # delete downloaded zip folder if exists
    if os.path.isdir("temp_download"):
        shutil.rmtree("temp_download")


def get_folder_and_unzip(filename):
    URL = r"https://aact.ctti-clinicaltrials.org/static/exported_files/monthly/{}".format(filename)
    r = requests.get(URL)  # get web content
    # translate downloaded content into byte stream
    z = zipfile.ZipFile(
        io.BytesIO(r.content)
    )
    # transform downloaded content into zip folder
    z.extractall("temp_download")


def preprocess(infile, func, outfile):
    df = func(infile)
    df.to_csv(outfile)


def get_data(list_of_filenames):
    for filename in tqdm(list_of_filenames):
        print(f"{filename = }")

        conditions_etl_file = "etl_folder/conditions/conditions_{}.csv".format(filename[:8])
        countries_etl_file = "etl_folder/countries/countries_{}.csv".format(filename[:8])

        has_conditions = glob.glob(conditions_etl_file)
        has_countries = glob.glob(countries_etl_file)

        if has_conditions and has_countries:
            continue

        get_folder_and_unzip(filename)

        # Analysis
        if not has_conditions:
            preprocess("temp_download/conditions.txt", create_conditions_df, conditions_etl_file)

        if not has_countries:
            preprocess("temp_download/countries.txt", create_countries_df, countries_etl_file)

        # delete downloaded zip folder
        shutil.rmtree("temp_download")


def main():
    prepare_folders()
    URL = r"https://aact.ctti-clinicaltrials.org/pipe_files"
    list_of_filenames = get_filename_list(URL)

    # datasets = ["conditions", "countries"]
    # for dataset in datasets:
    #     get_data(list_of_filenames, dataset)

    get_data(list_of_filenames)


if __name__ == "__main__":
    main()
