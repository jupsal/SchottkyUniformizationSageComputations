###############################################################################
# Defines the function which builds the slit map (5.19) and also each of the
# composition functions which lead to the slitmap. These are in here for
# diagnosing which components are large (dominant) in product for example.
###############################################################################

from sage.all import *
from uniformization.plot_uniformization import plot_lines, plot_points

# Build the slitmap all in one step.
def build_slitmap(omega):
    return ( omega(gamma=-1)**2 + omega(gamma=1)**2 )/( omega(gamma = -1)**2 -\
                omega(gamma=1)**2 )

def build_slitmap_detailed(
        omega, delta, q, Points=[], Lines=[], point_colors=[], circle_colors=[],
        line_colors=[], field=CDF, point_size=50, save_plots=False
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
    #   Points(optional) = points whose image we wish to plot in the slitmap
    #   Lines(optional) = lines whose image we wish to plot in the slitmap
    #   point_colors(optional) = colors for points, passable to keep things
    #                           uniform
    #   circle_colors(optional) = colors for circles, passable to keep things
    #                           uniform
    #   line_colors(optional) = colors for lines, passable to keep things
    #                           uniform
    #   field = which field do we want to work over? Must be CC or CDF for
    #           plotting lines
    #   point_size = marker size for point_plot
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
    zeta1dataC0 = [field(zeta1(z=C0(t=v))) for v
                                in srange(0.0,2*pi+2*tstep,tstep)]
                            #CC it from symbolic to complex for plotting!
    zeta1dataCj = [ [ field(zeta1(z=Cj(k)(t=v))) for v in\
        srange(0.0,2*pi+2*tstep,tstep) ] for k in range(genus) ]
        # Produces something such that zeta1dataCj[k] gives the image
        # of C_k under zeta1 as a long list with (2*pi+0.2)/0.1 elements.
        # This can probably be optimized.

    zeta1plot = line(zeta1dataC0, rgbcolor=(1,0,0), legend_label='C_0',
                        linestyle='--')

    zeta1plot += plot_lines( zeta1dataCj, colors=circle_colors, 
                             group_circles=True )
    #zeta1plot += sum( [ line( zeta1data, rgbcolor = circle_colors[itnum],
    #    legend_label='C_'+str(itnum+1) ) for itnum, zeta1data in
    #    enumerate(zeta1dataCj) ] )

    # If 'points' is given as input, then plot them as well.
    if len(Points)>0:
        # Check to see if we have colors passed in, if not create them
        if len(point_colors)==0:
            point_colors = [ (0.6*random(), random(), random()) for k in
                                 xrange(len(Points)) ]

        zeta1datapoints = [ field(zeta1(z=p)) for p in Points ]
        zeta1plot += plot_points(zeta1datapoints, point_colors,
                            mark_size=point_size)

    if len(Lines)>0:
        # Check to see if we have colors passed in, if not create them
        if len(line_colors)==0:
            line_colors = [ (0.6*random(), random(), random()) for k in
                                 xrange(len(Lines)) ]

        zeta1datalines = [ map(field,map(lambda g: zeta1(z=g), L)) for L
                            in Lines ]
        # Maybe this can be optimzed
        zeta1plot += plot_lines(zeta1datalines, line_colors, thickness=2)

    if save_plots==False:
        zeta1plot.show(title='$\zeta_1$ plot')
    # We usually don't want to save this one.

    #zeta1plot = plot_lines(zeta1datalines, line_colors)
    #zeta1plot.show(title='WTF')
    
    ## If we want to examine the image of each circle more, plot one at a time:
    for itnum, zeta1data in enumerate(zeta1dataCj):
        analyze_plot = line(zeta1data, rgbcolor=circle_colors[itnum],
                        legend_label='C_'+str(itnum+1))
        if len(Points)>0:
            analyze_plot += plot_points(zeta1datapoints, point_colors,
                                 mark_size=point_size)
        if len(Lines)>0:
            analyze_plot += plot_lines(zeta1datalines, line_colors,
                    thickness=2)
    
        if save_plots==False:
            analyze_plot.show(title='Image of C_'+str(itnum+1)+' under $\zeta_1$')
        # We usually don't want to save this one.
    
    
    # Now do it for zeta2
    zeta2 = lambda z: (1-z)/(1+z)
    zeta2dataC0 = [ field(zeta2(z=zeta1data)) for zeta1data in zeta1dataC0 ]
    zeta2dataCj = [ [ field(zeta2(z=zeta1dataCj[k][j])) for j in
        xrange(len(zeta1dataCj[k])) ] for k in xrange(genus) ]

    # zeta2dataCj can probably be made better (optimize) with iterators,
    # but blah RN

    zeta2plot = line(zeta2dataC0, rgbcolor=(1,0,0), legend_label='C_0',
            linestyle='--')
    zeta2plot += plot_lines( zeta2dataCj, colors=circle_colors,
            group_circles=True )
    #zeta2plot += sum( [ line( zeta2data, rgbcolor=circle_colors[itnum],
    #    legend_label='C_'+str(itnum+1) ) for itnum, zeta2data in
    #    enumerate(zeta2dataCj) ] )

    # If 'points' is given as input, then plot them as well.
    if len(Points)>0:
        zeta2datapoints = [ field(zeta2(z=p)) for p in zeta1datapoints ]
        zeta2plot += plot_points(zeta2datapoints, point_colors,
                            mark_size=point_size)

    if len(Lines)>0:
        zeta2datalines = [ map(field, map(zeta2,L)) for L in zeta1datalines ]
        zeta2plot += plot_lines(zeta2datalines, line_colors, thickness=2)

    if save_plots==False:
        zeta2plot.show(title='$\zeta_2$ plot', aspect_ratio = 1)
    # Don't save this one, we usually don't want it.

    zed = lambda z: 0.5*(1/z + z)
    # Now do it for zed (the last eqn in (5.18))
    zeddataC0 = [ field(zed(z=zeta2data)) for zeta2data in zeta2dataC0 ]
    zeddataCj = [ [ field(zed(zeta2dataCj[k][j])) for j in 
        xrange(len(zeta2dataCj[k])) ] for k in range(genus) ]

    # zeddataCj can probably be made better (optimize) with iterators, 
    # but blah RN

    zedplot = line(zeddataC0, rgbcolor=(1,0,0), legend_label='C_0',
                    linestyle='--')
    # Get the axis range for plotting below with lines and points
    ax_rangeC0 = zedplot.get_axes_range()

    zedplot += plot_lines( zeddataCj, colors=circle_colors, 
                            group_circles=True )

    if len(Points)>0:
        zeddatapoints = [ field(zed(z=p)) for p in zeta2datapoints ]
        zedplot += plot_points(zeddatapoints, point_colors, 
                            mark_size=point_size)
        #zedplot += sum( [ point( p, marker='x', size=50,
        #    rgbcolor=point_colors[iternum] ) for iternum, p
        #    in enumerate(zeddatapoints) ] )

    if len(Lines)>0:
        zeddatalines = [ map(field,map(zed, L)) for L in zeta2datalines ]
        zedplot += plot_lines(zeddatalines, line_colors, thickness=2)

    if save_plots==False:
        zedplot.show(title='zedplot')
    else:
        zedplot.save('zedplot.eps')

    # also plot the zedplot C_0 near C_0 in case the lines do interesting
    # things near there. Use the data in ax_range_C0
    zedplot.set_axes_range( ax_rangeC0['xmin'], ax_rangeC0['xmax'], 
            ax_rangeC0['ymin'], ax_rangeC0['ymax'] )
    if save_plots==False:
        zedplot.show(title='zedplot near C_0')
    else:
        zedplot.save('zedplot_C0.eps')

    # also plot the zedplot C_j near C_j in case the lines do interesting
    # things near there.
    # Get the axes range for Cj
    for j in xrange(genus):
        Cplot = line(zeddataCj[j])
        ax_rangeC = Cplot.get_axes_range()
        zedplot.set_axes_range( ax_rangeC['xmin'], ax_rangeC['xmax'], 
                ax_rangeC['ymin'], ax_rangeC['ymax'] )
        if save_plots==False:
            zedplot.show(title='zedplot near C_'+str(j+1))
        else:
            zedplot.save('zed_C_'+str(j+1)+'.eps')



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
