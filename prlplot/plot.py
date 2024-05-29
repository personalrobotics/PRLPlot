from contextlib import contextmanager
from typing import Optional, Union

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

from .util import collapse_dict


FIG_SIZE = (7/4, 21/16)
TEXT_SIZE = 7
RC_CONFIG = collapse_dict({
    "font": {"size": TEXT_SIZE, "family": "Times New Roman"},
    "axes": {"titlesize": TEXT_SIZE, "labelsize": TEXT_SIZE},
    "xtick": {"labelsize": TEXT_SIZE},
    "ytick": {"labelsize": TEXT_SIZE},
    "legend": {"fontsize": TEXT_SIZE},
    "figure": {"titlesize": TEXT_SIZE, "figsize": FIG_SIZE},
})


@contextmanager
def figure(*args, **kwargs):
    with plt.rc_context(RC_CONFIG):
        fig = plt.figure(*args, **kwargs)
        yield fig
        finalize_figure(fig)


def finalize_figure(fig: Figure, style_axes=True):
    if style_axes:
        for ax in fig.axes:
            finalize_axes(ax)
    fig.tight_layout(pad=0)


def finalize_axes(ax: Axes):
    ax.spines[['right', 'top']].set_visible(False)

    bbox = Bbox.union([line.get_bbox() for line in ax.get_lines()])
    ax.set_xticks([bbox.xmin, bbox.xmax])
    ax.set_yticks([bbox.ymin, bbox.ymax])

    ax.set_xlabel(ax.get_xlabel(), labelpad=-ax.xaxis.label.get_fontsize())
    ax.set_ylabel(ax.get_ylabel(), labelpad=-ax.yaxis.label.get_fontsize())


def plot_kwargs(baseline: Optional[Union[str, int]] = None, **kwargs):
    if baseline is None:
        color = "#d00"
    elif isinstance(baseline, str):
        color = baseline
    else:
        color = ["#b3cfff"][baseline]
    new_kwargs = {
        "color": color,
        "clip_on": False,
        "zorder": 4 if baseline is None else 3,
        **kwargs
    }
    return new_kwargs


def line_plot_kwargs(baseline: Optional[Union[str, int]] = None, **kwargs):
    new_kwargs = plot_kwargs(baseline)
    new_kwargs.update({
        "markersize": 2,
        "markeredgecolor": new_kwargs["color"],
        "markeredgewidth": 2,
        "linewidth": 2,
        "marker": "o"
    })
    new_kwargs.update(kwargs)
    return new_kwargs


def savefig_png(fig: Figure, path: str, *args, **kwargs):
    kwargs_ = {"transparent": True, "pad_inches": 0,
               "bbox_inches": "tight", "dpi": 300, **kwargs}
    fig.savefig(path, *args, **kwargs_)


def savefig_pdf(fig: Figure, path: str, *args, **kwargs):
    kwargs_ = {"transparent": True, "format": "pdf", **kwargs}
    fig.savefig(path, *args, **kwargs_)
