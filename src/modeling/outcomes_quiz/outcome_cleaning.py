from __future__ import division
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import copy
import operator


def load_data(filename):
    """
    Returns a pandas dataframe loaded from a csv file.

    Parameters
    ----------
    filename: str
        The filename/path of the csv file to be loaded

    Returns
    -------
    df: pandas dataframe
    """
    return pd.read_csv(filename)


def drop_features(df):
    """
    Returns a dataframe where unnecessary rows have been dropped.

    Since this project wasn't concerned with non-4 year degree programs,
    I dropped all majors that were related to occupational technical degrees

    Would like to refactor this so that what will be dropped isn't hardcoded.

    Parameters
    ----------
    df: pandas dataframe
        Original pandas dataframe of raw data

    Returns
    -------
    df_copy: pandas dataframe
        Copy of original dataframe with appropriate rows dropped
    """
    df_copy = copy.deepcopy(df[df['Major_category'] !=
                            'Industrial Arts & Consumer Services'])
    return df_copy


def normalize_column(df, col):
    """
    Returns a normalized column by forcing all values between 0 and 1

    Parameters
    ----------
    df: pandas dataframe
        The dataframe containing the column to normalized
    col: str
        The name of the column to be normalized

    Returns
    -------
    norm_col: pandas Series
        A new column containing the normalized values of the input column
    """
    min_val = df[col].min()
    max_val = df[col].max()
    return (df[col] - min_val) / (max_val - min_val)


def add_features(df):
    """
    Returns same dataframe after adding featured engineered columns inplace
    to dataframe.

    Would like to refactor this so what is added isn't hardcoded.

    Parameters
    ----------
    df: pandas dataframe
        The original dataframe used in this project

    Returns
    -------
    df: pandas dataframe
        Original dataframe with added columns/features
    """
    df['full_time_employment_rate'] = (df['Employed_full_time_year_round'] /
                                       df['Employed'])
    df['pay_IQR_range'] = df['P75th'] - df['P25th']
    df['field_of_study'] = df.apply(field_majorcat_mapper, axis=1)
    df['norm_ur'] = normalize_column(df, 'Unemployment_rate')
    df['norm_ftr'] = normalize_column(df, 'full_time_employment_rate')
    df['norm_med_income'] = normalize_column(df, 'Median')
    df['norm_p25th_income'] = normalize_column(df, 'P25th')
    df['norm_p75th_income'] = normalize_column(df, 'P75th')
    df['risk_rating'] = (
                         (df.norm_ur - df.norm_ur.median()) +
                         (df.norm_ftr.median() - df.norm_ftr) +
                         (df.norm_p25th_income.median() - df.norm_p25th_income)
                         )
    df['gain_rating'] = (
                         (df.norm_med_income - df.norm_med_income.median()) +
                         (df.norm_p75th_income - df.norm_p75th_income.median())
                         )
    return df


def clean_and_engineer(df):
    """
    Returns a fully cleaned dataframe after dropping and adding features to
    the input raw dataframe.

    Parameters
    ----------
    df: pandas dataframe
        Raw dataframe for this project

    Returns
    -------
    final_df: pandas dataframe
        Copy of raw dataframe where appropriate features have been dropped and
        engineereed features have been added.
    """
    clean_df = drop_features(df)
    return add_features(clean_df)


def load_and_clean(filename):
    """
    Loads a csv file and returns a fully cleaned dataframe.

    Parameters
    ----------
    filename: str
        Filename/path of csv file containing raw data for project

    Returns
    -------
    cleaned_df: pandas dataframe
        Fully cleaned dataframe after dropping and adding features to
        the input file.
    """
    df = load_data(filename)
    return clean_and_engineer(df)


def load_clean_write(in_file, out_file):
    """
    Loads a csv file and writes a new csv file containing fully cleaned data.

    Parameters
    ----------
    in_file: str
        Filename/path of input csv file containing raw data for project.

    Returns
    -------
    out_file: str
        Filename/path of output csv file containing cleaned data for project.
    """
    df = load_and_clean(in_file)
    df.to_csv(out_file, index=False)
    return "Successly wrote file!"


def field_majorcat_mapper(series):
    """
    Returns the appropriate field_of_study based on the major_category of each
    individual major.

    Parameters
    ----------
    series: pandas Series row
        Row containing a Major_category column
    Returns
    -------
    field: str
        Field of study label
    """
    outcome_field_dict = get_outcome_field_dict()
    for field, major_cats in outcome_field_dict.iteritems():
        if series['Major_category'] in major_cats:
            return field


def get_outcome_field_dict():
    """
    Returns dictionary mapping field_of_study to major_category
    """
    outcome_field_dict = {

     'Business and Communication': {'Education',
                                    'Business',
                                    'Communications & Journalism'},

     'Creative Arts': {'Arts'},

     'Math, Sciences, and Engineering': {'Engineering',
                                         'Biology & Life Science',
                                         'Agriculture & Natural Resources',
                                         'Computers & Mathematics',
                                         'Physical Sciences'},

     'Public Service, Law, and Policy': {'Health',
                                         'Psychology & Social Work',
                                         'Law & Public Policy'},

     'Social Sciences': {'Social Science',
                         'Humanities & Liberal Arts',
                         'Interdisciplinary'}
     }

    return outcome_field_dict
