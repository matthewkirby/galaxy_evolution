# This script displays two side-by-side versions of a 200 x 200 square pixel
# cutout centered on each galaxy meeting the magnitude limit described above.
# One version is on a log scale between -0.1 to 2 DN/s, while the other is on a
# log scale between -0.1 to 25 DN/s.
# python classify_galaxies.py images/imagelist.txt
import ds9
import sys
from astropy.io import fits
import ediscs

# Read the list of images.
print ''
print "Reading in list of images in %s" % sys.argv[1]
print ''
file = open(sys.argv[1], 'rU')
content = file.readlines()

# Open a ds9 window.
d = ds9.ds9()

# For each image,
quitflag = 0
for item in content:

    # Intialize control flags.
    changeflag = 0
    skipmorph = 0
    skipflags = 0

    if quitflag == 0:
        # Let the user know which image they are working on.
        print '-------------------------'
        print ''
        print 'Current image:'
        print item

        # Send image to ds9 display
        ediscs.display_image(item, d)

        # Read image header and data.
        f = fits.open(item, mode='update')
        header = f[0].header

        # Print existing classifications in f[0].header and morphology choices.
        ediscs.print_classifications(f[0].header)
        ediscs.print_morph_choices()

        # Give user option of updating morphology.
        while quitflag == 0 and skipmorph == 0:

            newmorph = raw_input('Press RETURN to keep the current classification or enter a new one (q for quit):')

            if newmorph == 'q':
                quitflag = 1
            elif newmorph == '':
                skipmorph = 1
            else:
                changeflag = 1
                header['MORPH'] = newmorph

        # Give user option of setting flags.
        while quitflag == 0 and skipflags == 0:
            # Print current status of flags.
            ediscs.print_flags(f[0].header)
            newflag = raw_input(
                'Which flag would you like to set (enter flag number, RETURN for next galaxy, or q for quit)?')

            if newflag == 'q':
                quitflag = 1
            elif newflag == '':
                skipflags = 1
                if changeflag == 1:
                    f.close()
                    print ''
                    print 'The header has been updated.'
            else:
                changeflag = 1
                if newflag == '1':
                    f[0].header.append(('S0DISK', '1', 'SO Disk'))
                    print f[0].header['S0DISK']
                elif newflag == '2':
                    f[0].header.append(('BAR', '1', 'Bar'))
                elif newflag == '3':
                    f[0].header.append(('EDGEON', '1', 'Edge On'))
                elif newflag == '4':
                    f[0].header.append(('SMALL', '1', 'Smal'))
                elif newflag == '5':
                    f[0].header.append(('LSB', '1', 'Low Surface Brightness'))
                elif newflag == '6':
                    f[0].header.append(('DEFECT', '1', 'Defect'))
                elif newflag == '7':
                    f[0].header.append(('DUST', '1', 'Dust'))
                elif newflag == '8':
                    f[0].header.append(('DISTURBED', '1', 'Disturbed'))

        if quitflag == 1:
            d.set("exit")
            if changeflag == 1:
                f.close()
                print ''
                print 'The header has been updated.'