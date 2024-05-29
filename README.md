# PRLPlot

PRLPlot is a collection of simple opinionated plotting tools for generating high-quality plots for scientific papers.
The aim of this library is to make it as easy as possible to create beautiful plots in a specific style.

PRLPlot currently supports a limited number of types of plots, and welcomes feature additions and enhancements!

A demo of PRLPlot and a comparison against standard matplotlib plots is available in a Colab notebook [here](https://colab.research.google.com/drive/101v6qjB_aggAIF01Lk3RG_BqQn1-ygGf?usp=sharing).

## Installation

Install with:

```bash
pip install git+https://github.com/personalrobotics/PRLPlot.git
```

## Example

Plotting with PRLPlot is very easy, and very similar to regular pyplot. The plots are also very customizable, as PRLPlot is unintrusive to your plotting pipeline. A runnable notebook is available [here](https://colab.research.google.com/drive/101v6qjB_aggAIF01Lk3RG_BqQn1-ygGf?usp=sharing).

```python
from matplotlib import pyplot as plt
import numpy as np

import prlplot


X = np.linspace(0, 1, 5)
ours = X**0.3
theirs = X**0.7

# Plotting with PRLPlot is easy!
with prlplot.figure() as fig:
    ax = fig.add_subplot()
    ax.set_title("Ours vs Theirs")
    ax.plot(X, ours, label="Ours", **prlplot.line_plot_kwargs(baseline=None))
    ax.plot(X, theirs, label="Theirs", **prlplot.line_plot_kwargs(baseline=0))
    ax.legend()
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")

# Save losslessly as a PDF (OUTSIDE of the with block!)
prlplot.savefig_pdf(fig, "plot.pdf")
plt.show()
```
