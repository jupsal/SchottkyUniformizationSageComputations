###############################################################################
# This file should hold all of the stuff to do the forward problem, i.e. from
# group data construct branch places and hence the algebraic curve.
###############################################################################
import signal #For breaking up a function call if it is too slow

def handler(signum, frame): #handler for signal
	print "Forever is over!"
	raise Exception("Computation of omega taking too long")


x,y = var('x,y')
assume(x,'real'); assume(y,'real')
zeta = x+I*y #local variable
t = var('t') # for parametric plotting
z = var('z') # complex variable not specified by x,y
gamma = var('gamma') #base point for 'abelmap' or prime function

plot_circles = True # If true, then 
plot_F = False
prime_function_tests = False # Test to see if prime function is giving what you
							 # want.


def main():
	[delta,q] = define_group_data(0)
	genus = len(q)
#	define_circles(delta,q) ## We actually don't even need the circles for the
#	forward problem in the hyperelliptic case (all of the circles centered on
#	the real axis) since we can just take the pre_branch_pts (below) to be
#	delta_j \pm q_j. Therefore, we only include it in the following "if_plot"
#	check. However, we keep it a separate function since we may actually need
#	the circles and to see where they intersect the axis in the non
#	hyperelliptic case.

	# Plotting
	if plot_circles: load("plot_circles.sage") # Plot just the unit circle and
											   # the Cj
	if plot_F: load("plot_F.sage") # Plot the whole fundamental region

	# Define the points of intersection of the Cj with the real axis. The image
	# of these points under the slitmap (5.19) are the branch points of the
	# curve.
	# For the hyperelliptic case this is easy, we know what the circles look
	# like so this is where they intersect. For the nonhyperelliptic case we
	# need to do something else maybe. For example, evaluate Cj(t=0)?
	pre_branch_pts = [ delta[j]-q[j] for j in xrange(genus) ]
	pre_branch_pts += [ delta[j]+q[j] for j in xrange(genus) ]

	# Define the "theta_j" as in "Computational approach...", which we call
	# "phi_j", and load the defined function "build_prime_function"
	phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)

	# Define the prime function, omega
	load("build_prime_function.sage") # Now the function "build_prime_function"
									  # is available.

	threshold = 100 # this is probably big enough always. Break it off it
					# takes too long!

	signal.signal(signal.SIGALRM,handler)
	signal.alarm(20) #Let it take 20 seconds at most!
	try:
		omega = build_prime_function(threshold,len(q)) #STILL HAVE TO WRITE THIS
	except Expection, exc
		print exc
	
	# Define the slit map
	load("slitmap.sage")
	slitmap = build_slitmap(omega)

	# Branch points are the image of pre_branch_pts
	branch_pts = [slitmap(z = bp) for bp in pre_branch_pts]



def define_group_data(example_num):
	if example_num == 0:
		return [-1/2,1/2], [1/4,1/4] #delta, q

	if example_num == 1:
		return [-3/4,-1/4,1/2], [1/18,1/18,1/4]



















if __name__ == '__main__':
    main()


