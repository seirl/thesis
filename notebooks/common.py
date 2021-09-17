import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

try:
    from functools import cached_property
except ImportError:
    class cached_property(object):
        def __init__(self, func):
            self.__doc__ = getattr(func, "__doc__")
            self.func = func

        def __get__(self, obj, cls):
            if obj is None:
                return self

            value = obj.__dict__[self.func.__name__] = self.func(obj)
            return value


def pltsetup():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["New Century Schoolbook"],
        # "font.serif": ["TeX Gyre Schola"],
        "grid.linestyle": "dotted",
        "figure.autolayout": True,
    })


def load_text_distribution(path):
    d = [
        tuple(map(float, r.split()))
        for r in path.read_text().split('\n') if r
    ]
    x = [r[0] for r in d]
    y = [r[1] for r in d]
    return np.array(x), np.array(y)


LAYERS = {
    'full': 'Entire graph',
    'dir+cnt': 'Filesystem layer',
    'rev': 'Commit layer',
    'rel+rev': 'History layer',
    'ori+snp': 'Hosting layer',
}


types_verbose = {
    'cnt': 'contents',
    'dir': 'directories',
    'rev': 'revisions',
    'rel': 'releases',
    'snp': 'snapshots',
    'ori': 'origins',
    'all': 'everything',
}


def exposant_hat(xmin, x, y, shift):
    sy = y[x >= xmin]
    sx = x[x >= xmin]
    # print(len(sy),len(sx),xmin)
    e_hat = 1 + sy.sum() / (sy * np.log(sx / (xmin-shift))).sum()
    return e_hat


def pcdf(xmin, e, s):
    # Disabled for performance reasons
    # assert np.amin(s) < xmin, ("ERROR, min(s) < xmin."
    #                            f" min(s) = {np.amin(s)}, xmin = {xmin}")
    return 1 - (s / xmin) ** (1 - e)


