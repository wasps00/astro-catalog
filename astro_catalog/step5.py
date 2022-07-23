nbins = 10
nbins2 = 5
resolution = 9999


def main(data, path):
    plot(data, "lgm_tot_p50", path, (-2000, 1000))


def plot(data, field, path, yrange=None):
    import matplotlib.pyplot as plt, numpy as np, os
    from scipy.interpolate import interp1d

    filepath = path + "/" + field + "-scatter.png"
    filepath2 = path + "/" + field + "-histogram.png"

    print(filepath)
    if yrange is not None:
        data = data[np.logical_and(data[field] > yrange[0], data[field] < yrange[1])]
    # Data
    x = data["z"][np.logical_and(np.isfinite(data["z"]), np.isfinite(data[field]))]
    y = data[field][np.logical_and(np.isfinite(data["z"]), np.isfinite(data[field]))]
    print("\tPlot " + field + "-redshift")
    plt.xlabel("redshift")
    plt.ylabel(field)
    plt.scatter(x, y, alpha=0.1, label="data")
    # Means
    bins = np.linspace(x.min(), x.max(), nbins)
    means_x = []
    means_y = []
    err_y = [[], []]
    for i in range(nbins - 1):
        means_x.append((bins[i] + bins[i + 1]) / 2)
        ys = y[np.logical_and(bins[i] <= x, x < bins[i + 1])]
        mean = ys.mean()
        means_y.append(mean)
        err_y[0].append(mean - np.percentile(ys, 16))
        err_y[1].append(np.percentile(ys, 84) - mean)
    interpolation = interp1d(means_x, means_y, "cubic")
    linspace = np.linspace(means_x[0], means_x[-1], resolution)
    plt.plot(
        linspace,
        interpolation(linspace),
        label="best fit - order 3",
        linestyle="--",
        color="green",
    )
    plt.errorbar(
        means_x,
        means_y,
        err_y,
        fmt="o",
        color="black",
        ecolor="red",
        linewidth=0.25,
        elinewidth=2,
        label="16th-84th percentile",
    )
    plt.legend()
    plt.title("Mean of property " + field + " for each redshift bin")
    os.makedirs(path, exist_ok=True)
    plt.savefig(filepath)
    plt.clf()
    # histograms
    bins = np.linspace(x.min(), x.max(), nbins2)
    for i in range(nbins2 - 1):
        plt.hist(
            y[np.logical_and(bins[i] <= x, x < bins[i + 1])],
            label="z in [{:.3f}, {:.3f}[".format(bins[i], bins[i + 1]),
            color="C" + str(i),
            orientation="horizontal",
            alpha=0.25,
        )
    plt.legend(loc="lower right")
    plt.xlabel("absolute frequency")
    plt.ylabel(field)
    plt.title("Absolute frequencies of property " + field + " for each redshift bin")
    plt.savefig(filepath2)
    plt.clf()
