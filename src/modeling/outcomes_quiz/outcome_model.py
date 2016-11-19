from __future__ import division
import pandas as pd
import numpy as np
import outcome_cleaning as cl


def normalize_ratings(df, ratings_col):
    """
    Normalize ratings values between 0 and 1, then add 1 to protect against
    ratings of zero.
    """
    return cl.normalize_column(df, ratings_col) + 1

def calculate_j_metric(df, rt_score, id_score):
    """
    """
    return (rt_score * df.norm_risk_rating) + (id_score * df.norm_gain_rating)

def calculate_outcome_weight(df, j_metric_col):
    """
    Normalize j_metric between 0 and 1, multiply by 2 to force the range from
    0 to 2.
    """
    return cl.normalize_column(df, j_metric_col) * 2

def calculate_final_prob(df, rt_score, id_score, field_dict):
    """
    """
    df['norm_risk_rating'] = normalize_ratings(df, 'risk_rating')
    df['norm_gain_rating'] = normalize_ratings(df, 'gain_rating')
    df['j_metric'] = calculate_j_metric(df, rt_score, id_score)
    df['final_metric'] = calculate_outcome_weight(df, 'j_metric')
    df['final_probs'] = df.apply(final_prob_mapper, args=(field_dict,),
                                 axis = 1)
    return df

def final_prob_mapper(row, prob_field_dict):
    """
    """
    for field, proba in prob_field_dict.iteritems():
        if row['field_of_study'] == field:
            return row['final_metric'] * proba
        else:
            continue
