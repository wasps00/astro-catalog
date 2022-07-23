from . import step3


def main(data, path):
    fields = [
        "petroMag_i",
        "absMagI",
        "h_alpha_flux",
        "oiii_5007_flux",
        "nii_6584_flux",
        "lgm_tot_p50",
        "sfr_tot_p50",
    ]
    yranges = [
        None,
        None,
        (-500, 3500),
        (-100, 500),
        (-0.1, 0.1),
        (-2000, 1000),
        (-2000, 1000),
    ]
    l_fields = len(fields)
    for i in range(l_fields):
        for j in range(i + 1, l_fields):
            step3.plot(data, fields[j], path, yranges[j], False, fields[i])
