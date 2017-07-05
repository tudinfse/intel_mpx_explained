import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use(["ggplot"])

# color pallets
PAIRED = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#e31a1c', '#fb9a99']
PRINTER_FRIENDLY = ['#b2df8a', '#fdae61', '#ffffbf', '#f4a582', '#1f78b4']
QUALITATIVE_3 = ['#8dd3c7', '#ffffb3', '#bebada']
QUALITATIVE_4 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072']
QUALITATIVE_5 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3']
QUALITATIVE_6 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462']
QUALITATIVE_7 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69']
STACKED_7 = ['#005a32', '#238443', '#41ab5d', '#78c679', '#addd8e', '#d9f0a3', '#ffffcc']


HATCH_TYPES = ['\\', '', '/', 'x', '+', '-', '*']
LINE_STYLES = ['-', '--', ':', '-', '--', ':', '-', '--', ':']
MARK_STYLES = ['o', 'v', 'p', 's', '^', '3', '4', 'D', 'H']


# style classes
class BasicStyle:
    """
    Defines style features that are common among all our plots
    """
    hatches = ("//////", r"\\\\\\", "", "", "")

    def __init__(self, need_hatching=True):
        self.need_hatching = need_hatching

    # main method
    def apply(self, ax: mpl.axes.Axes):
        self.font()
        self.axes(ax)
        self.edges(ax)
        self.grid(ax)
        self.ticks(ax)
        self.hatching(ax)
        self.legend(ax)
        self.title(ax)

        return ax

    # hooks
    def font(self):
        # font
        mpl.rcParams['pdf.fonttype'] = 42
        mpl.rcParams['ps.useafm'] = True
        mpl.rcParams['pdf.use14corefonts'] = True

    def axes(self, ax):
        # axes
        ax.set_facecolor("white")  # background
        ax.yaxis.label.set_color('black')
        ax.xaxis.label.set_color('black')

    def edges(self, ax):
        # edges
        for pos in ['top', 'bottom', 'right', 'left']:
            ax.spines[pos].set_edgecolor("black")

    def grid(self, ax):
        # grid
        ax.grid(
            color='#E0EEEE',  # azure2 from R
            linewidth="0.6",
            linestyle="-",  # solid line
        )
        ax.xaxis.grid(False)  # disable vertical lines

    def ticks(self, ax):
        # ticks
        ax.tick_params(
            labelcolor='black',
            which='major',
            direction='out',
            length=3,
            labelsize=9,
            right=False, top=False, bottom=False
        )
        ax.tick_params(
            labelcolor='black',
            which='minor',
            direction='out',
            length=0,
            labelsize=9,
            right=False, top=False, bottom=False
        )
        ax.tick_params(
            axis='x',
            pad=-1,
        )

    def hatching(self, ax):
        # hatching
        if self.need_hatching:
            bars = ax.patches
#            num_groups = int(len(bars) / len(self.hatches))
            num_groups = len(ax.get_xticks())
            hatches = [h for h in self.hatches for n in range(num_groups)]

            for bar, hatch in zip(bars, hatches):
                if hatch:
                    bar.set_hatch(hatch)
                    # bar.set_ec("black")

    def legend(self, ax):
        pass

    def title(self, ax):
        ax.set_title(
            ax.get_title(),
            {
                'fontsize': 10,
                'fontweight': 'bold',
                'horizontalalignment': "center",
            },
        )

    # helpers
    def globally_modify_legend(self, **kwargs):
        import matplotlib as mpl

        l = mpl.pyplot.gca().legend_

        defaults = dict(
            loc=l._loc,
            numpoints=l.numpoints,
            markerscale=l.markerscale,
            scatterpoints=l.scatterpoints,
            scatteryoffsets=l._scatteryoffsets,
            prop=l.prop,
            # fontsize = None,
            borderpad=l.borderpad,
            labelspacing=l.labelspacing,
            handlelength=l.handlelength,
            handleheight=l.handleheight,
            handletextpad=l.handletextpad,
            borderaxespad=l.borderaxespad,
            columnspacing=l.columnspacing,
            ncol=l._ncol,
            mode=l._mode,
            fancybox=type(l.legendPatch.get_boxstyle()) == mpl.patches.BoxStyle.Round,
            shadow=l.shadow,
            title=l.get_title().get_text() if l._legend_title_box.get_visible() else None,
            framealpha=l.get_frame().get_alpha(),
            bbox_to_anchor=l.get_bbox_to_anchor()._bbox,
            bbox_transform=l.get_bbox_to_anchor()._transform,
            frameon=l._drawFrame,
            handler_map=l._custom_handler_map,
        )

        if "fontsize" in kwargs and "prop" not in kwargs:
            defaults["prop"].set_size(kwargs["fontsize"])

        d = defaults.copy()
        d.update(kwargs.items())
        mpl.pyplot.legend(**dict(d))


