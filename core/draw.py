"""
Drawing plots
"""
import logging
import csv
from abc import ABCMeta, abstractmethod, abstractproperty

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from scipy.stats import trim_mean
from scipy.stats.mstats import mode, gmean, hmean

from core import prepare
from core import styles


class FexPlot:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.df = None
        self.plot = None

    @abstractproperty
    def StyleClass(self):
        pass

    @abstractmethod
    def get_data(self, df, columns):
        pass

    @abstractmethod
    def build_plot(self):
        pass

    def save_plot(self, filename="generic_name.pdf"):
        logging.info("Saving plot")
        fig = self.plot.get_figure()
        fig.savefig(
            filename,
            dpi="figure",
            pad_inches=0.0,
            bbox_inches='tight'
        )


class LinePlotTput(FexPlot):
    StyleClass = styles.LinePlotStyle

    def __init__(self):
        self.current_subplot = None
        super(LinePlotTput, self).__init__()

    def get_data(self, df, columns):
        """
        Remove redundant data
        """
        self.df = df.dropna()
        self.df = self.df[["compilertype", "num_clients", "tput", "lat"]]
        self.df.sort_values(["compilertype", "num_clients"], inplace=True)
        logging.debug(self.df)

    def build_plot(self,
                   xlabel=r"Throughput ($\times 10^3$ msg/s)", ylabel="Latency (ms)",
                   legend_loc='upper left',
                   figsize=(4, 3),
                   subplot=None,
                   build_names="short",
                   **kwargs):
        logging.info("Building plot")

        style = self.StyleClass()

        # create a canvas
        plot = subplot
        if not plot:
            _, plot = plt.subplots()

        # draw lines, one build type at a time
        labels = []
        idx = 0
        for key, grp in self.df.groupby(['compilertype']):
            if not grp.empty:
                plot = grp.plot(
                    ax=plot,
                    x="tput",
                    y="lat",
                    kind="line",
                    #            linestyle=styles.LINE_STYLES[idx],
                    marker=styles.MARK_STYLES[idx],
                    markersize=8,
                    color=style.colors[idx],
                    title="",
                    figsize=figsize,
                    linewidth=3,
                    **kwargs
                )
                labels.append(prepare.BUILD_NAMES[build_names][key])
                idx += 1

        # get line styles for legend
        lines, _ = plot.get_legend_handles_labels()

        # apply other styles
        plot = style.apply(plot)
        plot = style.legend(plot, lines, labels, legend_loc)
        plot.xaxis.grid(True)

        plot.tick_params(axis='both', which='major', labelsize=12)

        plot.set_xlabel(xlabel, fontsize=14)
        plot.set_ylabel(ylabel, fontsize=14)

        # save the resulting plot as an object property
        self.plot = plot
        self.current_subplot = subplot

    def get_current_subplot(self):
        return self.current_subplot


class BarplotOverhead(FexPlot):
    StyleClass = styles.BarplotStyle

    def get_data(self, df, columns, margins=True):
        # leave only the required columns
        self.df = df.dropna()
        self.df = self.df[["name", "overhead", "compilertype"]]

        # restructure and better-name table
        self.df = self.df.pivot_table(
            index="name",
            columns="compilertype",
            values="overhead",
            margins=margins,
            aggfunc=gmean,   #np.mean,
            margins_name="mean"
        )

        # remove mean row values and leave only column means
        if margins:
            self.df.drop("mean", 1, inplace=True)

        # print the resulting table in debug mode
        logging.debug(self.df)
