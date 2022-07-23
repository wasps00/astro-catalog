resolution = 9999


def main(data, path):
    plot(data, "z", path, (-0.007, 0.11), std_mod=False)
    plot(data, "petroMag_u", path, (13, 30))
    plot(data, "petroMag_r", path)
    plot(data, "petroMag_i", path)
    plot(data, "petroMag_z", path)
    plot(data, "h_alpha_flux", path, (-500, 500), 100)
    plot(data, "h_beta_flux", path, (-0.02, 0.02), 100)
    plot(data, "oiii_5007_flux", path, (-100, 500), 100)
    plot(data, "nii_6584_flux", path, (-0.1, 0.1), 100)
    plot(data, "lgm_tot_p50", path, (0, 20), 100)
    plot(data, "sfr_tot_p50", path, (-5, 5), 100)
    plot(data, "absMagU", path)
    plot(data, "absMagG", path)
    plot(data, "absMagR", path)
    plot(data, "absMagI", path)
    plot(data, "absMagZ", path)


def middles(bins):
    res = []
    bin_index = 0
    while bin_index < len(bins) - 1:
        res.append((bins[bin_index] + bins[bin_index + 1]) / 2)
        bin_index += 1
    return res


def plot(
    data,
    field,
    path,
    range=None,
    bin="auto",
    std_mod=True,
    filename=None,
    title=None,
    x=None,
    residuals=True,
):
    import math, matplotlib.pyplot as plt, numpy as np, os, scipy.stats as stats, warnings
    from scipy.stats import sem as scipy_sem, median_abs_deviation as scipy_mad

    if filename is None:
        filename = field
    if title is None:
        title = field
    if x is None:
        x = data[field][np.isfinite(data[field])]
    if range is not None:
        x = x[np.logical_and(x > range[0], x < range[1])]
    filepath = path + "/" + filename + ".png"
    filepath2 = path + "/" + filename + "-residuals.png"
    print(filepath)
    print("\tPlot histogram")
    count, bins, _ = plt.hist(x, bin, range, density=True, color="green", label=field)
    plt.xlabel(field)
    plt.ylabel("relative frequency")
    plt.title(title)
    mean = x.mean() if std_mod else sum(x) / x.size
    print("\tCompute mean", mean)
    warnings.filterwarnings("ignore")
    sem = (
        scipy_sem(x)
        if std_mod
        else math.sqrt(sum((x - np.full(x.size, mean)) ** 2)) / x.size
    )
    warnings.resetwarnings()
    print("\tCompute sem", sem)
    print("\tPlot mean ± sem")
    plt.axvline(mean, color="red", label="mean ± sem")
    plt.axvspan(mean - sem, mean + sem, alpha=0.25, color="red")
    median = np.median(x)
    print("\tCompute median", median)
    mad = scipy_mad(x)
    print("\tCompute mad", mad)
    print("\tPlot median ± mad")
    plt.axvline(median, color="blue", label="median ± mad")
    plt.axvspan(median - mad, median + mad, alpha=0.25, color="blue")
    plt.legend()
    os.makedirs(path, exist_ok=True)
    plt.savefig(filepath)
    std = x.std()
    plt.cla()
    if residuals:
        print("\tCompute std", std)
        if range is None:
            range = bins[0], bins[-1]
        linspace = np.linspace(range[0], range[1], resolution)
        warnings.filterwarnings("ignore")
        plt.plot(
            linspace,
            stats.norm.pdf(linspace, loc=mean, scale=std),
            color="brown",
            label="estimated values",
        )
        warnings.resetwarnings()
        plt.title(title + " (residuals)")
        plt.legend()
        plt.xlabel(field)
        plt.ylabel("relative frequency")
        plt.scatter(middles(bins), count, s=20, c="orange", label="observed values")
        plt.savefig(filepath2)
    plt.cla()
