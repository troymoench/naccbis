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


def pa(data):
    return data["ab"] + data["bb"] + data["hbp"] + data["sf"] + data["sh"]


def lob_p(data):
    """ LOB% = (H+BB+HBP-R)/(H+BB+HBP-(1.4*HR))
    :param
    :returns:
    """
    num = data["h"]+data["bb"]+data["hbp"]-data["r"]
    denom = data["h"]+data["bb"]+data["hbp"]-(1.4*data["hr"])
    return num / denom


def era(data):
    return data["er"] / data["ip"] * 9


def ra_9(data):
    return data["r"] / data["ip"] * 9


def so_9(data):
    return data["so"] / data["ip"] * 9


def bb_9(data):
    return data["bb"] / data["ip"] * 9


def hr_9(data):
    return data["hr"] / data["ip"] * 9


def whip(data):
    return (data["bb"] + data["h"]) / data["ip"]


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


def basic_pitching_metrics(data, conference=False, inplace=False):
    """ Calculate basic pitching metrics. These metrics do not depend on league
    wide metrics.
    :param data: A DataFrame
    :param conference: Omit metrics that cannot be calculated based on conference data
    :param inplace: modify the DataFrame inplace?
    :returns: A DataFrame
    """
    if not inplace:
        data = data.copy()
    if not conference:
        data["pa"] = pa(data)
        data["avg"] = avg(data)
        data["obp"] = obp(data)
        data["slg"] = slg(data)
        data["ops"] = ops(data)
        data["hbp_p"] = hbp_p(data)
        data["bb_p"] = bb_p(data)
        data["so_p"] = so_p(data)
        data["iso"] = iso(data)
        data["babip"] = babip(data)
        data["lob_p"] = lob_p(data)
    data["era"] = era(data)
    data["ra_9"] = ra_9(data)
    data["so_9"] = so_9(data)
    data["bb_9"] = bb_9(data)
    data["hr_9"] = hr_9(data)
    data["whip"] = whip(data)
    return data
