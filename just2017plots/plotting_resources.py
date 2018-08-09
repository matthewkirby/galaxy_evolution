import numpy as np
from astropy.table import Table, join


def flux2mag(f):
    return -2.5*np.log10(f) + 23.9


def calc_mag(photo, filt):
    flux = 'f'+filt
    mag = flux2mag(photo[flux])
    photo[filt] = mag
    photo[filt][np.isnan(mag)] = 101.

    return

# Gehrels 1986 Poissonian confidence intervals
def upper_limit(n, s=1.0):
    return n + s*np.sqrt(n+.75) + 0.25*(s*s + 3.)


def lower_limit(n, s=1.0):
    return n - s*np.sqrt(n - 0.25) + 0.25*(s*s - 1.)


def average_error(n, s=1.0):
    u = upper_limit(n, s)-n
    l = n-lower_limit(n, s)
    return 0.5*(u+l)


def load_clusters():
    with open('../catalogs/personal_catalogs/cluster_info.dat') as fin:
        data = fin.readlines()[1:]

    # Load the color-magnitude relation table
    cmrtable = Table().read('../catalogs/personal_catalogs/cluster_cmr.dat', format='csv')

    # Load the cluster data
    data = [row.split() for row in data]
    cllist = [{'tablename': row[1], 'papername': row[2],
               'ra': float(row[3]), 'dec': float(row[4]), 'z': float(row[5]),
               'r200': float(row[6]), 'sigma': float(row[7]), 'sigma_hi': float(row[8]),
               'sigma_lo': float(row[9]), 'm200': float(row[10]), 'count': int(row[11]),
               'rinfall': float(row[12]), 'D_A': float(row[13])}
              for row in data]
    cltable = Table(cllist)
    
    # Merge the two
    cltable = join(cllist, cmrtable, keys='papername')
    
    return cltable

def add_red_blue(objs, cl):
    red = objs[np.where(objs['UB_color'] > (cl['cmr']-.2))]
    blue = objs[np.where(objs['UB_color'] <= (cl['cmr']-.2))]
    return red, blue


def add_ub_color(table):
    rfmags = Table().read('../catalogs/eazy_colors/ediscs_zldp_zfors_EAzY_outputs.csv', format='csv')
    rfmags.rename_column('id', 'ids')

    fulltable = join(table, rfmags['ids','MAG_AB_rfB', 'MAG_AB_rfU'], keys='ids', join_type='left')
    fulltable['UB_color'] = fulltable['MAG_AB_rfU'] - fulltable['MAG_AB_rfB']
    return fulltable




