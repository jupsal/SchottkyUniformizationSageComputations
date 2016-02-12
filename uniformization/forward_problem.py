###############################################################################
# This file should hold all of the stuff to do the forward problem, i.e. from
# group data construct branch places.
###############################################################################
import signal #For breaking up a function call if it is too slow
from sage.all import *
from uniformization.plot_uniformization import *
from uniformization.prime_function import build_prime_function, test_prime_function
from uniformization.slitmap import *

def handler(signum, frame): #handler for signal
	print "Calculation of the prime function taking too long. Consider \
					lowering product_threshold or increasing max_time"
	raise Exception("Exiting from build_prime_function")


def forward_problem(delta, q, prime_function_tests=False,
slitmap_tests=False, slitmap_full=False, plot_circles=False, plot_F=False, 
plot_branch_pts=False, prec='double', product_threshold=5, max_time=200):
    #
    # This module does the full forward problem. Starting with group data,
    # construct the SK prime function, the slitmap, and hence the branch points
    # of an algebraic curve. 
    #
    # input:	
    # 	delta = list of centers of circles
    # 	q = list of radii of circles
    # 	prime_function_tests = Check to see if the prime function passes some
    # 							tests
    # 	slitmap_tests = Check to see if the slitmap passes some tests
    # 	slitmap_full = Plot each component of the slitmap, for diagnostic
    # 					reasons
    # 	plot_circles = circle plot, unit circle and the Cj excised
    # 	plot_F = Plots the whole fundamental domain, F, with shading
    # 	plot_branch_pts = Plots the branch points with red xs
    #   prec = precision of group data. Double or infinite. Double is faster.
    # 	product_threshold = determines the max number of terms in the prime \
    # 							function product
    # 	max_time = max time for prime function computation before timeout
    #
    # output:
    # 	branch_pts = branch points obtained.
    
    z = var('z') # complex variable
    gamma = var('gamma') #base point for 'abelmap' or prime function
    
    genus = len(q)

    # Change group data to double or infinite precision
    if prec == 'double':
        delta, q = map(CDF, delta), map(CDF, q) # Complex double
    elif (prec=='infinite' or prec=='inf'):
        delta, q = map(CC, delta), map(CC, q) #infinite precision
    else:
        raise TypeError("Either 'double' or 'infinite' precision must be " 
                "entered for 'prec'.")
    

    # Before plotting, define a uniform color scheme to be used throughout all
    # plots so we can keep track of which circle is which.
    circle_colors = [ (0.6*random(), random(), random()) for k in xrange(genus)
                        ]
    # Plot some stuff about the region if we want.
    if plot_circles: 
        D_zeta=circle_plots(delta, q, colors=circle_colors) #returns plot data
        D_zeta.show(axes = True, title='$D_{\zeta}$', aspect_ratio = 1) 
        # show and put on an equal-axis plot

    if plot_F:
        D_zeta=F_plot(delta, q, colors=circle_colors) #returns plot data
        D_zeta.show(axes = True, title='$D_{\zeta}$')
        # show, but maybe not on equal-axis plot.
    
    # Build the prime function, but make sure it doesn't take too long
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(max_time) #Let it take max_time seconds at most!
    try:
        omega = build_prime_function(delta, q, product_threshold)
    except Exception, exc: #stop if it takes too long.
        print exc
    
    # Test that the prime function obeys certain things we expect.
    if prime_function_tests: test_prime_function(omega, delta, q)
    
    # Build the slitmap
    slitmap = build_slitmap(omega)
    
    # Test the slit map
    if slitmap_tests: test_slitmap(slitmap)
    
    # Build the slitmap piece by piece for diagnostic purposes.
    if slitmap_full: build_slitmap_detailed(omega, delta, q,
                circle_colors=circle_colors)
    # this thing can output some stuff for use, but for now it just plots. 
    
    
    # Define the points of intersection of the Cj with the real axis. The image
    # of these points under the slitmap (5.19) are the branch points of the
    # curve.
    # For the hyperelliptic case this is easy, we know what the circles look
    # like so this is where they intersect. For the nonhyperelliptic case we
    # need to do something else maybe. For example, evaluate Cj(t=0)?
    pre_branch_pts = [ delta[j]-q[j] for j in xrange(genus) ]
    pre_branch_pts += [ delta[j]+q[j] for j in xrange(genus) ]
    
    # Branch points are the image of pre_branch_pts
    branch_pts = [slitmap(z = bp) for bp in pre_branch_pts]
    
    # Simple plot of branch points if interested. Shows location.
    if plot_branch_pts:
        branch_plot=branch_point_plot(branch_pts)
        branch_plot.show(axes = True, title='Branch Points')
    
    return branch_pts

