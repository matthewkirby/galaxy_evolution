import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

def find_histogram_edges(hist, bins):
    xs, ys = [], []
    for i in range(len(hist)):
        xs.append(bins[i])
        xs.append(bins[i+1])
        ys.append(hist[i])
        ys.append(hist[i])
    return xs, ys


def main():
    plt.rc('text', usetex=True)

    primus_table = Table().read('../catalogs/personal_catalogs/useable_catalog.csv', format='csv')

    # Make subtable with the appropriate cuts
    subtable = primus_table[np.where(primus_table['zSpec'] > 0.0)]
    subtable = subtable[np.where(subtable['zLDP_good'] == 1)]
    subtable = subtable[np.where(subtable['zSpec_Q'] == 1)]
    subtable = subtable[np.where(subtable['zLDP'] < 0.85)]
    subtable = subtable[np.where(subtable['slit_distance'] < 0.5)]

    # Calculate delta-z for each object in subtable
    subtable['dz'] = subtable['zLDP'] - subtable['zSpec']

    # Make tables for each Q value
    Q4 = subtable[np.where(subtable['Q'] == 4)]
    Q3 = subtable[np.where(subtable['Q'] >= 3)]
    Q2 = subtable[np.where(subtable['Q'] >= 2)]

    for dz in [0.02, 0.03, 0.04]:
        print '-------------------\ndz = %f' % dz
        for i in range(3):
            N_tot = len(eval('Q' + str(4 - i))['dz'])
            N_good = len(eval('Q' + str(4 - i))[np.where(abs(eval('Q' + str(4 - i))['dz']) <= dz)])
            percent_good = 100. * (1.0 - float(N_good) / float(N_tot))
            print 'Q%i = %0.1f' % (4-i, percent_good)

    # Calculate the dispersions
    print '--------------------\nDispersions'
    for i in range(3):
        print 'Q%i > %f' % (4-i, np.sum(eval('Q' + str(4 - i))['dz']**2)/len(eval('Q' + str(4 - i))['dz']))




if __name__ == '__main__':
    main()
