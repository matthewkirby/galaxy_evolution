from astropy.table import Table, vstack
import matplotlib.pyplot as plt

cname_list = ['cl1018_catalog_v7.0.fits',
              'cl1037_catalog_v7.0.fits',
              'cl1040_catalog_v7.0.fits',
              'cl1054-11_catalog_v7.0.fits',
              'cl1054-12_catalog_v7.0.fits',
              'cl1059_catalog_v7.0.fits',
              'cl1103_catalog_v7.0.fits',
              'cl1138_catalog_v7.0.fits',
              'cl1216_catalog_v7.0.fits',
              'cl1227_catalog_v7.0.fits',
              'cl1232_catalog_v7.0.fits',
              'cl1301_catalog_v7.0.fits',
              'cl1353_catalog_v7.0.fits',
              'cl1354_catalog_v7.0.fits',
              'cl1411_catalog_v7.0.fits',
              'cl1420_catalog_v7.0.fits']

megacat = Table()
for cname in cname_list:
        table = Table.read(cname)
        megacat = vstack([megacat, table])

megacat.write('../personal_catalogs/megacat.fits', format='fits')