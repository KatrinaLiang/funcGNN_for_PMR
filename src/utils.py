"""Data processing utilities."""

import json
import math
from texttable import Texttable


def tab_printer(args):
    """
    Function to print the logs in a nice tabular format.
    :param args: Parameters used for the model.
    """
    args = vars(args)
    keys = sorted(args.keys())
    t = Texttable()
    t.add_rows([["Parameter", "Value"]])
    t.add_rows([[k.replace("_", " ").capitalize(), args[k]] for k in keys])
    print(t.draw())


def process_graph_from_json(path):
    """
    Reading a json file of a graph.
    :param path: Path to a JSON file.
    :return data: Dictionary with data.
    """
    data = json.load(open(path))
    return data


def calculate_loss(prediction, target):
    # TODO replace with binary cross entropy as loss function
    """
    Calculating the squared loss on the normalized GED.
    :param prediction: Predicted log value of GED.
    :param target: Actual log value of GED.
    :return score: Log Squared Error.
    """
    log_prediction = -math.log(prediction)
    log_target = -math.log(target)
    score = (log_prediction - log_target) ** 2
    return score

# def calculate_normalized_ged(data):
#     """
#     Calculating the normalized GED for a pair of graphs.
#     :param data: Data table.
#     :return norm_ged: Normalized GED score.
#     """
#     norm_ged = data["ged"]/(0.5*(len(data["labels_1"])+len(data["labels_2"])))
#     return norm_ged
