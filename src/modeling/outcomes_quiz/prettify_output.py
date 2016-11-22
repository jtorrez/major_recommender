import pandas as pd
import numpy as np

prettified_columns = {'Major_category':'Major Category',
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
                 '75th Percentile Income (US$)',
                 'Risk Rating',
                 'Gain Rating',
                 'Probability of Your Interest']

def prettify_final_output(df, pretty_columns, final_columns):
    df['Unemployment Rate (%)'] = df.Unemployment_rate * 100
    df['Full Time Employment Rate (%)'] = df.full_time_employment_rate * 100
    df.rename(columns=pretty_columns, inplace=True)
    return df[final_columns]
