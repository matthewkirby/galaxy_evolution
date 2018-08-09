# DJRemote/completeness/speccomplete/comp6.pro

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt

def find_histogram_edges(hist, bins):
    xs, ys = [], []
    for i in range(len(hist)):
        xs.append(bins[i])
        xs.append(bins[i+1])
        ys.append(hist[i])
        ys.append(hist[i])
    return xs, ys


def main():
    #plt.rc('text', usetex=True)

    # Open and prepare the table
    full_table = Table().read('../catalogs/personal_catalogs/useable_catalog.csv', format='csv')
    photo = full_table[np.where(full_table['slit_distance'] < 0.5)]
    photo = photo[np.where(photo['Rauto'] > 0)]
    photo = photo[np.where(photo['Vauto'] > 0)]
    photo = photo[np.where(photo['Iauto'] > 0)]
    photo['VI'] = photo['Vauto'] - photo['Iauto']

    # Separate by Q
    Q4 = photo[np.where(photo['Q'] == 4)]
    Q3 = photo[np.where(photo['Q'] == 3)]
    Q2 = photo[np.where(photo['Q'] == 2)]
    all = photo[np.where(photo['Q'] >= 2)]

    # Histogram Rauto
    hist_edges = np.arange(18., 24.1, 0.25)
    xR4, yR4 = find_histogram_edges(np.log10(np.histogram(Q4['Rauto'], hist_edges)[0]), hist_edges)
    xR3, yR3 = find_histogram_edges(np.log10(np.histogram(Q3['Rauto'], hist_edges)[0]), hist_edges)
    xR2, yR2 = find_histogram_edges(np.log10(np.histogram(Q2['Rauto'], hist_edges)[0]), hist_edges)
    xRa, yRa = find_histogram_edges(np.log10(np.histogram(all['Rauto'], hist_edges)[0]), hist_edges)

    # Histogram V-I
    hist_edges2 = np.arange(0., 2.51, 0.1)
    xV4, yV4 = find_histogram_edges(np.log10(np.histogram(Q4['VI'], hist_edges2)[0]), hist_edges2)
    xV3, yV3 = find_histogram_edges(np.log10(np.histogram(Q3['VI'], hist_edges2)[0]), hist_edges2)
    xV2, yV2 = find_histogram_edges(np.log10(np.histogram(Q2['VI'], hist_edges2)[0]), hist_edges2)
    xVa, yVa = find_histogram_edges(np.log10(np.histogram(all['VI'], hist_edges2)[0]), hist_edges2)

    ##############################################################
    # Build the plot
    f, ((a0, a1), (a2, a3)) = plt.subplots(2,2)
    plt.setp([a.get_xticklabels() for a in f.axes[0:-2]], visible=False)
    f.subplots_adjust(hspace=0, wspace=0)

    # Make histogram of Rauto
    a0.plot(xR4, yR4, '-k', lw=1, label=r'$Q=4$')
    a0.plot(xR3, yR3, '-b', lw=1, label=r'$Q=3$')
    a0.plot(xR2, yR2, '-r', lw=1, label=r'$Q=2$')
    a0.plot(xRa, yRa, '-k', lw=2, label=r'$Q\geq2$')
    a0.axvline(22.6, c='0.5', lw=0.8)
    a0.axvline(22.9, c='r', lw=0.8)
    a0.set_xlim([18, 24])
    a0.set_ylim(-0.15, 4)
    a0.set_ylabel(r'$log(N)$')
    a0.tick_params(direction='in', which='both')
    a0.set_xticks(np.arange(18, 24.1, 1))
    a0.minorticks_on()

    # Make histogram of V-I
    a1.plot(xV4, yV4, '-k', lw=1, label=r'$Q=4$')
    a1.plot(xV3, yV3, '-b', lw=1, label=r'$Q=3$')
    a1.plot(xV2, yV2, '-r', lw=1, label=r'$Q=2$')
    a1.plot(xVa, yVa, '-k', lw=2, label=r'$Q\geq2$')
    a1.set_xlim([0, 2.5])
    a1.set_ylim(-0.15, 4)
    #a1.yaxis.set_label_position('right')
    a1.yaxis.tick_right()
    a1.tick_params(direction='in', which='both')
    a1.minorticks_on()
    a1.legend()

    a2.axvline(22.6, c='0.5', lw=0.8)
    a2.set_xlim([18, 24])
    a2.set_ylim([0.0, 1.05])
    a2.set_xticks(np.arange(18, 24.1, 1))
    a2.set_xlabel(r'$R_{auto}$')
    a2.set_ylabel('Fraction of Targets')
    a2.tick_params(direction='in', which='both')
    a2.minorticks_on()

    a3.yaxis.set_label_position('right')
    a3.yaxis.tick_right()
    a3.set_xlabel(r'$(V-I)$')
    a3.tick_params(direction='in', which='both')
    a3.minorticks_on()




    plt.show()
    #plt.savefig('mag_hist.png', dpi=300)


if __name__ == '__main__':
    main()