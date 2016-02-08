##############################################################################
# This file should do the backward problem, i.e. starting from an algebraic
# curve, get the group data.
#
# Requires: branch_pts
#############################################################################

import signal #For breaking up a function call if it is too slow
import numpy as np

def handler(signum, frame): #handler for signal
	print "Calculation of the prime function taking too long. Consider lowering product_threshold or increasing max_time"
	raise Exception("Exiting from build_prime_function")

max_time = 30 # take at MOST 30 seconds to compute the prime function omega

z = var('z') # complex variable not specified by x,y
gamma = var('gamma') #base point for 'abelmap' or prime function

# Define option variables if they do not exist.
if 'plot_circles' not in locals(): plot_circles = False # If true, then plot circles
if 'plot_F' not in locals(): plot_F = False
if 'prime_function_tests' not in locals():
	prime_function_tests = False # Test to see if prime function is giving what you
                             # want.
if 'plot_branch_pts' not in locals(): plot_branch_pts = False


product_threshold = 12 #this product_threshold determines the maximum number of terms in the product we take for omega.

def main():
	# Check to see that the branch points are labeled monotonically. If not we
	# call an exception and ask for a monotonically increasing list.
	if ~is_increasing(branch_pts):
		raise Exception("The branch_pts list must be monotonically increasing")
	
	genus = len(branch_pts)/2 # There are 2g branch_pts
	if ~len(branch_pts)%2: raise Expection("Right now this module only works for
		hyperelliptic curves with an even number of branch points")
	
	# Define the Cj algebraically
	[delta,q] = define_group_data(genus) # We have delta[0] = delta_1, delta[1]
								# = delta_2 etc. Kind of messy but it works out.
								# There are g of each delta_j, q_j

	# Define the location of the intersection of the C_j with the real axis. We
	# have C_j = delta_j + q_j e^(it) centered on the real-axis. Therefore, for
	# the hyperelliptic case we just take one pre-branch point (i.e. the
	# preimage of the branchpoint under the slitmap) to be delta_j + q_j and the
	# other to be delta_j - q_j.
	# -------!!!!----!!!-- Question for non hyperelliptic case: What is
	# important about taking the intersectin of C_j with the real-axis? Are we
	# guaranteed that  -- These are defined algebraically.
	pre_branch_pts = [None]*2*len(xrange(genus))
	pre_branch_pts[::2] = [ delta[j]-q[j] for j in xrange(genus) ]
	pre_branch_pts[1::2] = [ delta[j]+q[j] for j in xrange(genus) ]
	# There are 2g pre_branch_pts. We interlace them in this way to help with
	# the algebraic problem below.
	
	# Define the phi_j and the prime function, omega, algebraically in the following module
	load("build_prime_function.sage") # Now the function "build_prime_function" is available. Also gives local access to phi_j as a list

	signal.signal(signal.SIGALRM,handler)
	signal.alarm(max_time) #Let it take max_time seconds at most!
	try:
		#see file "build_prime_function.sage" to see how this prime function builder construction works.
		omega = build_prime_function(product_threshold) #STILL HAVE TO WRITE THIS
	except Expection, exc:
		print exc

	# Define the slit map, algebraically again
	load("slitmap.sage")
	slitmap = build_slitmap()

	# Map the pre_branch_pts to the branch points under the slit map. The result
	# is an algebraic expression which we compare to the true branch_pts. There
	# are 2g alg_branch_pts
	alg_branch_pts = map(slitmap,pre_branch_pts)

	# Now we want to solve this system. There are 2g unknown alg_branch_pts and
	# 2g known branch_pts. Therefore we have 2g equations in 2g unknowns. Solve
	# it up!!!
	# I don't know if this will just work like this. I imagine it will be
	# slow...
	# We also want to be careful to organize these well. We want the first
	# equation to be delta_1 - q_1 = e_1, delta_1 + q_1 = e_2 etc. The numbering
	# doesn't matter but we do want the two adjacent branch points to be labeled
	# by delta - q and delta + q respectively. 
	eqns = [ alg_branch_pts[k] == branch_pts[k] for k in xrange(len(branch_pts)) ]
	sol = solve(eqns, delta+q, solution_dict=True) # Solve and get a dictionary
	delta = [sol[delt] for delt in delta] # Loop over the variables in delta,
										  # i.e. delta_0,delta_1,... 
										  # and grab them from the dictionary
	q = [sol[cue] for cue in q]
	
	# Great! Now we have the circles. Plot them for funsies.
	if plot_circles:
		load("./plotting/plot_circles.sage") # Plot just the unit circle and the Cj
	if plot_F: load("./plotting/plot_F.sage") # Plot the whole fundamental region
	
	return None #end main()



# This function defines group data algebraically
def define_group_data(genus):
	delta = list(var('delta_%d' % j) for j in xrange(1,genus+1)) 
	q = list(var('q_%d' % j) for j in xrange(1,genus+1)) 
							# start at 1 to agree with the paper.
	return delta, q
	
def is_increasing(list):
	dx = np.diff(list)
	return np.all(dx>=0)



















if __name__ == '__main__':
    main()
