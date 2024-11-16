"""Base visualisation style

Examples:
    ```python
    from vis import uni_plot
    fig, ax = uni_plot(x, y1, label="y1")
    uni_plot(x, y2, ax=ax, label="y2", xlabel="xlabel", ylabel="ylabel")
    ```
"""

import contextlib
import os
from typing import IO
from typing import Any
from typing import Generator
from typing import Sequence

import matplotlib as mpl
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.typing import ColorType

from vis.colour import ColourScheme

MPL_RC: dict[str, dict[str, Any]] = {
    "lines": {
        "linewidth": 2.5,
        "markersize": 3,
    },
    "font": {
        "family": "serif",
        "size": 10,
    },
    "axes": {
        "linewidth": 1,
        "titlesize": 10,
        "labelsize": 10,
        "xmargin": 0,
        "grid": True,
        "prop_cycle": cycler(color=ColourScheme.Primary.value),
    },
    "grid": {
        "linewidth": 0.6,
    },
    "legend": {
        "framealpha": 1,
        "facecolor": "FFFFFF",
        "edgecolor": "000000",
        "fancybox": False,
        "title_fontsize": 10,
        "fontsize": "small",
    },
}
"""MatplotlibRc, refer to [matplotlib.rc()][matplotlib.rc]"""


@contextlib.contextmanager
def ctx(config: dict[dict[str, Any]] | None = None) -> Generator[None, None, None]:
    """Context manager + decorator to temporarily set style parameters.

    Args:
        config: A dictionary where keys are Matplotlib rc parameter groups
                    and values are dictionaries of parameter settings.
                    If None, use [MPL_RC][vis.MPL_RC].
    Yields:
        (None): This function is a generator that yields control back to the caller.

    Examples:
        ```python
        with ctx({'lines': {'linewidth': 2}, 'axes': {'labelsize': 'large'}}):
            # Your plotting code here

        @ctx({'lines': {'linewidth': 2}, 'axes': {'labelsize': 'large'}})
        def plot():
            # Your plotting code here
        ```
    """

    for key, value in (config or MPL_RC).items():
        mpl.rc(key, **value)

    yield

    mpl.rcdefaults()


