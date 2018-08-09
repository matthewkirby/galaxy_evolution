import numpy as np
from astropy.table import Table


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


def main():
    ldpcat = Table().read('../../catalogs/personal_catalogs/slits_phot_zs_cutonslitdist.csv', format='csv')
    cllist = load_clusters()

    rauto_cut = 22.9
    zmemb = 0.02

    tot_nmemb = 0
    tot_nphot, tot_ntargets, tot_nldp, tot_nq4 = 0, 0, 0, 0
    frauto_cut = 10**((rauto_cut-23.9)/(-2.5))

    for cl in cllist:
        phot = Table().read('../../catalogs/ediscs_v7.0/{}_catalog_v7.0.fits'
                            .format(cl['tablename']))
        phot = phot[np.where(phot['fRauto'] >= frauto_cut)]
        n_phot = len(phot)

        cl_table = ldpcat[np.where(ldpcat['field'] == cl['tablename'])]
        cl_table = cl_table[np.where(cl_table['Rauto'] <= rauto_cut)]
        cl_table['dz'] = abs(cl_table['zLDP']-cl['z'])

        n_targets = len(cl_table)
        cl_table = cl_table[np.where(cl_table['slit_distance'] < 1.)]
        n_ldp = len(cl_table[np.where(cl_table['Q'] >= 2)])
        n_q4 = len(cl_table[np.where(cl_table['Q'] >= 4)])
        n_memb = len(cl_table[np.where((cl_table['Q'] >= 4) & (cl_table['dz'] < zmemb))])

        tot_nmemb += n_memb

        if cl['count']:
            tot_nphot += n_phot
            tot_ntargets += n_targets
            tot_nldp += n_ldp
            tot_nq4 += n_q4
            print('{} & {} & {} & {} & {} & {} \\\\'.format(cl['papername'], n_phot, n_targets, n_ldp,
                                                        n_q4, n_memb))
        if not cl['count']:
            print('{} & \\nodata & \\nodata & \\nodata & \\nodata & {} \\\\'.format(cl['papername'], n_memb))

    print('\hline')
    print('Total & {} & {} & {} & {} & {}'.format(tot_nphot, tot_ntargets, tot_nldp, tot_nq4, tot_nmemb))

if __name__ == '__main__':
    main()