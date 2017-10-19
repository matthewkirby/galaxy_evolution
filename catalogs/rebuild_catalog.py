import sys, os

# None of this is tested

os.remove('personal_catalogs/megacat.fits')
os.chdir('ediscs_v7.0')

# Build the base catalog
os.system('build_megacat.py')

# Add LDP information
os.chdir('..')
os.system('merge_ldp_fors2.py')