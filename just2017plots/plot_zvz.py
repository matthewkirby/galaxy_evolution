import matplotlib.pyplot as plt
import numpy as np
import astropy.table as table
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

    primus_table = Table().read('../catalogs/personal_catalogs/primus_fors2.fits')

    # Make subtable with the appropriate cuts
    subtable = primus_table[np.where(primus_table['zSpec'] > 0.0)]
    subtable = subtable[np.where(subtable['zLDP_good'] == 1)]
    subtable = subtable[np.where(subtable['zSpec_quality'] == 1)]
    subtable = subtable[np.where(subtable['zLDP'] < 0.85)]

    # Calculate delta-z for each object in subtable
    subtable['dz'] = subtable['zLDP'] - subtable['zSpec']

    # Make tables for each Q value
    Q4 = subtable[np.where(subtable['Q'] == 4)]
    Q3 = subtable[np.where(subtable['Q'] >= 3)]
    Q2 = subtable[np.where(subtable['Q'] >= 2)]

    # Build the zvz plots
    f, ((a0, a1), (a2, a3), (a4, a5)) = plt.subplots(3,2)
    plt.setp([a.get_xticklabels() for a in f.axes[0:-2]], visible=False)
    f.subplots_adjust(hspace=0, wspace=0.1)
    for i in range(3):
        eval('a'+str(2*i)).plot(eval('Q'+str(4-i))['zSpec'], eval('Q'+str(4-i))['zLDP'], '.k', ms=4)
        eval('a' + str(2 * i)).plot(np.arange(0.,1.1, 0.1), np.arange(0.,1.1, 0.1), '0.7', lw=0.8)

        eval('a' + str(2 * i)).set_xlim([0, 1.1])
        eval('a' + str(2 * i)).set_ylim([0, 0.95])

        if i == 0:
            eval('a' + str(2 * i)).text(0.1, 0.8, r'$Q=%i$' % (4-i))
        elif i > 0:
            eval('a' + str(2 * i)).text(0.1, 0.8, r'$Q\geq%i$' % (4-i))


    # Build the residual plots
    bins = np.arange(-0.6, 0.61, 0.01)
    for i in range(3):
        hist, b = np.histogram(eval('Q'+str(4-i))['dz'], bins=bins)
        loghist = np.log10(hist)
        loghist[np.isinf(loghist)] = -1

        # Find the percentage of outliers
        N_tot = len(eval('Q'+str(4-i))['dz'])
        N_good = len(eval('Q'+str(4-i))[np.where(abs(eval('Q'+str(4-i))['dz']) <= 0.02)])
        percent_good = 100.*(1.0 - float(N_good)/float(N_tot))

        print N_tot, N_good

        xs, ys = find_histogram_edges(loghist, bins)
        eval('a' + str(2 * i + 1)).plot(xs, ys, '-k', lw=1)
        eval('a' + str(2 * i + 1)).vlines([0.02,-0.02], -0.1, 2.3, colors='0.5', lw=0.8)

        eval('a' + str(2 * i + 1)).set_xlim([-0.6, 0.6])
        eval('a' + str(2 * i + 1)).set_ylim([-0.1, 2.3])
        eval('a' + str(2 * i + 1)).yaxis.tick_right()
        eval('a' + str(2 * i + 1)).text(-0.5, 1.85, r'${:.1f} \%$'.format(percent_good))


    a2.set_ylabel(r'$z_{LDP}$')
    a3.yaxis.set_label_position('right')
    a3.set_ylabel(r'$\log_{10}(N)$')
    a4.set_xlabel(r'$z_{spec}$')
    a5.set_xlabel(r'$\Delta z = |z_{LDP} - z_{spec}|$')
    plt.savefig('../just2017plots/zvz.png', dpi=300)

    #print len(primus_table[np.where(primus_table['Q'] >= 2)])






if __name__ == '__main__':
    main()
