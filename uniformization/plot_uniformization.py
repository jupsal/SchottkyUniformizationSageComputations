###############################################################################
# Plotting associated with the Schottky uniformization is here. I.e. the region,
# calculated branch points, etc.
###############################################################################

from sage.all import *

# plot_circles plots ONLY the unit circle and the interior circle. No filling.
def circle_plots(delta, q, colors=[], field=CDF):
    #
    # This module plots the circles from group data in the complex plane
    # input:
    #   delta = list of centers of circles
    #   q = radius of circles
    #   colors = list of len genus of RGBcolors for uniform plotting
    #   field = which field do we want to work with? CDF by default because it's
    #            cheapest. Should only get CC or CDF for this.
    # 
    # output:
    #   D_zeta = plot data. To show this plot it is recommended to use 
    #       D_zeta.show(axes=True, title='$D_{\zeta}$', aspect_ratio=1)
    #
    
    genus = len(q)
    
    # Define the C0, Cj
    C0 = lambda t: exp(I*t)
    Cj = [ lambda t, j=j: delta[j] + q[j]*exp(I*t) for j in xrange(genus) ]
    # use lambda t, j=j so that j is fixed for each element in the list Cj

    # Colors for plotting, if not already passed.
    if len(colors)==0:
        colors = [(0.6*random(),random(),random()) for k in range(genus)]
         #For plotting, multiply the first one by 0.6 so nothing is TOO red
    
    # Plot the circles, identifying edges with like colors.
    ## First plot C_0
    D_zeta = line( [field(C0(v)) for v in srange(0,2*pi+0.2,0.1)], 
            linestyle='--', rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )

    ## Plot the C_j. first create a list of lists so that CjData[0] is the 0th
    ##    circle as a bunch of data points.
    CjData = [ map(field,map(circle, srange(0,2*pi+0.2,0.1)))
                for circle in Cj ]

    D_zeta += plot_lines( CjData, colors=colors, thickness=3, 
                            group_circles=True )
    
    return D_zeta
	

def F_plot(delta, q, colors=[], field=CDF):
    #
    # This module  plots the fundamential region, F, including filling and Cjp
    #
    # input:
    #   delta = list of centers of circles
    #   q = radius of circles
    #   colors = list of len genus of RGBcolors for uniform plotting
    #   field = underlying field, CC or CDF
    #
    # output:
    #   D_zeta = plot data
    #

    # Define our parametric plotting variable
    #t = var('t')
    #assume(t,'real')
    genus = len(q)
    x,y = var('x,y', domain='real')
    zeta = x+I*y # For the fill plot.

    # Define the C0, Cj, Cjp
    C0 = lambda t: exp(I*t)
    Cj = [ lambda t, j=j: delta[j] + q[j]*exp(I*t) for j in xrange(genus) ]
    #Cj = [ delta[j] + q[j]*exp(I*t) for j in range(genus) ]
    #Cjp = [ 1/circle.conjugate() for circle in Cj ]

    Cjp = [ lambda t, j=j: (conjugate(delta[j]) + q[j]*exp(-I*t))**(-1.) 
                for j in xrange(genus) ]
    
    # Define circles for filling regions D_zeta and D_zeta'
    C0_fill = norm(zeta)-1 # norm(zeta) = x^2+y^2, sage syntax
    Cj_fill = [ norm(zeta-delta[j]) - q[j]**2 for j in range(genus) ]
                                        # norm(z) = x^2+y^2, a sage syntax
    Cjp_fill = [ norm(1/zeta.conjugate()-delta[j]) - q[j]**2 for j in
                range(genus) ] # norm(z) = x^2+y^2, a sage syntax
    
    # Colors for plotting, if colors not already passed.
    if len(colors)==0:
        colors = [(0.6*random(),random(),random()) for k in range(genus)]
         #For plotting, multiply the first one by 0.6 so nothing is TOO red

	
    
    # Get the right viewing window. Calculate the maximum on the real axis
   # xplot_range = [max( [ abs(circle.substitute(t=0)) for circle in Cjp ] )]
   # xplot_range += [max( [ abs(circle.substitute(t=pi)) for circle in Cjp ]
   #     )]
   # xplot_range = max( xplot_range+[1] ) # Add 1 to make sure we at least
   #                                      # get the unit circle
   # yplot_range = [max( [ norm(CDF(circle.substitute(t=pi/2))) for circle in
   #     Cjp ] )]
   # yplot_range += [max( [ norm(CDF(circle.substitute(t=-pi/2))) for circle
   #     in Cjp ] )]
   # yplot_range = max( yplot_range+[1] ) # Add 1 to make sure we at least get
   #                                     # the unit circle

    xplot_range = [max( [ abs(circle(0)) for circle in Cjp ] )]
    xplot_range += [max( [ abs(circle(pi)) for circle in Cjp ]
        )]
    xplot_range = max( xplot_range+[1] ) # Add 1 to make sure we at least
                                         # get the unit circle
    yplot_range = [max( [ norm(field(circle(pi/2))) for circle in
        Cjp ] )]
    yplot_range += [max( [ norm(field(circle(-pi/2))) for circle
        in Cjp ] )]
    yplot_range = max( yplot_range+[1] ) # Add 1 to make sure we at least 
                                         # get the unit circle
    
    # Plot the circles, identifying edges with like colors.
    ## First plot C_0
    #D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
    #    rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
    D_zeta = line( [field(C0(v)) for v in srange(0,2*pi+0.2,0.1)], 
            linestyle='--', rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
    ## Plot the C_j
    #D_zeta += sum( [line( [CC(Cj[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
    #    rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) )
    #        for j in range(genus)] )
    
    CjData = [ map(field, map(circle, srange(0,2*pi+0.2,0.1)))
                for circle in Cj ]
    D_zeta += plot_lines( CjData, colors=colors, thickness=3,
                            group_circles=True )

    ## Plot the C_j'
    CjpData = [ map(field, map(circle, srange(0,2*pi+0.2,0.1))) 
                for circle in Cjp ]
    D_zeta += plot_lines( CjpData, colors=colors, thickness=3,
                            group_circles=True )

    ## Plot the C_j'
    #D_zeta += sum( [line( [CC(Cjp[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
    #    rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
    ## Fill the two regions, D_\zeta and D_zeta'
    D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='red', borderwidth=0, alpha=0.2
            )
    D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='blue', borderwidth=0, alpha=0.2
            )
	
    return D_zeta

