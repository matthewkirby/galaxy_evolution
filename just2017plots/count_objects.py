import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

def main():
    primus_table = Table().read('../catalogs/personal_catalogs/useable_catalog.csv', format='csv')
    Nobj2 = len(primus_table[np.where(primus_table['Q'] >= 2)])
    Nobj3 = len(primus_table[np.where(primus_table['Q'] >= 3)])
    Nobj4 = len(primus_table[np.where(primus_table['Q'] >= 4)])
    print "Nobj Q>=2,3,4:", Nobj2, Nobj3, Nobj4

    # Make cut on slit-photometry distance
    subtable = primus_table[np.where(primus_table['slit_distance'] < 0.5)]
    Nobj2 = len(subtable[np.where(subtable['Q'] >= 2)])
    Nobj3 = len(subtable[np.where(subtable['Q'] >= 3)])
    Nobj4 = len(subtable[np.where(subtable['Q'] >= 4)])
    print "Nobj Q>=2,3,4:", Nobj2, Nobj3, Nobj4

    # Make cut on zLDP > 0.85
    subtable = subtable[np.where(subtable['zLDP'] < 0.85)]
    Nobj2 = len(subtable[np.where(subtable['Q'] >= 2)])
    Nobj3 = len(subtable[np.where(subtable['Q'] >= 3)])
    Nobj4 = len(subtable[np.where(subtable['Q'] >= 4)])
    print "Nobj Q>=2,3,4:", Nobj2, Nobj3, Nobj4

    # Make cut on zLDP < 0
    subtable = subtable[np.where(subtable['zLDP'] > 0.)]
    Nobj2 = len(subtable[np.where(subtable['Q'] >= 2)])
    Nobj3 = len(subtable[np.where(subtable['Q'] >= 3)])
    Nobj4 = len(subtable[np.where(subtable['Q'] >= 4)])
    print "Nobj Q>=2,3,4:", Nobj2, Nobj3, Nobj4



if __name__ == '__main__':
    main()
