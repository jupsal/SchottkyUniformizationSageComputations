###############################################################################
# This file should hold all of the stuff to do the forward problem, i.e. from
# group data construct branch places and hence the algebraic curve.
#
# It requires: delta, q (group data)
###############################################################################
import signal #For breaking up a function call if it is too slow
from operator import itemgetter ##Test if I REALLY need to import this. I bet it's already there.

def handler(signum, frame): #handler for signal
	print "Calculation of the prime function taking too long. Consider lowering product_threshold or increasing max_time"
	raise Exception("Exiting from build_prime_function")

max_time = 30 # take at MOST 30 seconds to compute the prime function omega

z = var('z') # complex variable
gamma = var('gamma') #base point for 'abelmap' or prime function

# Define option variables if they do not exist.
if 'plot_circles' not in locals(): plot_circles = False # If true, then plot circles
if 'plot_F' not in locals(): plot_F = False
if 'prime_function_tests' not in locals():
	prime_function_tests = False # Test to see if prime function is giving what you
							 # want.
if 'plot_branch_pts' not in locals(): plot_branch_pts = False


product_threshold = 12 # this product_threshold determines the maximum number of terms in the product we take for omega.


def main():
	genus = len(q)
	G = FreeGroup(genus) #Go ahead and define the free group now. We will need it in any case.

#	define_circles(delta,q) ## We actually don't even need the circles for the
#	forward problem in the hyperelliptic case (all of the circles centered on
#	the real axis) since we can just take the pre_branch_pts (below) to be
#	delta_j \pm q_j. Therefore, we only include it in the following "if_plot"
#	check. However, we keep it a separate function since we may actually need
#	the circles and to see where they intersect the axis in the non
#	hyperelliptic case.

	# Plotting
	if plot_circles: load("./plotting/plot_circles.sage") # Plot just the unit circle and
											   # the Cj
	if plot_F: load("../plotting/plot_F.sage") # Plot the whole fundamental region

	# Define the points of intersection of the Cj with the real axis. The image
	# of these points under the slitmap (5.19) are the branch points of the
	# curve.
	# For the hyperelliptic case this is easy, we know what the circles look
	# like so this is where they intersect. For the nonhyperelliptic case we
	# need to do something else maybe. For example, evaluate Cj(t=0)?
	pre_branch_pts = [ delta[j]-q[j] for j in xrange(genus) ]
	pre_branch_pts += [ delta[j]+q[j] for j in xrange(genus) ]

	# Define the Schottky group elements phi_j (theta_j in "A Computational approach..." and define the prime function, omega
	load("build_prime_function.sage") # Now the function "build_prime_function"
									  # is available. Also gives local access to phi_j

	signal.signal(signal.SIGALRM,handler)
	signal.alarm(max_time) #Let it take max_time seconds at most!
	try:
		# see file "build_prime_function.sage" to see how this prime function builder construction works.
		omega = build_prime_function(product_threshold)
	except Exception, exc #stop if it takes too long.
		print exc
	if prime_function_tests:
		load("../prime_function_tests.sage") ## FIGURE OUT HOW TO DO THIS
	
	# Define the slit map
	load("slitmap.sage")
	slitmap = build_slitmap()

	# Branch points are the image of pre_branch_pts
	branch_pts = [slitmap(z = bp) for bp in pre_branch_pts]
	
	if plot_branch_pts:
		branch_plot = sum( [point( CC(bp), marker='x' ) for bp in branch_pts] )
		branch_plot.show(axes = True)


	return None #end main()



if __name__ == '__main__':
    main()


