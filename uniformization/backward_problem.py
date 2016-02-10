##############################################################################
# This file should do the backward problem, i.e. starting from branch points of
# an algebraic curve, get the group data.
#############################################################################

import signal #For breaking up a function call if it is too slow
import numpy as np
from sage.all import *
from uniformization.plot_uniformization import *
from uniformization.prime_function import build_prime_function, test_prime_function
from uniformization.slitmap import *

def handler(signum, frame): #handler for signal
    print "Calculation of the prime function taking too long. Consider "\
              "lowering product_threshold or increasing max_time"
    raise Exception("Exiting from build_prime_function")

def backward_problem(branch_pts, prime_function_tests=False,
slitmap_tests=False, slitmap_full=False, plot_circles=False, plot_F=False,
plot_branch_pts=False, prec='double', product_threshold=5, max_time=200):
    # input:	
    # 	branch_pts = list of branch points
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
    # 	max_time = max time for prime function computation before timeout
    # 							function product
    #
    # output:
    #   delta = list of centers of circles
    #   q = list of radii of circles

    z = var('z') # complex variable not specified by x,y
    gamma = var('gamma') #base point for 'abelmap' or prime function
    
    # Make sure we are in the hyperbollic case.
    if len(branch_pts)%2 != 0: 
        raise ValueError("Right now this module only works for "
		"hyperelliptic curves with an even number of branch points. Try again "
        "with len(branch_pts)%2=0")

    # Force the list to be monotonically increasing. 
    branch_pts = sorted(branch_pts) # the lists are short enough rn 
                                   # this probably isn't too slow. 

    # Make sure no two branch points coincide
    if duplicates_in_list(branch_pts):
        raise ValueError("The list branch_pts cannot have duplicaties. This "
        "program does not yet support branch_pts of multiplicity greater than "
        " 1")
        
    genus = len(branch_pts)/2 # There are 2g branch_pts

    # Change branch point data to double or infinite precision
    if prec == 'double':
        branch_pts = map(CDF, branch_pts) # Complex double field
    elif (prec == 'infinity' or prec == 'inf'):
        branch_pts = map(CC, branch_pts) # infinite precision
    else:
        raise TypeError("Either 'double' or 'infinite' precision must be "
                        "entered for 'prec'")

    # Plot the branch points if you want, not really necessary here.
    if plot_branch_pts: branch_point_plot(branch_pts)

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
    
    # Define the prime function algebraically, make sure it doesn't take too
    # long!
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(max_time) #Let it take max_time seconds at most!
    try:
        omega = build_prime_function(delta, q, product_threshold)
    except Exception, exc: #stop if it takes too long
        print exc
    
    # Test that the prime function obeys certain things that we expect.
    if prime_function_tests: test_prime_function(omega, delta, q)
    
    
    # Define the slit map, algebraically again
    slitmap = build_slitmap(omega)
    
    # Test the slit map if we want -- IS THIS ALLOWED FOR ALGEBRAICALLY DEFINED
    # OMEGA?
    if slitmap_tests: test_slitmap(slitmap) 
    
    # Build the slitmap piece by piece for diagnostic purposes. -- IS THIS
    # ALLOWED FOR ALGEBRAICALLY DEFINED OMEGA?
    if slitmap_full: build_slitmap_detailed(omega, delta, q)
    
    # Map the pre_branch_pts to the branch points under the slit map. The result
    # is an algebraic expression which we compare to the true branch_pts. There
    # are 2g alg_branch_pts
    alg_branch_pts = map(lambda x: slitmap(z=x),pre_branch_pts)
    
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
    # The above thing might give multiple answers, i.e. len(sol)>1. If so, we
    # need to look through all possible answers for now since I do not now know
    # how to determine which is which.
    ####### THIS IS ALL SOOOO WONKY
    deltalist = []
    qlist = []
    for solnum in xrange(len(sol)):
        delta_vals = [sol[solnum][delt] for delt in delta] # Loop over the variables in delta,
                                          # i.e. delta_0,delta_1,... 
                                          # and grab them from the dictionary
        q_vals = [sol[solnum][cue] for cue in q]
        deltalist += [delta_vals]
        qlist += [q_vals]
        
        delta_vals = [delt(1) for delt in delta_vals]
        q_vals = [cue(1) for cue in q_vals]
    
        # Great! Now we have the circles. Plot them for funsies.
        if plot_circles: circle_plots(delta_vals, q_vals) # Plot just the unit circle and the
                                            # Cj
        if plot_F: F_plot(delta_vals, q_vals) # Plot the whole fundamental region
    
    return delta, q



# This function defines group data algebraically
def define_group_data(genus):
    delta = list(var('delta_%d' % j, domain='real') for j in xrange(1,genus+1)) 
    # Do you get something different if you assume the above are real?
    q = list(var('q_%d' % j) for j in xrange(1,genus+1)) 
                        # start at 1 to agree with the paper.
    return delta, q
	
def duplicates_in_list(listy):
    dx = np.diff(listy)
    return np.any(dx==0) # returns true if any duplicates

