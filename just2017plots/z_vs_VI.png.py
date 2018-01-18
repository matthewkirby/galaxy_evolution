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

def calc_outlier_frac(res, thresh):
    good = 0.0
    N = float(len(res))
    for r in res:
        if abs(r) < thresh:
            good+=1.0
    return (N-good)/N

def safediv(x,y):
    if y == 0: return -1
    return x/y

def main():
    plt.rc('text', usetex=True)

    # Open and prepare the table
    full_table = Table().read('../catalogs/personal_catalogs/useable_catalog.csv', format='csv')
    photo = full_table[np.where(full_table['slit_distance'] < 0.5)]
    photo = photo[np.where(photo['Vauto'] > 0)]
    photo = photo[np.where(photo['Iauto'] > 0)]
    zspecs = photo[np.where(photo['zSpec'] > 0)]
    zspecs['VI'] = zspecs['Vauto']-zspecs['Iauto']

    # Separate by Q
    Q4 = zspecs[np.where(zspecs['Q'] == 4)]
    Q3 = zspecs[np.where(zspecs['Q'] == 3)]
    Q2 = zspecs[np.where(zspecs['Q'] == 2)]

    # Calculate the residuals
    res4 = Q4['zLDP']-Q4['zSpec']
    res3 = Q3['zLDP']-Q3['zSpec']
    res2 = Q2['zLDP']-Q2['zSpec']

    # Histogram VI
    hist_edges = np.arange(0.0, 2.6, 0.25)
    x4, y4 = find_histogram_edges(np.histogram(Q4['VI'], hist_edges)[0], hist_edges)
    x3, y3 = find_histogram_edges(np.histogram(Q3['VI'], hist_edges)[0], hist_edges)
    x2, y2 = find_histogram_edges(np.histogram(Q2['VI'], hist_edges)[0], hist_edges)

    # Histogram outliers
    out_edges = np.arange(0.0, 2.6, 0.5)
    of4, of3, of2 = [], [], []
    N4, N3, N2 = [], [], []
    for i in range(1, len(out_edges)):
        inbin = res4[(Q4['VI'] > out_edges[i-1]) & (Q4['VI'] < out_edges[i])]
        N4.append(float(len(inbin)))
        of4.append(calc_outlier_frac(inbin, 0.02))
    for i in range(1, len(out_edges)):
        inbin = res3[(Q3['VI'] > out_edges[i-1]) & (Q3['VI'] < out_edges[i])]
        N3.append(float(len(inbin)))
        if len(inbin) <= 5:
            of3.append(-1)
            continue
        of3.append(calc_outlier_frac(inbin, 0.02))
    for i in range(1, len(out_edges)):
        inbin = res2[(Q2['VI'] > out_edges[i-1]) & (Q2['VI'] < out_edges[i])]
        N2.append(float(len(inbin)))
        if len(inbin) <= 5:
            of2.append(-1)
            continue
        of2.append(calc_outlier_frac(inbin, 0.02))
    xo4, yo4 = find_histogram_edges(of4, out_edges)
    xo3, yo3 = find_histogram_edges(of3, out_edges)
    xo2, yo2 = find_histogram_edges(of2, out_edges)

    # Set up the histogram error bars
    df4 = [of4[i]*np.sqrt(safediv(1., N4[i]) + safediv(1., (N4[i]*of4[i]))) for i in range(0, len(of4))]
    df3 = [of3[i]*np.sqrt(safediv(1., N3[i]) + safediv(1., (N3[i]*of3[i]))) for i in range(0, len(of3))]
    df2 = [of2[i]*np.sqrt(safediv(1., N2[i]) + safediv(1., (N2[i]*of2[i]))) for i in range(0, len(of2))]

    ##############################################################
    # Build the plot
    f, ((a0), (a1), (a2)) = plt.subplots(3,1, gridspec_kw={'height_ratios':[1,2,1]})
    plt.setp([a.get_xticklabels() for a in f.axes[0:-1]], visible=False)
    f.subplots_adjust(hspace=0, wspace=0.1)

    # Make histogram of VI
    a0.plot(x4, y4, '-k', lw=1)
    a0.plot(x3, y3, '-b', lw=1)
    a0.plot(x2, y2, '-r', lw=1)
    a0.set_xlim([0, 2.5])
    a0.set_ylim([0, 60])
    a0.set_ylabel('N')

    # Make and format residuals plot
    a1.axhline(0.0, c='0.5', lw=0.8)
    a1.scatter(Q4['VI'], res4, c='k', s=8, label=r'$Q=4$')
    a1.scatter(Q3['VI'], res3, c='blue', s=8, marker='^', label=r'$Q=3$')
    a1.scatter(Q2['VI'], res2, c='red', s=8, marker='s', label=r'$Q=2$')
    a1.set_xlim([0, 2.5])
    a1.set_ylim([-0.8, 0.3])
    a1.set_ylabel(r'$z_{LDP}-z_{spec}$')
    a1.set_yticks(np.arange(-.6, .3 + .05, .2))
    a1.legend()

    # Make outlier plot
    a2.plot(xo4, yo4, '-k', lw=1)
    a2.plot(xo3, yo3, '-b', lw=1)
    a2.plot(xo2, yo2, '-r', lw=1)

    ebar_centers = out_edges[:-1]+np.diff(out_edges)/2.
    a2.errorbar(ebar_centers-0.04, of4, yerr=df4, fmt='.k', elinewidth=0.8, capsize=2, markersize=0)
    a2.errorbar(ebar_centers, of3, yerr=df3, fmt='^b', elinewidth=0.8, capsize=2, markersize=0)
    a2.errorbar(ebar_centers+0.04, of2, yerr=df2, fmt='sr', elinewidth=0.8, capsize=2, markersize=0)

    a2.set_xlim([0, 2.5])
    a2.set_ylim([0.0, 1.05])
    a2.set_ylabel('Outlier Fraction')
    a2.set_xlabel(r'$(V-I)$')
    a2.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    a2.set_xticks(np.arange(0, 2.6, 0.5))




    #plt.show()
    plt.savefig('zvVI.png', dpi=300)


if __name__ == '__main__':
    main()