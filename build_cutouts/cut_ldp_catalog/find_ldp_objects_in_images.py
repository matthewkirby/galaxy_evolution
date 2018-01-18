import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy import wcs


def find_objects_in_image(catalog, fname):

    '''
    Description
    Takes in the ldp catalog and converts to pixels using the wcs in the respective image
    Finally, save a file containing valid objects in each image (1 per image)
    
    Inputs
    catalog: LDP catalog (astropy table)
    fname: Filename of the image to find pixel numbers

    Outputs
    None
    '''

    print "Resoling RA/DEC into pixels using WCS for %s" % fname

    # Determine which detector we are using for pixel ranges
    if fname[0] == 'i': ACS = False
    elif fname[0] == 'j': ACS = True

    # Open the fits file and parse wcs header info
    image = fits.open('../../images/'+fname)
    w = wcs.WCS(image[1].header)

    # Convert ra/dec to pixels
    locs = zip(catalog['ra'], catalog['dec'])
    pixels = w.wcs_world2pix(locs, 1)

    # Remove pixels not in the image
    new_pixels = trim_objects_not_in_image(pixels, ACS)

    number = fname[4]+fname[5]
    if fname[7] == '1' or fname[7] == '3': 
        filters = 'F606W'
    elif fname[7] == '2' or fname[7] == '4': 
        filters = 'F814W'

    if ACS: outname = 'ACS_mask'+number+'_'+filters+'.txt'
    elif not ACS: outname = 'UVIS_mask'+number+'_'+filters+'.txt'

    np.savetxt('object_pixel_locations/'+outname, new_pixels, header='Image: %s' % fname, fmt='%.2f')

    return


def trim_objects_not_in_image(pixels, ACS):
    
    '''
    Description
    Takes in the pixels values from a wcs transformation and removes lines that are not in the image
    '''

    xmin, ymin = 0, 0
    if ACS:
        xmax, ymax = 4222, 4244
    if not ACS:
        xmax, ymax = 4136, 4394

    ys = pixels[:,1]

    xs = pixels[:,0]
    pixels = pixels[np.where(xs > xmin + 100)]
    xs = pixels[:,0]
    pixels = pixels[np.where(xs < xmax - 100)]

    ys = pixels[:,1]
    pixels = pixels[np.where(ys > ymin + 100)]
    ys = pixels[:,1]
    pixels = pixels[np.where(ys < ymax - 100)]

    return pixels



def main():
    # Load object catalog
    catalog = Table().read('../../catalogs/personal_catalogs/useable_catalog.csv', format='csv')
    catalog = catalog[np.where(catalog['Rauto'] < 22.9)]
    purecat = catalog[np.where(catalog['Q'] >= 3)]

    # Load filelist of images
    file_list = np.loadtxt('../../images/image_list.dat', dtype=str)

    for fileN in file_list:
        find_objects_in_image(catalog, fileN)

    return







if __name__ == "__main__":
    main()