class BarplotStyle(BasicStyle):
    bar_edge_color = "black"
    colors = ['#a6cee3', '#1f78b4', '#33a02c', '#b2df8a',  '#E8F7DA', '#e31a1c', '#fdbf6f']
    hatches = ("//////", "", "", r"\\\\\\", "//////",)

    def __init__(self, legend_ncol=5, legend_loc=None, **kwargs):
        super(BarplotStyle, self).__init__(**kwargs)
        self.legend_ncol = legend_ncol

        # I din't set it as default attribute value to support situation when caller also had a default value
        self.legend_loc = legend_loc if legend_loc else (0.005, 0.874)

    def ticks(self, ax):
        super(BarplotStyle, self).ticks(ax)
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=0)

    def legend(self, ax):
        l = ax.legend(
            title=None,
            loc=self.legend_loc,
            frameon=True,
            ncol=self.legend_ncol,
            labelspacing=0,
            columnspacing=1,
            borderpad=0.2,
            handlelength=0.7,
            fontsize=10,
            edgecolor='white',
            fancybox=False,
            framealpha=1,
        )
        l.get_frame().set_facecolor('#ffffff')


class BarplotMultithreadedStyle(BarplotStyle):
    colors = ['#ffffff', '#a6cee3', '#1f78b4', '#33a02c', '#b2df8a', '#E8F7DA', '#e31a1c', '#fdbf6f',]
    hatches = ("", "//////", "", "", r"\\\\\\", "//////",)


class BarplotWithNativeStyle(BarplotStyle):
    colors = ['#ffffff', '#a6cee3', '#1f78b4', '#33a02c', '#b2df8a', '#E8F7DA', '#e31a1c', '#fdbf6f',]
    hatches = ("", "//////", "", "", r"\\\\\\", "//////",)


class BarplotMPXFatureStyle(BarplotStyle):
    colors = ['#1f78b4', '#1f78b4', '#1f78b4', '#33a02c', '#33a02c', '#33a02c']
    hatches = ("", "//////", r"\\\\\\", "", "//////", r"\\\\\\",)


class BarplotClusteredStyle(BarplotStyle):
    colors = ['#33a02c', '#b2df8a', '#FF9C1F', '#FFC51F', '#1f78b4', '#a6cee3']
    bar_edge_color = "black"
    hatches = ("", "", "", "//", "//", "\\\\", "")


class VarInputBarStyle(BasicStyle):
    bar_edge_color = "black"
    colors = ['#a6cee3', '#1f78b4', '#33a02c', '#b2df8a',  '#E8F7DA', '#e31a1c', '#fdbf6f']
    hatches = ("//////", "", "", r"\\\\\\", "//////",)

    def ticks(self, ax):
        super(VarInputBarStyle, self).ticks(ax)
        ax.tick_params(
            labelcolor='black',
            which='major',
            direction='out',
            length=0,
            labelsize=9,
            right=False, top=False, bottom=False
        )
        ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=20)

    def title(self, ax):
        # title
        ax.set_title(
            ax.get_title(),
            {
                'fontsize': 10,
                'fontweight': 'bold',
                'verticalalignment': 'top',
                'horizontalalignment': "center",
                'position': (0.5, 0.95),
                'backgroundcolor': 'white',
            },
        )


class LinePlotStyle(BasicStyle):
    colors = ['#969696', '#a6cee3', '#1f78b4', '#33a02c', '#b2df8a',  '#E8F7DA', '#e31a1c', '#fdbf6f']

    def legend(self, ax, lines=(), labels=(), legend_loc="best"):
        ax.legend(
            lines,
            labels,
            title=None,
            loc=legend_loc,
            frameon=False,
            ncol=1,
            labelspacing=0.5,
            columnspacing=1,
            borderpad=1,
            handlelength=2,
            fontsize=12,
        )
        return ax
