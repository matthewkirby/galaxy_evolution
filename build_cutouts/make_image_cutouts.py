import numpy as np
from astropy.nddata import Cutout2D
import matplotlib.pyplot as plt
from astropy.io import fits


def load_centers(fname):
    # Determine which detector we are using for pixel ranges
    if fname[0] == 'i': instrument = 'UVIS'
    elif fname[0] == 'j': instrument = 'ACS'

    number = fname[4:6]
    if fname[7] in ['1', '3']:
        opt_filter = 'F606W'
    elif fname[7] in ['2', '4']:
        opt_filter = 'F814W'

    outname = instrument + '_mask' + number + '_' + opt_filter + '.txt'
    x, y = np.loadtxt('cut_ldp_catalog/object_pixel_locations/'+outname, unpack=True)

    details = {'instrument': instrument, 'mask': number, 'filter': opt_filter}

    return zip(x, y), details


def main():
    Ncutout = 0
    # Load image
    fname = 'ic8h01030_drz.fits'
    image = fits.open('../images/'+fname)[1].data

    # Load coords
    coords, details = load_centers(fname)

    # Make cutout

    for coord in coords:
        # Build the header
        hdr = fits.Header()
        hdr['filename'] = fname
        hdr['instrmnt'] = details['instrument']
        hdr['mask'] = details['mask']
        hdr['filter'] = details['filter']

        cutout = Cutout2D(image, coord, (100,100))

        fits.PrimaryHDU(cutout.data, header=hdr).writeto('cutouts/cutout%i.fits' % Ncutout, overwrite=True)
        Ncutout += 1










if __name__ == '__main__':
    main()
