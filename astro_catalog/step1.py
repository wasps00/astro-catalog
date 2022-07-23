def read_catalog(filename):
    from astropy.io import fits

    hdulist = fits.open(filename)
    data = hdulist[1].data
    hdulist.close()
    return data


def filter_catalog(catalog, id):
    return catalog[catalog["ID"] == id]