#        self.df.to_csv("tmp.csv", quoting=csv.QUOTE_NONNUMERIC)

    def build_plot(self,
                   xlabel="", ylabel="Overhead w.r.t. native",
                   legend_loc=None,
                   figsize=(12, 2),
                   text_points=(),
                   vline_position=6,
                   title="",
                   ncol=5,
                   build_names="short",
                   **kwargs):

        # rename builds
        self.df.rename(columns=prepare.BUILD_NAMES[build_names], inplace=True)

        logging.info("Building plot")

        style = self.StyleClass(legend_ncol=ncol, legend_loc=legend_loc)
        plot = self.df.plot(
            kind="bar",
            figsize=figsize,
            linewidth=0.5,
            edgecolor=style.bar_edge_color,
            color=style.colors,
            title=title,
            **kwargs
        )
        plot = style.apply(plot)

        if kwargs.get("logy", False) == True:
            plot.set_yscale('log', basey=2)
            plot.yaxis.set_major_formatter(plticker.LogFormatter(base=2))

        # parametrize labels
        plot.set_ylabel(ylabel, fontsize=10)
        plot.set_xlabel("", fontsize=0)  # remove x label

        # vertical line - usually, a delimiter for mean values
        plot.axvline(vline_position, linewidth=0.9, color='grey', dashes=[3, 3])

        # additional text
        for point in text_points:
            plot.text(point[0], point[1], point[2], fontsize=8)

        # save the resulting plot as an object property
        self.plot = plot


class BarplotMultithreaded(BarplotOverhead):
    StyleClass = styles.BarplotMultithreadedStyle


class BarplotWithNative(BarplotOverhead):
    StyleClass = styles.BarplotWithNativeStyle


class BarplotMPXFature(BarplotOverhead):
    StyleClass = styles.BarplotMPXFatureStyle


class BarplotClusteredStacked(FexPlot):
    StyleClass = styles.BarplotClusteredStyle

    def get_data(self, df, columns):
        """
        Remove redundant data
        """
        self.df = df[["name", "compilertype"] + columns]
        self.columns = columns
        logging.debug(df)
#        self.df.to_csv("tmp.csv", quoting=csv.QUOTE_NONNUMERIC)

    def build_plot(self,
                   xlabels=(), ylabel="[ylabel not specified]",
                   legend_loc="",
                   figsize=(12, 2.35),
                   text_points=(),
                   vline_position=0,
                   title="",
                   df_callback=None,
                   df_callback_args=(),
                   **kwargs):

        logging.info("Building plot")

        # prepare a plot canvas
        plot = plt.subplot(111)
        style = self.StyleClass(need_hatching=False)

        # get build types and rename
        xlabels = [prepare.BUILD_NAMES["long"].get(l, l) for l in xlabels]

        # builds clusters
        df_bars = [g for _, g in self.df.groupby('compilertype')]
        for index, df_bar in enumerate(df_bars):

            # restructure and better-name table
            df_bar.reindex(index=["name"], columns=self.columns)
            if df_callback:
                df_callback(df_bar, *df_callback_args)

            df_bar.plot(
                kind="bar",
                linewidth=1,
                stacked=True,
                ax=plot,
                legend=False,
                figsize=figsize,
                edgecolor=style.bar_edge_color,
                color=style.colors,
                title=title,
                **kwargs
            )

            df_bars[index] = df_bar

        plot = style.apply(plot)

        # bar labels
        self.shorten_bar_names(plot, xlabels, self.columns, df_bars, style.hatches)

        # axis labels
        n_ind = len(df_bars[0].index)
        plot.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(len(df_bars) + 1)) / 2.)
        plot.set_xticklabels(df_bars[0]["name"], rotation=0)
        plot.xaxis.set_tick_params(pad=7)

        plot.set_ylabel(ylabel, fontsize=10)
        plot.set_xlabel("", fontsize=0)  # remove x label

        # legend
        self.add_stacked_legend(plot, xlabels, self.columns, df_bars)

        # align subplots
        plt.subplots_adjust(left=0.07, right=0.86, top=0.95, bottom=0.14)

        # save the resulting plot as an object property
        self.plot = plot

    @staticmethod
    def shorten_bar_names(plot, labels, columns, df_bars, hatches):
        # x coords of this transformation are data, and y coord are axes
        trans = plot.get_xaxis_transform()

        n_df = len(df_bars)
        n_col = len(columns)

        drawn_texts = {}
        h, l = plot.get_legend_handles_labels()  # get the handles we want to modify
        for i in range(0, n_df * n_col, n_col):  # len(h) = n_col * n_df
            for j, pa in enumerate(h[i:i + n_col]):
                for k, rect in enumerate(pa.patches):  # for each index
                    label_ind = int(i / n_col)
                    rect.set_x(rect.get_x() + 1 / float(n_df + 2) * i / float(n_col))
                    if hatches:
                        rect.set_hatch(hatches[j] * 3)
                    rect.set_width(1 / float(n_df + 2))

                    if labels and (k, label_ind) not in drawn_texts:
                        plot.text(
                            rect.get_x() + rect.get_width() / 2.0,  # x - in the middle of the bar
                            -0.07,
                            compilertype_tinynames(labels[label_ind]),
                            fontsize=6,
                            ha='center',
                            va='bottom',
                            transform=trans
                        )
                        drawn_texts[(k, label_ind)] = True
        return plot

    @staticmethod
    def add_stacked_legend(plot, labels, columns, df_bars):
        h, l = plot.get_legend_handles_labels()
        n_df = len(df_bars)
        n_col = len(columns)

        # stack names
        l1 = plot.legend(
            h[:n_col],
            l[:n_col],
            loc=[1.005, 0.455],
            handlelength=0.7,
            labelspacing=0.3,
            fontsize=10
        )
        l1.get_frame().set_facecolor('white')

        # bar names
        if labels:
            slabels = ""
            stinynames = ""
            for i in range(0, n_df):
                slabels += labels[i] + "\n"
                stinynames += compilertype_tinynames(labels[i]) + "\n"
            plot.text(1.010, -0.09, stinynames, fontsize=10, transform=plot.transAxes)
            plot.text(1.040, -0.09, slabels, fontsize=10, transform=plot.transAxes)

        plot.add_artist(l1)

        return plot


