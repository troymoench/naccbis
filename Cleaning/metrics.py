""" This module provides metrics and related functions """
# Standard library imports
# Third party imports
import numpy as np
import pandas as pd
# Local imports


def avg(data):
    return data["h"] / data["ab"]


def obp(data):
    numerator = data["h"] + data["bb"] + data["hbp"]
    denominator = data["ab"] + data["bb"] + data["hbp"] + data["sf"]
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


# *********************
# * Advanced Metrics **
# *********************

def bsr(data, bmult=1.0):
    """ Base Runs
    BsR = A(B/(B+C)) + D
    requires ab, h, 2b, 3b, hr, bb, hbp, sf, sh, gdp, sb, cs
    """

    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]

    a = data["h"] + data["bb"] + data["hbp"] - data["hr"] - data["cs"] - data["gdp"]
    b = (.777*x1b + 2.61*data["x2b"] + 4.29*data["x3b"] + 2.43*data["hr"]
         + 0.03*(data["bb"] + data["hbp"]) + 1.30*data["sb"] + .13*data["cs"]
         + 1.08*data["sh"] + 1.81*data["sf"] + 0.70*data["gdp"] - 0.04*(data["ab"] - data["h"]))
    c = data["ab"] - data["h"] + data["sh"] + data["sf"]
    d = data["hr"]

    b = b*bmult

    return a*(b/(b+c)) + d


def bsr_bmult(data):
    """ Base Runs B multiplier """

    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]

    a = data["h"] + data["bb"] + data["hbp"] - data["hr"] - data["cs"] - data["gdp"]
    a = data["h"] + data["bb"] + data["hbp"] - data["hr"] - data["cs"] - data["gdp"]
    b = (.777*x1b + 2.61*data["x2b"] + 4.29*data["x3b"] + 2.43*data["hr"]
         + 0.03*(data["bb"] + data["hbp"]) + 1.30*data["sb"] + .13*data["cs"]
         + 1.08*data["sh"] + 1.81*data["sf"] + 0.70*data["gdp"] - 0.04*(data["ab"] - data["h"]))
    c = data["ab"] - data["h"] + data["sh"] + data["sf"]
    d = data["hr"]

    b_act = c*(d - data["r"])/(data["r"] - d - a)
    b_est = b
    return b_act/b_est


