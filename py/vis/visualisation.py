"""Base visualisation style

Examples:
    ```python
    from vis import uni_plot
    fig, ax = uni_plot(x, y1, label="y1")
    uni_plot(x, y2, ax=ax, label="y2", xlabel="xlabel", ylabel="ylabel")
    ```
"""

import os
from typing import IO, Sequence

import matplotlib as mpl
from cycler import cycler
from matplotlib import pyplot as plt
from matplotlib.typing import ColorType

from vis import ColourScheme


def uni_plot(
    y: Sequence[float],
    x: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    label: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    c: ColorType | None = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Line plot x vs y

    Args:
        y: y-axis data
        x: x-axis data
        ax: Axes to plot on. New figure on None
        label: Label for legend
        c: Colour of the line.

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

    ax.plot(x, y, label=label, c=c, **kwargs)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return fig, ax


def uni_scatter(
    y: Sequence[float],
    x: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    label: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    c: ColorType | None = None,
    s: int | float = 3,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Scatter plot x vs y

    Args:
        y: y-axis data
        x: x-axis data
        ax: Axes to plot on. New figure on None
        label: Label for legend
        xlabel: Label for x-axis
        ylabel: Label for y-axis
        c: Colour of the line.
        s: Size of the marker.

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

    ax.scatter(x, y, label=label, c=c, s=s, **kwargs)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return fig, ax


@classmethod
def dual_y_axis_plot(
    cls,
    y_s: tuple[Sequence[float], Sequence[float]],
    x: Sequence[float],
    *,
    ax: plt.Axes | None = None,
    xlabel: str | None = None,
    ylabels: tuple[str | None, str | None] = (None, None),
    colors: tuple[ColorType | None, ColorType] = (None, "r"),
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
    fig, ax = cls.univariate_plot(
        y_s[0], x, ax=ax, xlabel=xlabel, ylabel=ylabels[0], c=colors[0], **kwargs
    )
    ax_right = ax.twinx()
    cls.univariate_plot(
        y_s[1], x, ax=ax_right, ylabel=ylabels[1], c=colors[1], **kwargs
    )
    ax_right.spines["right"].set_color(colors[1])
    ax_right.yaxis.label.set_color(colors[1])
    ax_right.tick_params(axis="y", labelcolor=colors[1])
    ax_right.grid(False)

    return fig, ax


@classmethod
def dual_x_axis_plot(
    cls,
    y: Sequence[float],
    x_s: tuple[Sequence[float], Sequence[float]],
    *,
    ax: plt.Axes | None = None,
    xlabels: tuple[str | None, str | None] = (None, None),
    ylabel: str | None = None,
    colors: tuple[ColorType | None, ColorType] = (None, "r"),
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
    fig, ax = cls.univariate_plot(
        y, x_s[0], ax=ax, xlabel=xlabels[0], ylabel=ylabel, c=colors[0], **kwargs
    )
    ax_top = ax.twiny()
    cls.univariate_plot(y, x_s[1], ax=ax_top, xlabel=xlabels[1], c=colors[1], **kwargs)
    ax_top.spines["top"].set_color(colors[1])
    ax_top.xaxis.label.set_color(colors[1])
    ax_top.tick_params(axis="x", labelcolor=colors[1])
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


def get_fig_ax(ax: plt.Axes | None) -> tuple[plt.Figure, plt.Axes]:
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure  # axes must belong to 1 and only 1 figure

    return fig, ax


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


def _init_style():
    """Initialise URT Visualisation style. This is called on import"""
    mpl.rcParams["lines.linewidth"] = 2.5
    mpl.rcParams["lines.markersize"] = 1.5

    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["text.usetex"] = False

    mpl.rcParams["axes.linewidth"] = 1
    mpl.rcParams["axes.titlesize"] = 10
    mpl.rcParams["axes.labelsize"] = 10
    mpl.rcParams["axes.xmargin"] = 0
    mpl.rcParams["axes.grid"] = True

    mpl.rcParams["grid.linewidth"] = 0.6

    mpl.rcParams["legend.framealpha"] = 1
    mpl.rcParams["legend.facecolor"] = "FFFFFF"
    mpl.rcParams["legend.edgecolor"] = "000000"
    mpl.rcParams["legend.fancybox"] = False
    mpl.rcParams["legend.title_fontsize"] = 10
    mpl.rcParams["legend.fontsize"] = "small"

    mpl.rcParams["axes.prop_cycle"] = cycler(color=ColourScheme.Primary.value)
