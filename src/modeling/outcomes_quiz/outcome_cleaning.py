from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import operator


def load_data(filename):
    return pd.read_csv(filename)

def drop_features(df):
    df_copy = copy.deepcopy(df[df['Major_category'] != 'Industrial Arts & Consumer Services'])
    return df_copy

def add_features(df):
    df['full_time_employment_rate'] = df['Employed_full_time_year_round'] / df['Employed']
    df['pay_IQR_range'] = df['P75th'] - df['P25th']
    df['field_of_study'] = df.apply(field_majorcat_mapper, axis=1)
    return df

def clean_and_engineer(df):
    clean_df = drop_features(df)
    return add_features(clean_df)

def load_and_clean(filename):
    df = load_data(filename)
    return clean_and_engineer(df)

def field_majorcat_mapper(series):
    outcome_field_dict = get_outcome_field_dict()
    for field, major_cats in outcome_field_dict.iteritems():
        if series['Major_category'] in major_cats:
            return field

def get_outcome_field_dict():
    outcome_field_dict = {

    'Business and Communication': {'Education', 'Business',
    'Communications & Journalism'},

    'Creative Arts': {'Arts'},

     'Math, Sciences, and Engineering': {'Engineering',
     'Biology & Life Science', 'Agriculture & Natural Resources',
     'Computers & Mathematics', 'Physical Sciences'},

     'Public Service, Law, and Policy': {'Health', 'Psychology & Social Work',
     'Law & Public Policy'},

     'Social Sciences': {'Social Science', 'Humanities & Liberal Arts',
     'Interdisciplinary'}}

    return outcome_field_dict
