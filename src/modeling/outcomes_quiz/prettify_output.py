import pandas as pd
import numpy as np

prettified_columns = {'Major_category': 'Major Category',
                      'P25th': '25th Percentile Income (US$)',
                      'Median': 'Median Income (US$)',
                      'P75th': '75th Percentile Income (US$)',
                      'norm_risk_rating': 'Risk Rating',
                      'norm_gain_rating': 'Gain Rating',
                      'final_probs': 'Probability of Your Interest'
                      }

final_columns = ['Major',
                 'Major Category',
                 'Unemployment Rate (%)',
                 'Full Time Employment Rate (%)',
                 '25th Percentile Income (US$)',
                 'Median Income (US$)',
                 '75th Percentile Income (US$)']


def prettify_final_output(df, pretty_columns, final_columns, num_majors):
    """
    Returns a prettified version of the final dataframe for outputting to users

    Parameters
    ----------
    df: pandas dataframe
        Dataframe containing the final results of modeling the user's answers

    pretty_columns: dictionary
        Columns names to be cleaned up
        ugly_name(str): pretty_name(str) key-value pairs

    final_columns: list
        List of columns to included in final dataframe

    num_majors: int
        The number of majors to include in the outputting

    Returns
    -------
    pretty_df: pandas dataframe
        Dataframe with only the relevant, cleaned column names
    """
    df['Unemployment Rate (%)'] = df.Unemployment_rate * 100
    df['Full Time Employment Rate (%)'] = df.full_time_employment_rate * 100
    df.rename(columns=pretty_columns, inplace=True)
    return df[final_columns].head(num_majors)
