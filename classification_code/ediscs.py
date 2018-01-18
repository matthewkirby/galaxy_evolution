import ds9


def display_image(image, d):
    # Set the ds9 display mode to tile.
    d.set("tile yes")
    d.set("tile mode column")

    # Display the FITS file in the first ds9 frame.
    # d.showFITSFile('/Users/desai/research/ediscs/wide_field/visual_classifications/images/w1.fits')
    d.set('file ' + image)

    # Display the same FITS file in the second ds9 frame.
    d.set("frame 2")
    # d.showFITSFile('/Users/desai/research/ediscs/wide_field/visual_classifications/images/w1.fits')
    d.set('file ' + image)

    # Zoom the image to fit the ds9 frame.
    d.set("zoom to fit")

    # Scale the ds9 mage.
    d.set("scale log")
    # d.set("scale limits -0.1 2")

    # Zoom the image to fit the first ds9 frame.
    d.set("frame 1")
    d.set("zoom to fit")

    # Scale the ds9 image so that it has a log scale between -0.1 and 2 DN/s.
    d.set("scale log")
    # d.set("scale limits -0.1 25")


def keycheck(key, arr, default):
    if key in arr.keys():
        return arr[key]
    else:
        return default


def print_classifications(header):
    print 'Current Morphology:'
    print ''

    print 'MORPH=' + keycheck('MORPH', header, '')
    print ''


def print_flags(header):
    print ''
    print 'Current Flags:'
    print ''

    print '1. SODISK=' + keycheck('SODISK', header, '')
    print '2. BAR=' + keycheck('BAR', header, '')
    print '3. EDGEON=' + keycheck('EDGEON', header, '')
    print '4. SMALL=' + keycheck('SMALL', header, '')
    print '5. LSB=' + keycheck('LSB', header, '')
    print '6. DEFECT=' + keycheck('DEFECT', header, '')
    print '7. DUST=' + keycheck('DUST', header, '')
    print '8. DISTURBED=' + keycheck('DISTURBED', header, '')
    print ''


def print_morph_choices():
    print 'Star=-7'
    print 'nonstellar but compact=-6'
    print 'E=-5'
    print 'S0=-2'
    print 'Sa=1'
    print 'Sb=3'
    print 'Sc=5'
    print 'Sd=7'
    print 'Sm=9'
    print 'Irr=11'
    print 'unclassifiable=66'
    print ''