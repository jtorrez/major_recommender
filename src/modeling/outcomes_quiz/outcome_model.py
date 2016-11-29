from __future__ import division
import pandas as pd
import numpy as np
import outcome_cleaning as cl


def normalize_ratings(df, ratings_col):
    """
    Returns a normalized column by forcing all values between 0 and 1, then add
    1 to protect against ratings of zero.

    Parameters
    ----------
    df: pandas dataframe
        The dataframe containing the column to normalized
    ratings_col: str
        The name of the column to be normalized

    Returns
    -------
    norm_col: pandas Series
        A new column containing the normalized values of the input column
    """
    return cl.normalize_column(df, ratings_col) + 1


def calculate_j_metric(df, rt_score, id_score):
    """
    Returns calculated final match metric incoporating user's answers to risk
    and income gain questions.

    Parameters
    ----------
    df: pandas dataframe
        The dataframe containing the risk and gain scores for each majors

    rt_score: float
        The user's risk tolerance score

    id_score: float
        The user's income desire scores

    Returns
    -------
    final_metric: pandas Series column
        New column containing the final match metric based on the user's
        answesrs
    """
    return (rt_score * df.norm_risk_rating) + (id_score * df.norm_gain_rating)


def calculate_outcome_weight(df, j_metric_col):
    """
    Returns a normalized final_metric between 0 and 2.

    Normalizes final metric and then multiplies by 2 to force the range from
    0 to 2, so that poor matches are below 1 and reduce the probability of
    interest and good matches are above 1 and increase the probability of
    interest.

    Parameters
    ----------
    df: pandas dataframe
        The dataframe containing the final metric for each majors

    j_metric_col: str
        The name of the final metric column


    Returns
    -------
    final_metric: pandas Series column
        New column containing the normalized final match metric based on the
        user's answesrs
    """
    return cl.normalize_column(df, j_metric_col) * 2


def calculate_final_prob(df, rt_score, id_score, field_dict):
    """
    Returns a dataframe with the final probabilities of interest in each
    individual major calculated.

    Parameters
    ----------
    df: pandas dataframe
        The dataframe containing the the risk and gain ratings for each major

    rt_score: float
        The user's risk tolerance score

    id_score: float
        The user's income desire scores

    field_dict: dictionary
        Dictionary containing fields of study(str): predicted probability of
        interest(float) key-value pairs

    Returns
    -------
    df: pandas dataframe
        Final datframe containing probabilities of user's interest in each
        individual major
    """
    df['norm_risk_rating'] = normalize_ratings(df, 'risk_rating')
    df['norm_gain_rating'] = normalize_ratings(df, 'gain_rating')
    df['j_metric'] = calculate_j_metric(df, rt_score, id_score)
    df['final_metric'] = calculate_outcome_weight(df, 'j_metric')
    df['final_probs'] = df.apply(final_prob_mapper, args=(field_dict,),
                                 axis=1)
    return df


def final_prob_mapper(row, prob_field_dict):
    """
    Helper function that multiplies each field_of_study probability for an
    individual major by the final match metric.

    Parameters
    ----------
    row: pandas Series row
        Row from the dataframe

    prob_field_dict: dictionary
        Dictionary containing fields of study(str): predicted probability of
        interest(float) key-value pairs

    Returns
    -------
    final_prob: float
        The probability of interest multiplied by the final match metric
    """
    for field, proba in prob_field_dict.iteritems():
        if row['field_of_study'] == field:
            return row['final_metric'] * proba
        else:
            continue
