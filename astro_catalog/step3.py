resolution = 9999


def main(data, path):
    plot(data, "petroMag_u", path)
    plot(data, "h_alpha_flux", path, (-500, 3500))
    plot(data, "lgm_tot_p50", path, (-2000, 1000))
    plot(data, "sfr_tot_p50", path, (-2000, 1000))
    plot(data, "absMagU", path)


def plot(data, yfield, path, yrange=None, use_bins=True, xfield="z"):
    import matplotlib.pyplot as plt, numpy as np, os, scipy.stats as stats

    filepath = path + "/" + yfield + "-" + xfield + ".png"
    print(filepath)
    if yrange is not None:
        data = data[np.logical_and(data[yfield] > yrange[0], data[yfield] < yrange[1])]
    x = data[xfield][
        np.logical_and(np.isfinite(data[xfield]), np.isfinite(data[yfield]))
    ]
    y = data[yfield][
        np.logical_and(np.isfinite(data[xfield]), np.isfinite(data[yfield]))
    ]
    print("\tPlot " + yfield + "-" + xfield)
    plt.xlabel(xfield)
    plt.ylabel(yfield)
    pearson, p_value = stats.pearsonr(x, y)
    print("\tCompute Pearson coefficient", pearson)
    print("\tCompute p-value", p_value)
    plt.title(
        "{}-{}\nPearson coefficient: {:.2f}, p-value {:.2f}".format(
            yfield, xfield, float(pearson), float(p_value)
        )
    )
    plt.scatter(x, y, alpha=0.1)
    os.makedirs(path, exist_ok=True)
    plt.savefig(filepath)
    plt.cla()
    if use_bins and abs(pearson) > 0.5:
        path += "/step2bis/"
        bins = np.linspace(x.min(), x.max(), 6)
        for bin_index in range(len(bins) - 1):
            from .step2 import plot

            print("\tPlot", bins[bin_index], "to", bins[bin_index + 1])
            plot(
                data[
                    np.logical_and(
                        data[xfield] > bins[bin_index],
                        data[xfield] < bins[bin_index + 1],
                    )
                ],
                yfield,
                path,
                filename="{}-{}".format(yfield, bin_index),
                title="{},\n {} in [{},{}[".format(
                    yfield, xfield, bins[bin_index], bins[bin_index + 1]
                ),
            )
