from pandas import read_csv, DataFrame, Categorical, Series
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('../../core')
import styles

TOTALPROGRAMS=38

colors = ['#1f78b4', '#33a02c'] # [icc, gcc]

NAMES = {
    "icc": "MPX (ICC)",
    "gcc": "MPX (GCC)",
}

xlim=(-0.5, 6.5)
ylim=(-4, 100)
xticks=range(0, 7, 1)
yticks=range(0, 110, 20)

df = read_csv("raw2.csv")
df["total2"] = 100.0*df["total2"]/TOTALPROGRAMS
df = df[["securitylevel", "compiler", "total2"]]
df.sort_values(["compiler", "securitylevel"], inplace=True, ascending=[False, True])

_, plot = plt.subplots()
labels = []
idx = 0
for key, grp in df.groupby(['compiler'], sort=False):
    plot = grp.plot(
        ax=plot,
        x="securitylevel",
        y="total2",
        kind="line",
        #            linestyle=styles.LINE_STYLES[idx],
        marker=styles.MARK_STYLES[idx],
        markersize=10,
        title="",
        xlim=xlim,
        xticks=xticks,
        ylim=ylim,
        yticks=yticks,
        figsize=(4, 3),
        linewidth=3,
        color=colors[idx]
    )
    labels.append(NAMES[key])
    idx += 1

lines, _ = plot.get_legend_handles_labels()
plot.legend(
    lines,
    labels,
    title=None,
    loc='upper left',
    frameon=False,
    ncol=1,
    labelspacing=0.5,
    columnspacing=1,
    borderpad=1,
    handlelength=2,
    fontsize=12,
)

style = styles.BasicStyle()
plot = style.apply(plot)
plot.xaxis.grid(True)

plot.tick_params(axis='both', which='major', labelsize=12)

plot.set_xlabel(r"MPX Security levels", fontsize=12)
plot.set_ylabel(r"Broken programs (%)", fontsize=12)

fig = plot.get_figure()
fig.savefig(
    "usability.pdf",
    dpi="figure",
    pad_inches=0.0,
    bbox_inches='tight'
)
