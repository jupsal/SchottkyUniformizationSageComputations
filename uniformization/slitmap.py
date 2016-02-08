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

# Build the maps which, when composed, give the slitmap. Each individually for
# diagnostic reasons. The final thing, zed, is the same as the slitmap.
def build_slitmap_detailed(omega, delta, q):
    # input:
    # 	omega = prime function
    # 	delta = center of circles
    # 	q = radius of circles
    # 
    # output:
    #   zeta1dataC0, zeta1dataCj, zeta2dataC0, zeta2dataCj, zeddataC0, zeddata 
    #       = image of the appropriate circles under the appropriate maps. Given
    #           as a list in the Cj case.
    
    genus = len(q)

    colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
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
    zeta1plot += sum( [line( zeta1dataCj[k], rgbcolor = colors[k],
    legend_label='C_'+str(k+1) ) for k in range(genus)] )
    zeta1plot.show(title='zeta1plot')
    
    ## If we want to examine the image of each circle more, plot one at a time:
    for k in range(genus):
            analyze_plot = line(zeta1dataCj[k], rgbcolor=colors[k],
                    legend_label='C_'+str(k+1))
            analyze_plot.show(title='Image of C_'+str(k+1)+' under zeta_1')
    
    
    # Now do it for zeta2
    zeta2dataC0 = [ (1-zeta1dataC0[k])/(1+zeta1dataC0[k]) for k in\
                        range(len(zeta1dataC0)) ]
    zeta2dataCj = [ [(1-zeta1dataCj[k][j])/(1+zeta1dataCj[k][j]) for j in\
                        range(len(zeta1dataCj[k])) ] for k in range(genus) ]
    zeta2plot = line(zeta2dataC0, rgbcolor=(1,0,0), legend_label='C_0')
    zeta2plot += sum( [line( zeta2dataCj[k], rgbcolor = colors[k],
    legend_label='C_'+str(k+1) ) for k in range(genus)] )
    zeta2plot.show(title='zeta2plot', aspect_ratio = 1)
    
    # Now do it for zed (the last eqn in (5.18))
    zeddataC0 = [ 0.5*(1/zeta2dataC0[k] + zeta2dataC0[k]) for k in
    range(len(zeta2dataC0)) ]
    zeddataCj = [ [ 0.5*(1/zeta2dataCj[k][j] + zeta2dataCj[k][j]) for j in
    range(len(zeta2dataCj[k])) ] for k in range(genus) ]
    zedplot = line(zeddataC0, rgbcolor=(1,0,0), legend_label='C_0')
    zedplot.show(title='zedplot C_0')
    zedplot += sum( [line( zeddataCj[k], rgbcolor = colors[k],
    legend_label='C_'+str(k+1) ) for k in range(genus)] )
    zedplot.show(title='zedplot')

    return zeta1dataC0, zeta1dataCj, zeta2dataC0, zeta2dataCj, zeddataC0,\
            zeddata	

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
