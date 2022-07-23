import numpy as np

resolution = 9999


def theoretical_relation_BPT(x):
    return 0.61 / (x - 0.005) + 1.3


def theoretical_relation_CM(x):
    return -0.495 + 0.25 * x


def theoretical_relation_SFRm(x):
    return -8.64 + 0.76 * x


def is_over_theoretical_relation(x, y, theoretical_relation, range=(np.NINF, np.PINF)):
    range = np.full(x.size, range[0]), np.full(x.size, range[1])
    return np.logical_or(
        np.logical_or(x < range[0], x > range[1]), y >= theoretical_relation(x)
    )


def main(data, path):
    # BPT
    data_BPT = data[
        np.logical_and(
            np.logical_and(np.isfinite(data["z"]), data["h_alpha_flux"] != 0),
            data["h_beta_flux"] != 0,
        )
    ]
    x = data_BPT["nii_6584_flux"] / data_BPT["h_alpha_flux"]
    y = data_BPT["oiii_5007_flux"] / data_BPT["h_beta_flux"]
    z = data_BPT["z"][np.logical_and(x > 0, y > 0)]
    xx = np.log10(x[np.logical_and(x > 0, y > 0)])
    yy = np.log10(y[np.logical_and(x > 0, y > 0)])
    plot(
        xx,
        yy,
        z,
        "BPT",
        "log([NII] / Hα)",
        "log([OIII] / Hβ)",
        theoretical_relation_BPT,
        (-9, -0.078),
        path,
    )
    # color-mass
    data_CM = data[np.logical_and(np.isfinite(data["z"]), data["lgm_tot_p50"] > -2000)]
    x = data_CM["lgm_tot_p50"]
    y = data_CM["absMagU"] - data_CM["absMagR"]
    z = data_CM["z"]
    plot(
        x,
        y,
        z,
        "color-mass",
        "log10(M / M_⊙)",
        "u - r (color)",
        theoretical_relation_CM,
        (x.min() - 1, x.max() + 1),
        path,
    )
    # SFR-mass
    data_SFRm = data[
        np.logical_and(
            np.logical_and(np.isfinite(data["z"]), data["lgm_tot_p50"] > -2000),
            data["sfr_tot_p50"] > -2000,
        )
    ]
    x = data_SFRm["lgm_tot_p50"]
    y = data_SFRm["sfr_tot_p50"]
    z = data_SFRm["z"]
    plot(
        x,
        y,
        z,
        "SFR-mass",
        "log10(M / M_⊙)",
        "SFR",
        theoretical_relation_SFRm,
        (x.min() - 1, x.max() + 1),
        path,
    )


def plot(x, y, z, name, xlabel, ylabel, theoretical_relation, domain, path):
    import matplotlib.pyplot as plt, os
    from . import step2

    filepath = path + "/" + name + ".png"

    print(filepath)

    plt.colorbar(
        plt.scatter(x, y, c=z, cmap="plasma", alpha=0.3, vmin=z.min(), vmax=z.max())
    )
    linspace = np.linspace(domain[0], domain[1], resolution)
    plt.plot(
        linspace,
        theoretical_relation(linspace),
        color="red",
        label="theoretical relation",
    )
    plt.title(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    os.makedirs(path, exist_ok=True)
    plt.savefig(filepath)
    plt.clf()
    filter = is_over_theoretical_relation(x, y, theoretical_relation, range=domain)
    inverse_filter = np.logical_not(filter)
    step2.plot(
        None,
        xlabel,
        path,
        filename=name + "-x-up",
        title=xlabel + " (above the " + name + " theoretical relation)",
        x=x[filter],
        residuals=False,
    )
    step2.plot(
        None,
        xlabel,
        path,
        filename=name + "-x-down",
        title=xlabel + " (below the " + name + " theoretical relation)",
        x=x[inverse_filter],
        residuals=False,
    )
    step2.plot(
        None,
        ylabel,
        path,
        filename=name + "-y-up",
        title=ylabel + " (above the " + name + " theoretical relation)",
        x=y[filter],
        residuals=False,
    )
    step2.plot(
        None,
        ylabel,
        path,
        filename=name + "-y-down",
        title=ylabel + " (below the " + name + " theoretical relation)",
        x=y[inverse_filter],
        residuals=False,
    )
