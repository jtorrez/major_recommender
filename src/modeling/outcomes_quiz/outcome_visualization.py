import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def make_hist_box_plot(df, column, box_ratio=0.15, hist_ratio=0.85):
    sns.set(style="ticks")

    f, (ax_box, ax_hist) = plt.subplots(2,
                                        sharex=True,
                                        gridspec_kw={"height_ratios": \
                                                      (box_ratio, hist_ratio)})

    sns.boxplot(df[column], ax=ax_box)
    sns.distplot(df[column], ax=ax_hist)

    ax_box.set(yticks=[])
    sns.despine(ax=ax_hist)
    sns.despine(ax=ax_box, left=True)
    plt.show()