def branch_point_plot(b_pts):
    #
    # This module plots the branch points on the line
    #
    # input:
    #	b_pts = branch points
    #
    # output:
    # 	branch_plot = plot data. Use  branch_plot.show(axes = True,
    # 	title='Branch Points') to plot for example

    
    branch_plot = sum( [point( CC(bp), marker='x', size=50,
            rgbcolor='red' ) for bp in b_pts] )
    return branch_plot

def plot_points(
    Points, colors=[], mark=[], mark_size=50
    ):
    #
    # This module plots points in a certain color
    #
    # input:
    #   Points = points to plot, given as a list.
    #   colors = RGBcolors for plotting the points. This is passed
    #              in to uniformize colors across various plots
    #   mark = marker for plotting. Default is 'x' to show it's there
    #   mark_size = size of marker for plotting. Default is 50, it is big. Make
    #              it smaller for lines etc.
    # 
    # output:
    #   plot_data = plot output data. To be added to another plot ideally
    #
    if len(colors)==0:
        colors = [ (0.6*random(), random(), random()) for k in xrange(len(Points)) ]

    if len(mark)==0:
        mark = ['x','o','v','^','8','s','p','*','h','H','D']

    plot_data = sum( [ point( p, marker=mark[itnum%len(mark)], size=mark_size, 
        rgbcolor=colors[itnum] ) for itnum, p in enumerate(Points) ] )
    
    return plot_data

def plot_lines(
    lines, colors=[], thickness=1, legend_list=[], group_circles=False
    ):
    #
    # This module plots lines in a certain color. This color is fixed for each
    # line. The input MUST be CDF or CC.
    #
    # input:
    #   lines = lines to plot, given as a list of lists. I.e. it must be the
    #   case that lines[0]
    #   colors = RGBcolors for plotting the points. This is often passed
    #              in to uniformize colors across various plots
    #   thickness = line thickness for plotting
    #   l_label = legend label. By default there is not one.
    #   group_circles = is this a plot of the circles from the group data? if
    #                    so, make the legend appropriately.
    #   

    num_lines = len(lines)
    if len(colors)==0:
        colors = [ (0.6*random(), random(), random()) for k in
                         xrange(num_lines) ]

    # If this is a circle plot, give the correct legends. This shows up so much
    # it is worth putting here.
    if group_circles:
        legend_list = [ 'C_'+str(k+1) for k in xrange(len(lines)) ]

    # Legend list must be a list of Nones if one was not entered
    if len(legend_list)==0:
        legend_list = [None]*num_lines

    # Check to see that the input is a list of lists
    if type(lines[0]) != list:
        raise TypeError("The argument 'lines' in plot_lines must be a list of "
                " lists. Each element must be a list of complex numbers.")

    # Check to see that the input is CC or CDF type
    if (lines[0][0].parent() != CDF and lines[0][0] != CC):
        raise TypeError("The lines supplied to the module 'plot_lines' must be "
                "either of type CC or CDF.")

    plot_data = sum([ line(L, rgbcolor=colors[itnum], thickness=thickness,
                        legend_label=legend_list[itnum]) 
                        for itnum,L in enumerate(lines)])
    
    return plot_data