class Distribution:
    def __init__(self, x, y, xlabel, ylabel, desc):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.desc = desc
        self.y_cum = np.cumsum(y[::-1])[::-1]
        self.y_norm = y / np.sum(y)
        self.y_cum_norm = self.y_cum / np.sum(y)

    @cached_property
    def x_min(self):
        x_min = []
        missing = 0
        xmold = -1
        # print(len(self.x),flush=True)
        # print(max(self.x),flush=True)
        for xm in np.logspace(0, np.log10(max(self.x) + 0.1), 1000, dtype=int):
            if xm >= 1 and xm != xmold:
                if xm in self.x:
                    x_min.append(xm)
                    xmold = xm
                else:
                    missing += 1
            if missing == 1:
                break
        # on repart du plus grand (à partir du moment où certaines valeurs sont
        # manquantes)
        # en excluant la dernière valeur -> division par zero (1/ln(1))
        # print(x_min)
        # print(self.x)
        if len(x_min) != 0:
            max_x_min = max(x_min)
        else:
            max_x_min = 0
        for xm in (self.x[:-1])[self.x[:-1] > max_x_min]:
            x_min.append(xm)
        return x_min

    @cached_property
    def e_x_min(self):
        return [exposant_hat(xm, self.x, self.y, 0.0) for xm in self.x_min]

    @cached_property
    def e_x_min_shift(self):
        return [exposant_hat(xm, self.x, self.y, 0.5) for xm in self.x_min]

    @cached_property
    def D_max(self):
        dm = []
        for i in range(len(self.x_min)):
            xm = self.x_min[i]
            pc = pcdf(self.x_min[i], self.e_x_min[i], self.x[self.x >= xm])
            s = self.y[self.x >= xm]
            sc = np.cumsum(s) / np.sum(s)
            D = np.abs(sc - pc)
            dm.append(D.max())
        return dm

    def plot(self):
        fig = plt.figure()
        # fig.suptitle(self.desc)
        ax = fig.add_subplot()
        ax.grid()
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.plot(
            self.x,
            self.y,
            '.',
            markersize=3,
            label="Frequency ($= x$)",
            rasterized=True,
        )
        ax.plot(
            self.x,
            self.y_cum,
            '.',
            markersize=3,
            label="Cumulative freq. ($\\geq x$)", rasterized=True,
        )

        minDmax = min(self.D_max)
        iminDmax = self.D_max.index(minDmax)
        pivot = self.x_min[iminDmax]
        # x_before_pivot = self.x[self.x <= pivot]
        # x_after_pivot = self.x[self.x >= pivot]
        y_after_pivot = self.y[self.x >= pivot]

        power = self.fitted_power()

        ax.plot(
            self.x[self.x > 0],
            (
                (pivot / self.x[self.x > 0])
                ** (power - 1)
                * np.sum(y_after_pivot)
            ),
            "-",
            label='Power law fit ($\\alpha = {:.2}$)'.format(power),
            rasterized=True,
        )

        """
        ax.plot(
            x_before_pivot[x_before_pivot > 0],
            (
                (pivot / x_before_pivot[x_before_pivot > 0])
                ** (power - 1)
                * np.sum(y_after_pivot)
            ),
            "-",
            # label='fit using RML / up',
            color="green",
            label='Power law fit (α = {:.4})'.format(power),
            rasterized=True,
        )
        ax.plot(
            x_after_pivot,
            (
                (pivot / x_after_pivot) ** (power - 1)
                * np.sum(y_after_pivot)
            ),
            "--",
            color="green",
            # label='fit using RML / down',
            rasterized=True,
        )
        """
        ax.set_ylim(bottom=0.4)
        ax.legend(markerscale=4)

    def plot_ehat(self):
        fig = plt.figure()
        # fig.suptitle(self.desc + " ($\\hat{e}$)")
        ax = fig.add_subplot()
        ax.set_xlim(1, max(self.x))
        ax.set_ylim(1, 4)
        ax.grid()
        ax.set_xlabel("$x_{min}$")
        ax.set_ylabel("$\\hat{e}$")

        ax.set_xscale('log')

        ax.plot(
            self.x_min, self.e_x_min, "o", markersize=2, label="$\\hat{e} x$"
        )
        ax.plot(
            self.x_min, self.e_x_min_shift, "o", markersize=2,
            label="$\\hat{e} shift$"
        )
        ax.legend(markerscale=4)

    def plot_dmax(self):
        fig = plt.figure()
        # fig.suptitle(self.desc + " ($D_{max}$)")
        ax = fig.add_subplot()
        ax.set_xlim(1, max(self.x_min))
        ax.grid()
        ax.set_xlabel("$x_{min}$")
        ax.set_ylabel("$D_{max}$")
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.plot(self.x_min, self.D_max, "o", markersize=2, label="$D_{max}$")
        ax.legend(markerscale=4)

    def fitted_power(self):
        minDmax = min(self.D_max)
        iminDmax = self.D_max.index(minDmax)
        return self.e_x_min[iminDmax]

    def plot_fit(self):
        fig = plt.figure()
        # fig.suptitle(self.desc + " (fitted power law)")
        ax = fig.add_subplot()
        ax.grid()
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.plot(self.x, self.y_cum_norm, '.', markersize=2,
                label="Cumulative frequency (≥ x)")

        minDmax = min(self.D_max)
        iminDmax = self.D_max.index(minDmax)
        pivot = self.x_min[iminDmax]
        x_before_pivot = self.x[self.x <= pivot]
        x_after_pivot = self.x[self.x >= pivot]
        y_after_pivot = self.y[self.x >= pivot]

        ax.plot(
            x_before_pivot[x_before_pivot > 0],
            (
                (pivot / x_before_pivot[x_before_pivot > 0])
                ** (self.e_x_min[iminDmax] - 1)
                * np.sum(y_after_pivot) / np.sum(self.y)
            ),
            "-",
            label='fit using RML / up',
        )
        ax.plot(
            x_after_pivot,
            (
                (pivot / x_after_pivot) ** (self.e_x_min[iminDmax] - 1)
                * np.sum(y_after_pivot) / np.sum(self.y)
            ),
            "-",
            label='fit using RML / down',
        )

        ax.legend(markerscale=4)


def plot_all(dist, savepath, basename):
    p = Path(savepath)
    p.mkdir(exist_ok=True)

    if len(dist.x) > 1:
        dist.plot()
        plt.savefig(p / '{}.pdf'.format(basename), dpi=200)
        return
        dist.plot_ehat()
        plt.savefig(p / '{}_ehat.png'.format(basename))
        dist.plot_dmax()
        plt.savefig(p / '{}_dmax.png'.format(basename))
        dist.plot_fit()
        plt.savefig(p / '{}_fit.png'.format(basename))
        print(dist.fitted_power())
    else:
        print("Singular histogram", basename)
