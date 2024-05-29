from contextlib import contextmanager
from typing import Optional, Union
import warnings

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.font_manager
from matplotlib.transforms import Bbox

from .util import collapse_dict, generate_baseline_color

# Default figure size and text size
FIG_SIZE = (7/4, 21/16)
TEXT_SIZE = 7
OURS_COLOR = "#d00"
BASELINE_COLORS = ["#b3cfff", "#b3ffcf", "#b3ffff"]

# Matplotlib configuration dictionary for consistent styling
RC_CONFIG = collapse_dict({
    "font": {"size": TEXT_SIZE, "family": "Times New Roman"},
    "axes": {"titlesize": TEXT_SIZE, "labelsize": TEXT_SIZE},
    "xtick": {"labelsize": TEXT_SIZE},
    "ytick": {"labelsize": TEXT_SIZE},
    "legend": {"fontsize": TEXT_SIZE},
    "figure": {"titlesize": TEXT_SIZE, "figsize": FIG_SIZE},
})

# Fall back to generic serif font if requested font is unavailable
fonts = set(f.name for f in matplotlib.font_manager.fontManager.ttflist)
if RC_CONFIG["font.family"] not in fonts:
    warnings.warn(f"Default font \"{RC_CONFIG['font.family']}\" not available, "
                  "falling back to generic serif font.")
    RC_CONFIG["font.family"] = "serif"


@contextmanager
def figure(*args, **kwargs):
    """
    Context manager for creating and styling a Matplotlib figure with predefined configurations.

    All arguments are forwarded to `plt.figure()`

    Yields:
        Figure: The Matplotlib figure object.
    """
    with plt.rc_context(RC_CONFIG):
        fig = plt.figure(*args, **kwargs)
        yield fig
        finalize_figure(fig)


def finalize_figure(fig: Figure, style_axes=True):
    """
    Finalizes the figure's layout and optionally styling all axes.

    Args:
        fig (Figure): The Matplotlib figure object.
        style_axes (bool): If True, apply styles to all axes in the figure.
    """
    if style_axes:
        for ax in fig.axes:
            finalize_axes(ax)
    fig.tight_layout(pad=0)


def finalize_axes(ax: Axes):
    """
    Applies styling to a single Axes object.

    Args:
        ax (Axes): The Matplotlib axes object to style.
    """
    ax.spines[['right', 'top']].set_visible(False)

    bbox = Bbox.union([line.get_bbox() for line in ax.get_lines()])
    ax.set_xticks([bbox.xmin, bbox.xmax])
    ax.set_yticks([bbox.ymin, bbox.ymax])

    ax.set_xlabel(ax.get_xlabel(), labelpad=-ax.xaxis.label.get_fontsize())
    ax.set_ylabel(ax.get_ylabel(), labelpad=-ax.yaxis.label.get_fontsize())


def plot_kwargs(baseline: Optional[Union[str, int]] = None, n_baselines: Optional[int] = None, **kwargs):
    """
    Generates keyword arguments for plotting.

    Args:
        baseline (Optional[Union[str, int]]): 
            - If None, plots data as "ours", which will be the most prominent color.
            - If an integer, plots data with a prespecified less prominent color. 
              Defaults to a hardcoded list of colors, specify `n_baselines` to generate unique colors for each baseline.
            - If a string, plots data with the color specified by the string.
        n_baselines (Optional[int]): The number of baselines being plotted, used to generate unique colors for each baseline.
            If unspecified, defaults to a hardcoded list of colors, which may be insufficient for many baselines.
        **kwargs: Additional keyword arguments for plotting, inserted verbatim into the returned dict.

    Returns:
        dict: A dictionary of plot keyword arguments.
    """
    if baseline is None:
        color = OURS_COLOR
    elif isinstance(baseline, int):
        if n_baselines is None or n_baselines <= len(BASELINE_COLORS):
            assert 0 <= baseline < len(BASELINE_COLORS), \
                "Baseline index exceeds the number of hardcoded colors! " \
                "Please specify a custom baseline color or the number of baselines."
            color = BASELINE_COLORS[baseline]
        else:
            color = generate_baseline_color(baseline, n_baselines)
    else:
        color = baseline
    new_kwargs = {
        "color": color,
        "clip_on": False,
        "zorder": 4 if baseline is None else 3,
        **kwargs
    }
    return new_kwargs


def line_plot_kwargs(baseline: Optional[Union[str, int]] = None, n_baselines: Optional[int] = None, **kwargs):
    """
    Generates keyword arguments for line plots.

    Args:
        baseline (Optional[Union[str, int]]): 
            - If None, plots data as "ours", which will be the most prominent color.
            - If an integer, plots data with a prespecified less prominent color. 
              Defaults to a hardcoded list of colors, specify `n_baselines` to generate unique colors for each baseline.
            - If a string, plots data with the color specified by the string.
        n_baselines (Optional[int]): The number of baselines being plotted, used to generate unique colors for each baseline.
            If unspecified, defaults to a hardcoded list of colors, which may be insufficient for many baselines.
        **kwargs: Additional keyword arguments for plotting, inserted verbatim into the returned dict.

    Returns:
        dict: A dictionary of line plot keyword arguments.
    """
    new_kwargs = plot_kwargs(baseline, n_baselines)
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
    """
    Saves a Matplotlib figure as a PNG file with specified properties.

    Args:
        fig (Figure): The Matplotlib figure object to save.
        path (str): The file path to save the figure.
        *args: Additional positional arguments for `fig.savefig`.
        **kwargs: Additional keyword arguments for `fig.savefig`.
    """
    kwargs_ = {"transparent": True, "pad_inches": 0,
               "bbox_inches": "tight", "dpi": 300, **kwargs}
    fig.savefig(path, *args, **kwargs_)


def savefig_pdf(fig: Figure, path: str, *args, **kwargs):
    """
    Saves a Matplotlib figure as a PDF file with specified properties.

    Args:
        fig (Figure): The Matplotlib figure object to save.
        path (str): The file path to save the figure.
        *args: Additional positional arguments for `fig.savefig`.
        **kwargs: Additional keyword arguments for `fig.savefig`.
    """
    kwargs_ = {"transparent": True, "format": "pdf", **kwargs}
    fig.savefig(path, *args, **kwargs_)
