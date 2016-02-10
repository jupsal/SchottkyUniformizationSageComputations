###############################################################################
# Defines the function which builds the slit map (5.19) and also each of the
# composition functions which lead to the slitmap. These are in here for
# diagnosing which components are large (dominant) in product for example.
###############################################################################

from sage.all import *

# Build the slitmap all in one step.
def build_slitmap(omega):
    return ( omega(gamma=-1)**2 + omega(gamma=1)**2 )/( omega(gamma = -1)**2 -\
                omega(gamma=1)**2 )

def build_slitmap_detailed(
        omega, delta, q, points=[], pointColors=[], circle_colors=[]
        ):
    #
    # This module builds the maps which, when composed, give the slitmap. Each
    # is plotted individually for diagnostic reasons. The final thing, zed, is
    # the same as the slitmap.
    #
    # input:
    # 	omega = prime function
    # 	delta = center of circles
    # 	q = radius of circles
    #   points(optional) = points whose image we wish to plot in the slitmap
    # 
    # output:
    #   zeta1dataC0, zeta1dataCj, zeta2dataC0, zeta2dataCj, zeddataC0, zeddata 
    #       = image of the appropriate circles under the appropriate maps. Given
    #           as a list in the Cj case.
    #
    
    t = var('t', domain='real') 

    genus = len(q)

    # Get the colors for plotting if not passed. Multiply by 0.6 on the first
    # one so none of the colors are too close to red.
    if len(circle_colors)==0:
        circle_colors = [(0.6*random(),random(),random()) for k in 
                            xrange(genus)]
    
    tstep = 0.01 #step for parametric plotting, smaller is finer.

    # First define the C0, Cj which will be used throughout.
    C0 = exp(I*t)
    Cj = lambda j: delta[j] + q[j]*exp(I*t)
    
    # Start with zeta1
    zeta1 = -omega(gamma=1)/omega(gamma=-1) # -- for reference.
    zeta1dataC0 = [CC(zeta1(z=C0(t=v))) for v in srange(0.0,2*pi+2*tstep,tstep)]
                            #CC it from symbolic to complex for plotting!
    zeta1dataCj = [ [ CC(zeta1(z=Cj(k)(t=v))) for v in\
        srange(0.0,2*pi+2*tstep,tstep) ] for k in range(genus) ]
        # Produces something such that zeta1dataCj[k] gives the image
        # of C_k under zeta1 as a long list with (2*pi+0.2)/0.1 elements.
    zeta1plot = line(zeta1dataC0, rgbcolor=(1,0,0), legend_label='C_0')
    zeta1plot += sum( [ line( zeta1data, rgbcolor = circle_colors[itnum],
        legend_label='C_'+str(itnum+1) ) for itnum, zeta1data in
        enumerate(zeta1dataCj) ] )

    # If 'points' is given as input, then plot them as well.
    if len(points)>0:
        # Check to see if we have colors passed in, if not create them
        if len(pointColors)==0:
            pointColors = [ (0.6*random(), random(), random()) for k in
                                 xrange(len(points)) ]

        zeta1datapoints = [ CC(zeta1(z=p)) for p in points ]
        zeta1plot += sum( [ point(p, marker='x', size=50,
            rgbcolor=pointColors[itnum] ) for itnum, p in
            enumerate(zeta1datapoints) ] )

    zeta1plot.show(title='$\zeta_1$ plot')
    
    ## If we want to examine the image of each circle more, plot one at a time:
    for itnum, zeta1data in enumerate(zeta1dataCj):
        analyze_plot = line(zeta1data, rgbcolor=circle_colors[itnum],
                        legend_label='C_'+str(itnum+1))
        if len(points)>0:
            analyze_plot += sum( [ point( p, marker='x', size=50,
                rgbcolor=pointColors[iternum] ) for iternum, p in
                enumerate(zeta1datapoints) ] )
    
        analyze_plot.show(title='Image of C_'+str(itnum+1)+' under $\zeta_1$')
        # Would like all graphics, but this one in particular, to be EPS format.
    
    
    # Now do it for zeta2
    zeta2 = lambda z: (1-z)/(1+z)
    zeta2dataC0 = [ zeta2(z=zeta1data) for zeta1data in zeta1dataC0 ]
    zeta2dataCj = [ [ zeta2(z=zeta1dataCj[k][j]) for j in
        xrange(len(zeta1dataCj[k])) ] for k in xrange(genus) ]
    # zeta2dataCj can probably be made better with iterators, but blah RN

    zeta2plot = line(zeta2dataC0, rgbcolor=(1,0,0), legend_label='C_0')
    zeta2plot += sum( [ line( zeta2data, rgbcolor=circle_colors[itnum],
        legend_label='C_'+str(itnum+1) ) for itnum, zeta2data in
        enumerate(zeta2dataCj) ] )

    # If 'points' is given as input, then plot them as well.
    if len(points)>0:
        zeta2datapoints = [ CC(zeta2(z=p)) for p in zeta1datapoints ]
        zeta2plot += sum( [ point( p, marker='x', size=50,
            rgbcolor=pointColors[iternum] ) for iternum, p in
            enumerate(zeta2datapoints) ] )

    zeta2plot.show(title='$\zeta_2$ plot', aspect_ratio = 1)
    
    zed = lambda z: 0.5*(1/z + z)
    # Now do it for zed (the last eqn in (5.18))
    zeddataC0 = [ zed(z=zeta2data) for zeta2data in zeta2dataC0 ]
    zeddataCj = [ [ zed(zeta2dataCj[k][j]) for j in xrange(len(zeta2dataCj[k]))
        ] for k in range(genus) ]
    # zeddataCj can probably be made better with iterators, but blah RN

    zedplot = line(zeddataC0, rgbcolor=(1,0,0), legend_label='C_0')
    if len(points)>0:
        zeddatapoints = [ CC(zed(z=p)) for p in zeta2datapoints ]
        zedplot += sum( [ point( p, marker='x', size=50,
            rgbcolor=pointColors[iternum] ) for iternum, p
            in enumerate(zeddatapoints) ] )

    zedplot.show(title='zedplot C_0')
    
    zedplot += sum( [ line( zeddata, rgbcolor=circle_colors[itnum],
        legend_label='C_'+str(itnum+1) ) for itnum, zeddata in
        enumerate(zeddataCj) ] )

    zedplot.show(title='zedplot')

    return zeta1dataC0, zeta1dataCj, zeta2dataC0, zeta2dataCj, zeddataC0,\
            zeddataCj

