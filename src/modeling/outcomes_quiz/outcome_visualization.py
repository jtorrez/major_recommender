import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def make_hist_box_plot(df, column, box_ratio=0.15, hist_ratio=0.85):
    """
    Plots a combination box plot/histogram figure for a numerical column
    in a pandas dataframe.

    Parameters
    ----------
    df: pandas dataframe
        The pandas dataframe containing the data you'd like to Plots

    column: str
        The column name of the data you'd like to plot the distribution of

    box_ratio: float, optional, default=0.15
        The ratio of how large the box plot is to the size of the entire figure

    hist_ratio: float, optional, default=0.85
        The ratio of how large the histogram plot is to the size of the entire
        figure.

    Returns
    -------
    None

    Final line is plt.show()
    """
    sns.set(style="ticks")

    f, (ax_box, ax_hist) = plt.subplots(2,
                                        sharex=True,
                                        gridspec_kw={"height_ratios":
                                                     (box_ratio, hist_ratio)})

    sns.boxplot(df[column], ax=ax_box)
    sns.distplot(df[column], ax=ax_hist)

    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    plt.show()
