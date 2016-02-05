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
	D_zeta.show(axes = True, title='D_zeta')
	

# plot_F plots the fundamential region, F, including filling and Cjp
def F_plot(delta, q):
	# delta = list of centers of circles
	# q = radius of circles

	# Define our parametric plotting variable
	t = var('t')
	genus = len(q)
	
	# Define the C0, Cj, Cjp
	C0 = exp(I*t)
	Cj = lambda j: delta[j] + q[j]*exp(I*t)
	Cjp = lambda j: 1/(Cj(j).conjugate())
	
	# Define circles for filling regions D_zeta and D_zeta'
	C0_fill = abs(zeta)^2-1
	Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
	Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2
	
	# Colors for plotting
	colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
	                          #multiply the first one by 0.6 so nothing is TOO red
	
	# Find a better way to do this.  -- Maybe I actually can just leave it out?
	#xplot_range = 4.5 #to plot for x \in [-xplot_range,xplot_range]
	#yplot_range = 2 #to plot for y \in [-yplot_range,yplot_range]
	
	
	# Plot the circles, identifying edges with like colors.
	## First plot C_0
	D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
	rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
	## Plot the C_j
	D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
	rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
	range(genus)] )
	## Plot the C_j'
	D_zeta += sum( [line( [CC(Cjp(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
	rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
	## Fill the two regions, D_\zeta and D_zeta'
	D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill(k))>0 for k in
	range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
	incol='red', borderwidth=0, alpha=0.2 )
	D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill(k))>0 for k in
	range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
	incol='blue', borderwidth=0, alpha=0.2 )
	## Show the graphic
	D_zeta.show(axes = True, title='D_zeta')
	
# Plots the branch points on the line
def plot_branch_pts(b_pts):
	# input:
	#	b_pts = branch points
	#
	# output:
	# 	none

	branch_plot = sum( [point( CC(bp), marker='x' ) for bp in b_pts] )
	branch_plot.show(axes = True)
