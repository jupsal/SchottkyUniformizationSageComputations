###############################################################################
# Plotting associated with the Schottky uniformization is here. I.e. the region,
# calculated branch points, etc.
###############################################################################

from sage.all import *

# plot_circles plots ONLY the unit circle and the interior circle. No filling.
def circle_plots(delta, q):
	# delta = list of centers of circles
	# q = radius of circles

	# Define our parametric plotting variable
	t = var('t')
        assume(t,'real')
	genus = len(q)
	
	# Define the C0, Cj
	C0 = exp(I*t)
	Cj = lambda j: delta[j] + q[j]*exp(I*t)
	
	# Colors for plotting.
	colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
	                          #multiply the first one by 0.6 so nothing is TOO red
	
	# Plot the circles, identifying edges with like colors.
	## First plot C_0
	D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
	rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
	## Plot the C_j
	#D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
	#rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
	#range(genus)] )
	D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
	rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
	range(genus)] )
	## Show the graphic
	D_zeta.show(axes = True, title='$D_{zeta}$', aspect_ratio = 1) # show and
                                                    # put on an equal-axis plot
	

# plot_F plots the fundamential region, F, including filling and Cjp
def F_plot(delta, q):
	# delta = list of centers of circles
	# q = radius of circles

	# Define our parametric plotting variable
	t = var('t')
        assume(t,'real')
	genus = len(q)
        x,y = var('x,y', domain='real')
        zeta = x+I*y # For the fill plot.
	
	# Define the C0, Cj, Cjp
	C0 = exp(I*t)
	Cj = [ delta[j] + q[j]*exp(I*t) for j in range(genus) ]
	Cjp = [ 1/circle.conjugate() for circle in Cj ]
	
	# Define circles for filling regions D_zeta and D_zeta'
	C0_fill = norm(zeta)-1 # norm(zeta) = x^2+y^2, sage syntax
        Cj_fill = [ norm(zeta-delta[j]) - q[j]**2 for j in range(genus) ]
                                        # norm(z) = x^2+y^2, a sage syntax
	Cjp_fill = [ norm(1/zeta.conjugate()-delta[j]) - q[j]**2 for j in
                range(genus) ] # norm(z) = x^2+y^2, a sage syntax
	
	# Colors for plotting
	colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
	                          #multiply the first one by 0.6 so nothing is TOO red
	
        # Get the right viewing window. Calculate the maximum on the real axis
        xplot_range = [max( [ abs(circle.substitute(t=0)) for circle in Cjp ] )]
        xplot_range += [max( [ abs(circle.substitute(t=pi)) for circle in Cjp ]
            )]
        xplot_range = max( xplot_range+[1] ) # Add 1 to make sure we at least
                                             # get the unit circle
        yplot_range = [max( [ norm(CDF(circle.substitute(t=pi/2))) for circle in
            Cjp ] )]
        yplot_range += [max( [ norm(CDF(circle.substitute(t=-pi/2))) for circle
            in Cjp ] )]
        yplot_range = max( yplot_range+[1] ) # Add 1 to make sure we at least get
                                            # the unit circle
	
	# Plot the circles, identifying edges with like colors.
	## First plot C_0
	D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
	    rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
	## Plot the C_j
	D_zeta += sum( [line( [CC(Cj[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
	    rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) )
            for j in range(genus)] )
	## Plot the C_j'
	D_zeta += sum( [line( [CC(Cjp[j](t=v)) for v in srange(0,2*pi+0.2,0.1)],
	    rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
	## Fill the two regions, D_\zeta and D_zeta'
	D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='red', borderwidth=0, alpha=0.2
            )
	D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill[k])>0
            for k in range(0,genus)], (x,-xplot_range,xplot_range),
            (y,-yplot_range,yplot_range), incol='blue', borderwidth=0, alpha=0.2
            )
	## Show the graphic
	D_zeta.show(axes = True, title='$D_{zeta}$')
	
# Plots the branch points on the line
def branch_point_plot(b_pts):
	# input:
	#	b_pts = branch points
	#
	# output:
	# 	none

	branch_plot = sum( [point( CC(bp), marker='x', size=50,
            rgbcolor='red' ) for bp in b_pts] )
	branch_plot.show(axes = True, title='Branch Points')
