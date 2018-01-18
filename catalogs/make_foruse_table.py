import numpy as np
from astropy.table import Table


def calc_mag(photo, filt):
    flux = 'f'+filt
    mag = [flux2mag(f) for f in photo[flux]]
    photo[filt] = mag
    photo[filt].mask = np.isnan(mag)

    return


def flux2mag(f):
    return -2.5*np.log10(f) + 23.9


def main():
    full_table = Table().read('personal_catalogs/photo_ldp_fors2.csv', format='csv')
    print full_table.info
    photo = full_table[np.where(full_table['zLDP'] > 0.0)]
    print photo.info
    return
    filterlist = ['B1', 'V1', 'R1', 'I1', 'z1',
                  'B2', 'V2', 'R2', 'I2', 'z2',
                  'B3', 'V3', 'R3', 'I3', 'z3',
                  'Bauto', 'Vauto', 'Rauto', 'Iauto', 'zauto']

    for filt in filterlist:
        calc_mag(photo, filt)

    final_table = photo['field', 'ids', 'ra', 'dec', 'x', 'y',
                              'B1', 'V1', 'R1', 'I1', 'z1',
                              'B2', 'V2', 'R2', 'I2', 'z2',
                              'B3', 'V3', 'R3', 'I3', 'z3',
                              'Bauto', 'Vauto', 'Rauto', 'Iauto', 'zauto',
                              'zLDP5_7', 'Q5_7', 'zphot', 'zphot_errUP', 'zphot_errLO', 'class_StarR',
                              'zLDP', 'zLDPerr', 'Q', 'zLDP_good', 'slit_distance', 'zSpec', 'zSpec_Q']

    final_table.write('personal_catalogs/useable_catalog.csv', format='csv')

    return


if __name__ == '__main__':
    main()