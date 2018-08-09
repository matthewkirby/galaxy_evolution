import numpy as np
from astropy.table import Table, vstack
from astropy.io import fits
from astropy import wcs


def load_clusters():
    with open('../../catalogs/personal_catalogs/cluster_info.dat') as fin:
        data = fin.readlines()[1:]

    data = [row.split() for row in data]
    cllist = [{'tablename': row[1], 'papername': row[2],
               'ra': float(row[3]), 'dec': float(row[4]), 'z': float(row[5]),
               'r200': float(row[6]), 'sigma': float(row[7]), 'm200': float(row[8]),
               'count': int(row[9])}
              for row in data]
    return cllist


def find_objects_in_image(catalog, fname):
    """
    Description
    Takes in the ldp catalog and converts to pixels using the wcs in the respective image
    Finally, save a file containing valid objects in each image (1 per image)
    
    Inputs
    catalog: LDP catalog (astropy table)
    fname: Filename of the image to find pixel numbers

    Outputs
    None
    """

    print "Resolving RA/DEC into pixels using WCS for %s" % fname

    # Determine which detector we are using for pixel ranges
    if fname[0] == 'i': ACS = False
    elif fname[0] == 'j': ACS = True

    # Open the fits file and parse wcs header info
    image = fits.open('../../images/'+fname)
    w = wcs.WCS(image[1].header)

    # Convert ra/dec to pixels
    pixels = w.wcs_world2pix(zip(catalog['ra'], catalog['dec']), 1)
    catalog['xcoord'] = pixels[:, 0]
    catalog['ycoord'] = pixels[:, 1]

    # Remove pixels not in the image
    catalog = trim_objects_not_in_image(catalog, ACS)

    number = fname[4]+fname[5]
    if fname[7] == '1' or fname[7] == '3': filters = 'F606W'
    elif fname[7] == '2' or fname[7] == '4': filters = 'F814W'

    if ACS: outname = 'ACS_mask'+number+'_'+filters+'.csv'
    elif not ACS: outname = 'UVIS_mask'+number+'_'+filters+'.csv'

    catalog.write('object_pixel_locations/'+outname, format='csv', overwrite=True)

    return


def trim_objects_not_in_image(catalog, ACS):
    """
    Description
    Takes in the pixels values from a wcs transformation and removes lines that are not in the image
    """

    xmax, ymax = 4136, 4394
    if ACS:
        xmax, ymax = 4222, 4244

    catalog = catalog[np.where(catalog['xcoord'] < xmax-100)]
    catalog = catalog[np.where(catalog['xcoord'] > 100)]
    catalog = catalog[np.where(catalog['ycoord'] < ymax-100)]
    catalog = catalog[np.where(catalog['ycoord'] > 100)]

    return catalog


def main():
    dzcut = 0.02
    rauto_cut = 22.9

    # Load the cluster info
    cllist = load_clusters()

    # Load object catalog
    catalog = Table().read('../../catalogs/personal_catalogs/slits_phot_zs_cutonslitdist.csv', format='csv')
    purecat = catalog[np.where((catalog['Rauto'] < rauto_cut) &
                               (catalog['slit_distance'] < 1.0) &
                               (catalog['Q'] >= 3))]

    membercat = Table()
    # For each cluster, find members
    for cl in cllist:
        clcat = purecat[np.where(purecat['field'] == cl['tablename'])]
        print("{} in field {}".format(len(clcat), cl['tablename']))
        clcat = clcat[np.where(abs(clcat['zLDP'] - cl['z']) < dzcut)]
        print("{} in z range".format(len(clcat)))
        membercat = vstack((membercat, clcat))

    # Load filelist of images
    file_list = np.loadtxt('../../images/image_list.dat', dtype=str)

    for fileN in file_list:
        find_objects_in_image(membercat, fileN)

    return


if __name__ == "__main__":
    main()
