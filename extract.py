"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json
import sys
import helpers

from models import NearEarthObject, CloseApproach

from typing import List

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    result: List[NearEarthObject] = []
    with open(neo_csv_path, "r") as f:
        reader = csv.DictReader(f)
        fun = lambda entry: result.append(NearEarthObject(**entry))
        isunittesting = 'unittest' in sys.modules.keys()
        helpers.progress(
            reader,
            every=1000,
            fun=fun,
            start_text="Load neo data file",
            end_text="done.",
            suppress=isunittesting
        )
    return result


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    result: List[CloseApproach] = []
    with open(cad_json_path, "r") as f:
        cad = json.load(f)
        fields = cad["fields"]
        data = cad["data"]
        fun = lambda entry: result.append(CloseApproach(**dict(zip(fields, entry))))
        isunittesting = 'unittest' in sys.modules.keys()
        helpers.progress(
            data,
            every=15000,
            fun=fun,
            start_text="Load approaches data file",
            end_text="done.",
            suppress=isunittesting
        )
    return result