def linear_weights_incr(data, incr=0.00000001):
    """ Calculate Linear Weights using the increment method (plus one method)
    :param data: A Series with league totals
    :param incr: Increment value
    :returns: A Series with linear weights
    """

    cols = ["bb", "hbp", "ab", "h", "x2b", "x3b", "hr", "sb", "cs", "sf", "sh", "gdp"]
    v_input = data[cols]

    M_incr = pd.DataFrame([
                    [0, incr, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # hbp
                    [incr, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # bb
                    [0, 0, incr, incr, 0, 0, 0, 0, 0, 0, 0, 0],  # 1b
                    [0, 0, incr, incr, incr, 0, 0, 0, 0, 0, 0, 0],  # 2b
                    [0, 0, incr, incr, 0, incr, 0, 0, 0, 0, 0, 0],  # 3b
                    [0, 0, incr, incr, 0, 0, incr, 0, 0, 0, 0, 0],  # hr
                    [0, 0, 0, 0, 0, 0, 0, incr, 0, 0, 0, 0],  # sb
                    [0, 0, 0, 0, 0, 0, 0, 0, incr, 0, 0, 0],  # cs
                    [0, 0, incr, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # out
                    ], index=["lw_hbp", "lw_bb", "lw_x1b", "lw_x2b", "lw_x3b", "lw_hr", "lw_sb", "lw_cs", "lw_out"],
                    columns=cols)

    M_input = M_incr + v_input
    bmult = bsr_bmult(data)
    baseruns = bsr(data, bmult=bmult)

    # NOTE: The following are equivalent:
    # [(bsr(row, bmult) - baseruns) * (1 / incr) for _, row in M_input.iterrows()])
    return M_input.apply(lambda row: (bsr(row, bmult) - baseruns) * (1 / incr), axis=1)


def woba_weights(data, target):
    """ Calculate the woba weights for hbp, bb, 1b, 2b, 3b, hr
    :param
    :returns:
    """
    data = data.copy()
    data["x1b"] = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    lw = data.loc[:, "lw_hbp":"lw_out"]

    # subtract the value of the out
    lw = (lw.T - lw["lw_out"]).T

    lw.drop(columns=["lw_sb", "lw_cs", "lw_out"], inplace=True)
    lw.columns = ["hbp", "bb", "x1b", "x2b", "x3b", "hr"]

    totals = data[["hbp", "bb", "x1b", "x2b", "x3b", "hr"]]

    # calculate the dot product
    acc = totals.mul(lw).apply(np.sum, axis=1)
    raw = acc / data["pa"]
    scale = target / raw
    ww = (lw.T * scale).T
    ww.columns = ["ww_hbp", "ww_bb", "ww_x1b", "ww_x2b", "ww_x3b", "ww_hr"]
    ww["woba_scale"] = scale
    return ww


def woba(data, weights):
    """ Weighted On-Base Average (wOBA)
    :param data: DataFrame or Series of player, team, or league totals
    :param weights: DataFrame or Series of wOBA weights
    :returns: Series of wOBA values
    """
    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    return (weights["ww_hbp"]*data["hbp"] + weights["ww_bb"]*data["bb"] + weights["ww_x1b"]*x1b
            + weights["ww_x2b"]*data["x2b"] + weights["ww_x3b"]*data["x3b"]
            + weights["ww_hr"]*data["hr"]) / data["pa"]


def sbr(data, weights):
    """ Stolen Base Runs (SBR)
    SBR = runSB * SB + runCS * CS
    :param data: DataFrame or Series of player, team, or league totals
    :param weights: DataFrame or Series of linear weights
    :returns: Series of SBR values
    """
    return weights["lw_sb"]*data["sb"] + weights["lw_cs"]*data["cs"]


def lg_wsb(data, weights):
    """ lgwSB = (SB * runSB + CS * runCS) / (1B + BB + HBP – IBB)
    Used in the calculation of wSB.
    :param data: DataFrame or Series of league totals
    :param weights: DataFrame or Series of linear weights
    :returns: Series of lgwSB values
    """
    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    return ((weights["lw_sb"]*data["sb"] + weights["lw_cs"]*data["cs"])
            / (x1b + data["bb"] + data["hbp"]))


def wsb(data, lg_wsb):
    """ Weighted Stolen Base Runs (wSB)
    wSB = (SB * runSB) + (CS * runCS) – (lgwSB * (1B + BB + HBP – IBB))
    OR
    wSB = SBR - (lgwSB * (1B + BB + HBP – IBB))
    """
    x1b = data["h"] - data["x2b"] - data["x3b"] - data["hr"]
    return data["sbr"] - lg_wsb * (x1b + data["bb"] + data["hbp"])


def wraa(data, lg_woba, scale):
    """ Weighted Runs Above Average (wRAA)
    wRAA = ((wOBA - league wOBA) / wOBA scale) * PA
    :param
    :returns:
    """
    return ((data["woba"] - lg_woba) / scale) * data["pa"]


def off(data):
    """ Offensive Runs Above Average (OFF)
    OFF = wSB + wRAA
    :param
    :returns:
    """
    return data["wsb"] + data["wraa"]


def wrc(data, lg_woba, woba_scale, lg_r_pa):
    """ Weighted Runs Created (wRC)
    wRC = (((wOBA - league wOBA)/wOBA Scale) + (league R/PA))*PA
    :param
    :returns:
    """
    return (((data["woba"] - lg_woba) / woba_scale) + lg_r_pa) * data["pa"]


def wrc_p(data, lg_r_pa):
    """ Weighted Runs Created Plus (wRC+)
    Official formula:
    wRC+ = (((wRAA/PA + lgR/PA) + (lgR/PA - (park factor * lgR/PA))) / lgwRC/PA excluding pitchers)*100
    For our purposes:
    wRC+ = (((wRAA/PA) + lgR/PA) / lgR/PA)*100
    :param
    :returns:
    """
    return (((data["wraa"] / data["pa"]) + lg_r_pa) / lg_r_pa)*100


def off_p(data, lg_r_pa):
    """ Offensive Runs Plus (OFF+)
    OFF+ = (((OFF/PA) + lgR/PA) / lgR/PA)*100
    :param
    :returns:
    """
    return (((data["off"] / data["pa"]) + lg_r_pa) / lg_r_pa)*100


def rar(data, replacement_level):
    """ Runs Above Replacement (RAR)
    RAR = OFF - (repl level * PA)
    :param
    :returns:
    """
    return data["off"] - (replacement_level * data["pa"])


def multi_season(data, totals, func, inplace=False):
    """ Calculate metrics for multiple seasons
    :param
    :returns:
    """
    if not inplace:
        data = data.copy()

    new_totals = totals.copy()
    if new_totals.index.name != "season":
        new_totals = new_totals.set_index("season")

    df = pd.DataFrame()
    for name, group in data.groupby("season"):
        temp = pd.DataFrame(group)

        # totals_season must be a Series
        totals_season = new_totals.loc[name]
        temp = func(temp, totals_season)
        df = df.append(temp)

    return df


def season_offensive_metrics(data, totals_season):
    """ Calculate offensive metrics for a single season
    :param data: A DataFrame of single season data
    :param totals_season: A Series of league totals
    :returns: A DataFrame
    """
    if not isinstance(totals_season, pd.Series):
        raise TypeError("Expected {}. Got {}.".format(pd.Series, type(totals_season)))
    temp = data.copy()
    temp["sbr"] = sbr(temp, totals_season)
    temp["wsb"] = wsb(temp, totals_season["lg_wsb"])
    temp["woba"] = woba(temp, totals_season)
    temp["wraa"] = wraa(temp, totals_season["woba"], totals_season["woba_scale"])
    temp["off"] = off(temp)
    temp["wrc"] = wrc(temp, totals_season["woba"], totals_season["woba_scale"], totals_season["lg_r_pa"])
    temp["wrc_p"] = wrc_p(temp, totals_season["lg_r_pa"])
    temp["off_p"] = off_p(temp, totals_season["lg_r_pa"])
    return temp


def advanced_offensive_metrics(data, totals, inplace=False):
    """ Calculate advanced offensive metrics. These metrics do depend on league
    wide metrics.
    :param data: A DataFrame
    :param totals: A DataFrame of league wide totals and weights
    :param inplace: modify the DataFrame inplace?
    :returns: A DataFrame
    """
    if not inplace:
        data = data.copy()

    new_totals = totals.copy()
    if new_totals.index.name != "season":
        new_totals = new_totals.set_index("season")

    df = pd.DataFrame()
    for name, group in data.groupby("season"):
        temp = pd.DataFrame(group)

        # totals_season must be a Series
        totals_season = new_totals.loc[name]
        temp["sbr"] = sbr(group, totals_season)
        temp["wsb"] = wsb(temp, totals_season["lg_wsb"])
        temp["woba"] = woba(temp, totals_season)
        temp["wraa"] = wraa(temp, totals_season["woba"], totals_season["woba_scale"])
        temp["off"] = off(temp)
        temp["wrc"] = wrc(temp, totals_season["woba"], totals_season["woba_scale"], totals_season["lg_r_pa"])
        temp["wrc_p"] = wrc_p(temp, totals_season["lg_r_pa"])
        temp["off_p"] = off_p(temp, totals_season["lg_r_pa"])
        df = df.append(temp)

    return df
