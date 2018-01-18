import numpy as np
from astropy.table import Table
import bisect as bs


def load_photometry(name):
    photcat = Table().read(name)

    photcat['zLDP'] = -1.
    photcat['zLDPerr'] = -1.
    photcat['Q'] = -1
    photcat['zLDP_good'] = -1
    photcat['slit_distance'] = -1.
    photcat['zSpec'] = -1.
    photcat['zSpec_Q'] = -1.

    photcat['zLDP'].mask = True
    photcat['zLDPerr'].mask = True
    photcat['Q'].mask = True
    photcat['zLDP_good'].mask = True
    photcat['slit_distance'].mask = True
    photcat['zSpec'].mask = True
    photcat['zSpec_Q'].mask = True

    photcat.sort('ra')
    photcat['uid'] = np.arange(0, len(photcat['ra']), 1)

    return photcat


def match_row(photcat, row, id):
    photcat[id]['zLDP'] = row['zLDP']
    photcat[id]['zLDPerr'] = row['zLDPerr']
    photcat[id]['Q'] = row['Q']
    photcat[id]['zLDP_good'] = row['zLDP_good']
    photcat[id]['slit_distance'] = row['slit_distance']
    photcat[id]['zSpec'] = row['zSpec']
    photcat[id]['zSpec_Q'] = row['zSpec_quality']
    return

def main():
    primus_table = Table().read('personal_catalogs/primus_fors2.csv', format='csv')
    photcat = load_photometry('personal_catalogs/megacat.fits')


    match1, match2, match2res = 0, 0, 0

    ang_eps = 0.000278
    for row1 in primus_table:
        matches = []
        lo = bs.bisect_left(photcat['ra'], row1['ra']-ang_eps)
        hi = bs.bisect_right(photcat['ra'], row1['ra']+ang_eps)

        for row2 in photcat[lo:hi]:
            if abs(row1['ra']-row2['ra']) > ang_eps:
                continue
            if abs(row1['dec']-row2['dec']) > ang_eps:
                continue
            matches.append(row2['uid'])

        if len(matches) == 1:
            match1 += 1
            match_row(photcat, row1, matches[0])
        elif len(matches) > 1:
            match2 += 1
            continue  ####### Still need to resolve this #######################################################
            idmatch = match_multi(primus_table[matches], row1, dz)
            if idmatch < 0:
                continue
            primus_table[idmatch]['zSpec'] = row1['zSpec']
            primus_table[idmatch]['zSpec_quality'] = row1['zSpec_quality']
            match2res += 1

    print match1, match2
    photcat.write('personal_catalogs/photo_ldp_fors2.csv', format='csv')


if __name__ == '__main__':
    main()