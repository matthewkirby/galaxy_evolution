from astropy.table import Table, vstack, MaskedColumn
from astropy.io import fits
from astropy.coordinates import SkyCoord
import numpy as np
import bisect as bs
from astropy import units as u
import matplotlib.pyplot as plt


# Takes in a list of masks and returns an astropy table containing all of the primus outputs
def load_primus_data(masklist):
    primus_table = Table()
    for mask in masklist:
        catalog ='primus_catalogs/catalog_edsc0'+str(mask)+'.fits'

        hdu = fits.getdata(catalog, ext=0, header=True)
        ralist = hdu[0][0]
        declist = hdu[0][1]
        zlist = hdu[0][2]
        zerr = hdu[0][3]
        zconf = hdu[0][4]
        zgood = hdu[0][5]
        ra_spec = hdu[0][6]
        dec_spec = hdu[0][7]

        ttable = Table([ralist, declist, zlist, zerr, zconf, zgood, ra_spec, dec_spec],
                       names=('ra', 'dec', 'zLDP', 'zLDPerr', 'Q', 'zLDP_good', 'ra_slit', 'dec_slit'))
        primus_table = vstack([primus_table, ttable])

    photpos = SkyCoord(ra=primus_table['ra']*u.degree, dec=primus_table['dec']*u.degree)
    slitpos = SkyCoord(ra=primus_table['ra_slit']*u.degree, dec=primus_table['dec_slit']*u.degree)
    primus_table['slit_distance'] = photpos.separation(slitpos).arcsecond

    primus_table.sort('ra')
    primus_table['uid'] = np.arange(0, len(primus_table['ra']), 1)
    print "Done importing PRIMUS data"
    return primus_table


def load_zspecs():
    names, zspecs, zspecQs = np.genfromtxt('zspecs/all.zspec.dat', dtype=str, usecols=[0,1,2], unpack=True)
    # Parse names into RA and DEC
    zras, zdecs = [], []
    for name in names:
        tra = name[6:13]
        tdec = name[13:]
        tempra = "%ih%im%i.%is" % (int(tra[0:2]), int(tra[2:4]), int(tra[4:6]), int(tra[6:]))
        tempdec = "%sd%sm%s.%ss" % (tdec[0:3], tdec[3:5], tdec[5:7], tdec[7:])
        c = SkyCoord(tempra, tempdec, frame='icrs')

        zras.append(c.ra.deg)
        zdecs.append(c.dec.deg)
    print "Done importing FORS2 data"
    return Table([zras, zdecs, zspecs.astype(float), zspecQs.astype(int)], names=('ra', 'dec', 'zSpec', 'zSpec_quality'))


def find_histogram_edges(hist, bins):
    xs, ys = [], []
    for i in range(len(hist)):
        xs.append(bins[i])
        xs.append(bins[i+1])
        ys.append(hist[i])
        ys.append(hist[i])
    return xs, ys


def match_multi(matches, row1, dz):
    dzlist = matches['zLDP'] - row1['zSpec']
    if min(dzlist) < dz:
        ids = matches[np.where(dzlist == min(dzlist))]['uid']
        if isinstance(ids, float):
            return ids
        else:
            return ids[0]
    else:
        return -1


def main():
    # Make list of masks for PRIMUS catalogs
    masklist = np.arange(245, 281, 1).tolist()
    masklist.remove(249)
    masklist.remove(258)
    masklist.remove(267)

    #masklist = [245]

    # Load PRIMUS catalogs and build into astropy table
    primus_table = load_primus_data(masklist)
    #primus_table['zSpec'] = MaskedColumn(-1.*np.ones(len(primus_table)), mask=True)
    #primus_table['zSpec_quality'] = MaskedColumn(-1.*np.ones(len(primus_table)), mask=True)
    primus_table['zSpec'] = -1.
    primus_table['zSpec'].mask = True
    primus_table['zSpec_quality'] = -1
    primus_table['zSpec_quality'].mask = True

    # Load zSpec catalog and build into astropy table
    zspec_table = load_zspecs()

    match1 = 0
    match2 = 0
    match2res = 0

    ang_eps = 0.000278
    dz = 0.02
    for row1 in zspec_table:
        matches = []
        lo = bs.bisect_left(primus_table['ra'], row1['ra']-ang_eps)
        hi = bs.bisect_right(primus_table['ra'], row1['ra']+ang_eps)

        for row2 in primus_table[lo:hi]:
            if abs(row1['ra']-row2['ra']) > ang_eps:
                continue
            if abs(row1['dec']-row2['dec']) > ang_eps:
                continue
            matches.append(row2['uid'])

        if len(matches) == 1:
            match1 += 1
            primus_table[matches[0]]['zSpec'] = row1['zSpec']
            primus_table[matches[0]]['zSpec_quality'] = row1['zSpec_quality']
        elif len(matches) > 1:
            match2 += 1
            idmatch = match_multi(primus_table[matches], row1, dz)
            if idmatch < 0:
                continue
            primus_table[idmatch]['zSpec'] = row1['zSpec']
            primus_table[idmatch]['zSpec_quality'] = row1['zSpec_quality']
            match2res += 1


    print match1, match2, match2res
    print primus_table[np.where(primus_table['uid'] == 590)][0]

    primus_table.write('personal_catalogs/primus_fors2.csv', format='csv')


if __name__ == "__main__":
    main()