@ctx()
def uni_plot(
    x: Sequence[float],
    y: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    label: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Line plot x vs y

    Args:
        x: x-axis data
        y: y-axis data
        ax: Axes to plot on. New figure on None
        label: Legend label

    Returns:
        Figure and Axes that was passed in or created

    Other Args:
        **kwargs: Other keyword args for [Axes.plot()][matplotlib.axes.Axes.plot].
            Moreover,
            If `xlab_override_warn`, `ylab_override_warn` are falsy,
            the module will not warn when `xlabel` or `ylabel` is overridden.
    """
    fig, ax = get_fig_ax(ax)

    xlabel, ylabel = _no_override_axis_labels(ax, fig, xlabel, ylabel, kwargs)

    ax.plot(x, y, label=label, **kwargs)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return fig, ax


@ctx()
def uni_scatter(
    x: Sequence[float],
    y: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    label: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Scatter plot x vs y

    Args:
        x: x-axis data
        y: y-axis data
        ax: Axes to plot on. New figure on None
        label: Label for legend
        xlabel: Label for x-axis
        ylabel: Label for y-axis

    Returns:
        Figure and Axes that was passed in or created

    Other Args:
        **kwargs: Other keyword args for [Axes.plot()][matplotlib.axes.Axes.plot].
            Moreover,
            If `xlab_override_warn`, `ylab_override_warn` are falsy,
            the module will not warn when `xlabel` or `ylabel` is overridden.
    """
    fig, ax = get_fig_ax(ax)

    xlabel, ylabel = _no_override_axis_labels(ax, fig, xlabel, ylabel, kwargs)

    ax.scatter(x, y, label=label, **kwargs)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return fig, ax


@ctx()
def dual_y_axis_plot(
    y_s: tuple[Sequence[float], Sequence[float]],
    x: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    xlabel: str | None = None,
    ylabels: tuple[str | None, str | None] = (None, None),
    colors: tuple[ColorType | None, ColorType | None] = (None, None),
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot 2 ys against 1 x

    Args:
        y_s: y-axis data
        x: x-axis data
        ax: Axes to plot on. New figure on None
        xlabel: Label for x-axis
        ylabels: Labels for y-axis
        colors: Colour of the line.

    Returns:
        Figure and Axes that was passed in or created

    Other Args:
        **kwargs: Other keyword args for [Axes.plot()][matplotlib.axes.Axes.plot].
            Moreover,
            If `xlab_override_warn`, `ylab_override_warn` are falsy,
            the module will not warn when `xlabel` or `ylabel` is overridden.
    """
    fig, ax = uni_plot(
        x, y_s[0], ax=ax, xlabel=xlabel, ylabel=ylabels[0], c=colors[0], **kwargs
    )

    # The new axes wipe out all formatting.
    with ctx():
        ax_right = ax.twinx()

    # Hack to get the same color cycle (shared object).
    # If this fail, gotta dig into the source code to find the new mechanism
    try:
        ax_right._get_lines = ax._get_lines
    except AttributeError as e:
        raise AttributeError(
            "Color cycle hack failed. Check matplotlib version."
        ) from e

    uni_plot(x, y_s[1], ax=ax_right, ylabel=ylabels[1], c=colors[1], **kwargs)

    twin_color = ax_right.get_lines()[-1].get_color()

    ax_right.spines["right"].set_color(twin_color)
    ax_right.yaxis.label.set_color(twin_color)
    ax_right.tick_params(axis="y", labelcolor=twin_color)
    ax_right.grid(False)

    return fig, ax


def dual_x_axis_plot(
    y: Sequence[float],
    x_s: tuple[Sequence[float], Sequence[float]],
    *,
    ax: plt.Axes | None = None,
    xlabels: tuple[str | None, str | None] = (None, None),
    ylabel: str | None = None,
    colors: tuple[ColorType | None, ColorType | None] = (None, None),
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot 2 xs against 1 y

    Args:
        y: y-axis data
        x_s: x-axis data
        ax: Axes to plot on. New figure on None
        xlabels: Label for x-axis
        ylabel: Labels for y-axis
        colors: Colour of the line.

    Returns:
        Figure and Axes that was passed in or created

    Other Args:
        **kwargs: Other keyword args for [Axes.plot()][matplotlib.axes.Axes.plot].
            Moreover,
            If `xlab_override_warn`, `ylab_override_warn` are falsy,
            the module will not warn when `xlabel` or `ylabel` is overridden.
    """
    fig, ax = uni_plot(
        x_s[0], y, ax=ax, xlabel=xlabels[0], ylabel=ylabel, c=colors[0], **kwargs
    )

    # The new axes wipe out all formatting.
    with ctx():
        ax_top = ax.twiny()

    # Hack to get the same color cycle (shared object).
    # If this fail, gotta dig into the source code to find the new mechanism
    try:
        ax_top._get_lines = ax._get_lines
    except AttributeError as e:
        raise AttributeError(
            "Color cycle hack failed. Check matplotlib version."
        ) from e

    uni_plot(x_s[1], y, ax=ax_top, xlabel=xlabels[1], c=colors[1], **kwargs)

    twin_color = ax_top.get_lines()[-1].get_color()

    ax_top.spines["top"].set_color(twin_color)
    ax_top.xaxis.label.set_color(twin_color)
    ax_top.tick_params(axis="x", labelcolor=twin_color)
    ax_top.grid(False)

    return fig, ax


# TODO: Multivariate plot


def get_axes_siblings_twinx(ax: plt.Axes) -> list[plt.Axes]:
    """
    Args:
        ax: Axes to get siblings from

    Returns:
        Siblings (excluding itself) sharing the x axis
    """
    siblings = ax.get_shared_x_axes().get_siblings(ax)
    siblings.remove(ax)
    return siblings


def get_axes_siblings_twiny(ax: plt.Axes) -> list[plt.Axes]:
    """
    Args:
        ax: Axes to get siblings from

    Returns:
        Siblings (excluding itself) sharing the y axis
    """
    siblings = ax.get_shared_y_axes().get_siblings(ax)
    siblings.remove(ax)
    return siblings


def show():
    """Show figures"""
    plt.show()


def save(fig: plt.Figure, fname: str | os.PathLike | IO, **kwargs):
    """Wrapper for [Figure.savefig()][matplotlib.figure.Figure.savefig].
    Defaults: dpi=200, transparent=True

    Args:
        fig: Figure to save
        fname: File name

    Other Args:
        **kwargs: [Figure.savefig()][matplotlib.figure.Figure.savefig].
    """
    dpi = kwargs.pop("dpi", 200)
    transparent = kwargs.pop("transparent", True)
    fig.savefig(fname, bbox_inches="tight", dpi=dpi, transparent=transparent, **kwargs)


@ctx()
def get_fig_ax(ax: plt.Axes | None) -> tuple[plt.Figure, plt.Axes]:
    """Get figure and axes. Create new figure if axes is None"""
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure  # axes must belong to 1 and only 1 figure

    return fig, ax


@ctx()
def subplots(*args, **kwargs) -> tuple[plt.Figure, plt.Axes | list[plt.Axes]]:
    """Wrapper for [plt.subplots()][matplotlib.pyplot.subplots]

    Returns:
        Figure and (Axes or array of Axes)
    """
    return plt.subplots(*args, **kwargs)


def _no_override_axis_labels(
    ax: plt.Axes,
    fig: plt.Figure,
    xlabel: str | None,
    ylabel: str | None,
    kwargs,
) -> tuple[str | None, str | None]:
    """If xlabel or ylabel exist. Will NOT override it.
    User needs to explicit [Axes.set()][matplotlib.axes.Axes.set] it.

    Args:
        ax: Axes to check. Return `xlabel` and `ylabel` if None
        fig: Figure to print warning
        xlabel: Label for x-axis
        ylabel: Label for y-axis

    Other Args:
        **kwargs: Other keyword args for [Axes.plot()][matplotlib.axes.Axes.plot].
            Moreover,
            If `xlab_override_warn`, `ylab_override_warn` are falsy,
            the module will not warn when `xlabel` or `ylabel` is overridden.

    Returns:
        xlabel and ylabel
    """
    xlab_override_warn: bool = kwargs.pop("xlab_override_warn", True)
    ylab_override_warn: bool = kwargs.pop("ylab_override_warn", True)
    if ax is None:
        return xlabel, ylabel

    figure_id = fig.get_label() or fig.number

    if xlabel is None:
        xlabel = ax.get_xlabel()
    elif ax.get_xlabel() != "":
        curr_xlabel = ax.get_xlabel()
        if curr_xlabel != xlabel and xlab_override_warn:
            print(f"⚠️ [Fig {figure_id}] xlabel arg discarded")

    if ylabel is None:
        ylabel = ax.get_ylabel()
    elif ax.get_ylabel() != "":
        curr_ylabel = ax.get_ylabel()
        if curr_ylabel != ylabel and ylab_override_warn:
            print(f"⚠️ [Fig {figure_id}] ylabel arg discarded")

    return xlabel, ylabel


def style_init():
    """Initialise style. Permanent until [style_reset()][vis.style_reset]"""
    for key, value in MPL_RC.items():
        mpl.rc(key, **value)


def style_reset():
    """Reset style to default"""
    mpl.rcdefaults()
