import numpy as np
from astropy.nddata import Cutout2D
from astropy.io import fits
from astropy.table import Table


def load_centers(fname):
    # Determine which detector we are using for pixel ranges
    if fname[0] == 'i':
        instrument = 'UVIS'
    elif fname[0] == 'j':
        instrument = 'ACS'

    number = fname[4:6]
    if fname[7] in ['1', '3']:
        opt_filter = 'F606W'
    elif fname[7] in ['2', '4']:
        opt_filter = 'F814W'

    outname = instrument + '_mask' + number + '_' + opt_filter + '.csv'
    data = Table().read('cut_ldp_catalog/object_pixel_locations/'+outname, format='csv')

    return data


def main():
    ncutout = 0

    # Load the list of images
    imagelist = np.loadtxt('../images/image_list.dat', dtype=str)

    # Load image
    for fname in imagelist:
        image = fits.open('../images/'+fname)[1].data

        # Load coords
        coordcat = load_centers(fname)

        # Make cutout
        for row in coordcat:
            print "Building cutout #%i" % ncutout
            # Build the header
            hdr = fits.Header()
            hdr['filename'] = fname
            hdr['ra'] = row['ra']
            hdr['dec'] = row['dec']
            hdr['field'] = row['field']
            hdr['Q'] = row['Q']
            hdr['Rauto'] = row['Rauto']

            cutout = Cutout2D(image, [row['xcoord'], row['ycoord']], (200,200))

            fits.PrimaryHDU(cutout.data, header=hdr).writeto('cutouts/cutout%i.fits' % ncutout, overwrite=True)
            ncutout += 1


if __name__ == '__main__':
    main()