# Test various things about the slitmap
def test_slitmap(slitmap):
    # input: 
    #	slitmap - the map to be tested.
    #
    # output:
    #	none
    
    
    t = var('t')
    
    # First define the C0, Cj which will be used throughout.
    C0 = exp(I*t)
    Cj = lambda j: delta[j] + q[j]*exp(I*t)
    
    print '------------------------- Slit map tests ---------------------------'
    
    # The first test consists of seeing if the left endpoint of our interval is -1
    # and the right endpoint is 1. We also allow the alternative for "flipped" .i.e.
    # t=0 maps to the left endpoint and t=pi maps to the right endpoint, though this
    # should certainly not occur. If it does we need to examine.
    
    test = 'Passed'
    if (slitmap(z=C0(t=0)) != 1): #make sure we map to 1 or -1
        if (slitmap(z=C0(t=0)) == -1):
            test = 'Passed but FLIPPED'
        else: test = 'Failed' #else test fails
    print 'test1:                                       ', test
    
    #Do the same thing at t=pi
    test = 'Passed'
    if (slitmap(z=C0(t=pi)) != -1):
        if(slitmap(z=C0(t=pi))==1):
            test = 'Passed but FLIPPED'
        else: test = 'Failed'
    print 'test2:                                       ', test
    
    print '------------------------ End slit map tests ------------------------------'
   
    return None