class VarBarplotOverhead(FexPlot):
    StyleClass = styles.VarInputBarStyle

    def get_data(self, df, columns, margins=True, build_names="short"):
        df = df.dropna()
        self.df = df[["name", "overhead", "compilertype", "input"]]

        # print the resulting table in debug mode
        logging.debug(self.df)
#        self.df.to_csv("tmp.csv", quoting=csv.QUOTE_NONNUMERIC)

    def build_plot(self,
                   xlabel="", ylabel="Overhead w.r.t. native",
                   legend_loc="",
                   figsize=(12, 2),
                   text_points=(),
                   vline_position=6,
                   title="",
                   ncol=1,
                   **kwargs):

        logging.info("Building plot")

        # prepare a plot canvas
        fig, plot = plt.subplots(1, 4, figsize=figsize, sharey=True)
        plt.subplots_adjust(wspace=0.04, hspace=0.04)

        # set common y label
        plot[0].set_ylabel(ylabel, fontsize=10)

        # draw the subplots
        for i, (name, group) in enumerate(self.df.groupby("name")):
            # restructure subplot data
            group = group.dropna()
            group = group.pivot_table(index="compilertype", columns="input", values="overhead", margins=False)
            group.rename(columns=prepare.INPUT_NAMES["long"], inplace=True)
            group.rename(index=prepare.BUILD_NAMES["short"], inplace=True)

            style = self.StyleClass(need_hatching=False)
            subplot = group.plot(
                kind="bar",
                linewidth=0.5,
                edgecolor="black",
                color=style.colors,
                ax=plot[i],
                legend=False,
                title=name,
                **kwargs
            )

            if kwargs.get("logy", False) == True:
                subplot.set_yscale('log', basey=2)
                subplot.yaxis.set_major_formatter(plticker.LogFormatter(base=2))

            subplot = style.apply(subplot)
            subplot.set_xlabel("", fontsize=0)  # remove x label

        # get handles and labels for the shared legend
        h, l = subplot.get_legend_handles_labels()

        # common legend
        fig.legend(
            h,
            l,
            title="",
            bbox_to_anchor=(0.13, 0.9),
            frameon=False,
            ncol=ncol,
            labelspacing=0.5,
            columnspacing=0,
            borderpad=0,
            handlelength=0.7,
            fontsize=10
        )

        # additional text
        for point in text_points:
            plt.text(point[0], point[1], point[2], fontsize=8)

        # common title
        plt.suptitle(title, fontsize=10, fontweight='bold')

        self.plot = fig

    def save_plot(self, filename="generic_name.pdf"):
        logging.info("Saving plot")
        self.plot.savefig(
            filename,
            dpi="figure",
            pad_inches=0.0,
            bbox_inches='tight'
        )


# Helper functions
def compilertype_tinynames(compilertype):
    return prepare.BUILD_NAMES["tiny"].get(compilertype, compilertype)