def forward_problem_on_Points_and_Lines(
        delta, q, Points, Lines, plot_circles=True, plot_F=False,
        slitmap_full=True, slitmap_direct=False, prec='double', 
        product_threshold=5, max_time=200, prime_function_tests=False, 
        slitmap_tests=False, point_size=80, save_plots=False
        ):
    #
    # This module does the forward problem with test point(s) and line(s) in
    # place. I.e. it places a point somewhere in the fundamental domain, F, 
    # then tracks it as we do the slitmap. Usually we do this using 
    # slitmap_full which will be the default, however, there is a flag for
    # this.
    #
    # input:
    #   delta = centers of circles, list
    #   q = radii of circles, list
    #   Points = points to plot in the domain, list
    #   Lines = lines to plot in the domain, list
    #   plot_circles = plot the circles from the group data and the
    #       points and lines in the fundamental domain together.
    #   plot_F = plot the fundamental domain. Lines are filled in as well.
    #   slitmap_full = build the full slitmap, from zeta1, zeta2, z
    #   slitmap_direct = build the slitmap all in one step. Minimum output.
    #   prec = double or infinite precision of the group data?
    # 	product_threshold = determines the max number of terms in the prime \
    # 							function product
    # 	max_time = max time for prime function computation before timeout
    # 	prime_function_tests = Check to see if the prime function passes some
    # 							tests
    # 	slitmap_tests = Check to see if the slitmap passes some tests
    # 	point_size = marker size for point_plot
    #   save_plots = save the plots or just display them?
    #
    # output:
    #   only plots
    #
    z = var('z') # complex variable
    gamma = var('gamma') #base point for 'abelmap' or prime function
    
    genus = len(q)

    # Generate colors for plotting here since we want them to be uniform across
    # plot_circles and slitmap plots
    circle_colors = [ (0.6*random(), random(), random()) for k in 
            xrange(genus) ]
    point_colors = [ (0.6*random(), random(), random()) for k in
            xrange(len(Points)) ]
    line_colors = [ (0.6*random(), random(), random()) for k in
            xrange(len(Lines)) ]
    # We multiply the "R" by 0.6 so nothing is too red.

    # Change group data to double or infinite precision
    if prec == 'double':
        delta, q = map(CDF, delta), map(CDF, q) # Complex double
        Points = map(CDF, Points)
        Lines = [ map(CDF, line) for line in Lines ]
    elif (prec=='infinite' or prec=='inf'):
        delta, q = map(CC, delta), map(CC, q) #infinite precision
        Points = map(CC, Points)
        Lines = [ map(CC, line) for line in Lines ]
    else:
        raise TypeError("Either 'double' or 'infinite' precision must be " 
                "entered for 'prec'.")
    
    # Plot some stuff about the region if we want.
    if plot_circles:
        D_zeta = circle_plots(delta, q, colors=circle_colors) 
        D_zeta += plot_points(Points, colors=point_colors, 
                            mark_size=point_size)
        D_zeta += plot_lines(Lines, colors=line_colors, thickness=2)

        if save_plots==False:
            D_zeta.show(axes=True, title='$D_{\zeta}$', aspect_ratio=1) 
            # show and put on an equal-axis plot
        else:
            D_zeta.save('circle_plot.eps')

    # Plot F, the fundamental domain
    if plot_F:
        D_zeta = F_plot(delta, q, colors=circle_colors)
        D_zeta += plot_points(Points, colors=point_colors, 
                     mark_size=point_size)
        D_zeta += plot_lines(Lines, colors=line_colors, thickness=2)
        if save_plots==False:
            D_zeta.show(axes = True, title = '$F$, the Fundamental Domain')
        else:
            D_zeta.save('Fundamental_domain.eps')
    
    # Build the prime function, but make sure it doesn't take too long
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(max_time) #Let it take max_time seconds at most!
    try:
        omega = build_prime_function(delta, q, product_threshold)
    except Exception, exc: #stop if it takes too long.
        print exc
    
    # Test that the prime function obeys certain things we expect.
    if prime_function_tests: test_prime_function(omega, delta, q)
    
    # Build the slitmap in full, but right now the functionality does not exist
    # to plot the image of the points in this module. Therefore, this is not
    # advised to use now except to compare to the detailed slitmap to make sure
    # that is working right. Therefore, it is advised for NOW.
    if slitmap_direct:
        slitmap = build_slitmap(omega)
    
    # Test the slit map
    if slitmap_tests: test_slitmap(slitmap)
    
    # Build the slitmap piece by piece for diagnostic purposes. This now also
    # plots the image of the desired points.
    if slitmap_full: 
        build_slitmap_detailed(
                omega, delta, q, Points=Points, Lines=Lines,
                circle_colors=circle_colors, point_colors=point_colors,
                line_colors=line_colors, point_size=point_size,
                save_plots=save_plots
                )

    return None

