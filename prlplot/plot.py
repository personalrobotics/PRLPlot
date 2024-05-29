from typing import Any, Dict, Optional, Union
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from contextlib import contextmanager

FIG_SIZE = (7/4, 21/16)
TEXT_SIZE = 7
RC_CONFIG = {
    "font": {"size": TEXT_SIZE, "family": "Times New Roman"},
    "axes": {"titlesize": TEXT_SIZE, "labelsize": TEXT_SIZE},
    "xtick": {"labelsize": TEXT_SIZE},
    "ytick": {"labelsize": TEXT_SIZE},
    "legend": {"fontsize": TEXT_SIZE},
    "figure": {"titlesize": TEXT_SIZE, "figsize": FIG_SIZE},
}

def _collapse_dict(d: Dict[str, Any], keys=None):
    if keys is None:
        keys = []
    new_d = {}
    for k, v in d.items():
        keys.append(k)
        if isinstance(v, dict):
            new_d.update(_collapse_dict(v, keys))
        else:
            new_d[".".join(keys)] = v
        keys.pop()
    return new_d

@contextmanager
def figure(*args, **kwargs):
    fig = create_figure(*args, **kwargs)
    try:
        yield fig
    finally:
        finalize_figure(fig)

def create_figure(*args, **kwargs):
    with plt.rc_context(_collapse_dict(RC_CONFIG)):
        fig = plt.figure(*args, **kwargs)
    return fig

def finalize_figure(fig: Figure, style_axes=True):
    fig.tight_layout(pad=0)
    if style_axes:
        for ax in fig.axes:
            style_axes(ax)

def style_axes(ax: Axes):
    ax.spines[['right', 'top']].set_visible(False)
    ax.set_xticks(ax.get_xlim())
    ax.set_yticks(ax.get_ylim())
    ax.set_xlabel(ax.get_xlabel(), labelpad=-ax.xaxis.label.get_fontsize())
    ax.set_ylabel(ax.get_ylabel(), labelpad=-ax.yaxis.label.get_fontsize())

def plot_kwargs(baseline: Optional[Union[str, int]]=None):
    if baseline is None:
        color = "#d00"
    elif isinstance(baseline, str):
        color = baseline
    else:
        color = ["#b3cfff"][baseline]
    kwargs = {
        "color": color,
        "clip_on": False,
        "zorder": 3
    }
    return kwargs

def line_plot_kwargs(baseline: Optional[Union[str, int]]=None):
    kwargs = plot_kwargs(baseline)
    kwargs.update({
        "markersize": 2,
        "markeredgecolor": kwargs["color"],
        "markerfacecolor": "#fff",
        "markeredgewidth": 2,
        "linewidth": 2,
    })
    return kwargs

def savefig_png(fig: Figure, path: str, *args, **kwargs):
    kwargs_ = {"transparent": True, "pad_inches": 0, "bbox_inches": "tight", "dpi": 300, **kwargs}
    fig.savefig(path, *args, **kwargs_)

def savefig_pdf(fig: Figure, path: str, *args, **kwargs):
    kwargs_ = {"transparent": True, "format": "pdf", **kwargs}
    fig.savefig(path, *args, **kwargs_)
