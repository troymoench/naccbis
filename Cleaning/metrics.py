""" This module provides metrics and related functions """
# Standard library imports
# Third party imports
import pandas as pd
# Local imports


def avg(data):
    return data["h"] / data["ab"]


def obp(data):
    numerator = data["h"] + data["bb"] + data["hbp"]
    denominator = data["ab"] + data["bb"] + data["hbp"] + data["sf"] + data["sh"]
    return numerator / denominator


def slg(data):
    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    return (x1b + 2*data["x2b"] + 3*data["x3b"] + 4*data["hr"]) / data["ab"]


def ops(data):
    return obp(data) + slg(data)


def iso(data):
    return (data["x2b"] + 2*data["x3b"] + 3*data["hr"]) / data["ab"]


def babip(data):
    return (data["h"] - data["hr"]) / (data["ab"] + data["sf"] - data["so"] - data["hr"])


def sar(data):
    """ Steal Attempt Rate
    :param data: A DataFrame
    :returns: A Series
    """
    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    return (data["sb"] + data["cs"]) / (data["hbp"] + data["bb"] + x1b)


def go_fo(data):
    return data["go"] / data["fo"]


def hbp_p(data):
    return data["hbp"] / data["pa"] * 100


def bb_p(data):
    return data["bb"] / data["pa"] * 100


def so_p(data):
    return data["so"] / data["pa"] * 100


def basic_offensive_metrics(data, inplace=False):
    """ Calculate basic offensive metrics. These metrics do not depend on league
    wide metrics.
    :param data: A DataFrame
    :param inplace: modify the DataFrame inplace?
    :returns: A DataFrame
    """
    if not inplace:
        data = data.copy()
    data["avg"] = avg(data)
    data["obp"] = obp(data)
    data["slg"] = slg(data)
    data["ops"] = ops(data)
    data["go_fo"] = go_fo(data)
    data["hbp_p"] = hbp_p(data)
    data["bb_p"] = bb_p(data)
    data["so_p"] = so_p(data)
    data["iso"] = iso(data)
    data["babip"] = babip(data)
    data["sar"] = sar(data)
    return data
