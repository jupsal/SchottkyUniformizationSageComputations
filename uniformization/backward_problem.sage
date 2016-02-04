##############################################################################
# This file should do the backward problem, i.e. starting from an algebraic
# curve, get the group data.

import signal #For breaking up a function call if it is too slow
import numpy as np

def handler(signum, frame): #handler for signal
	print "Forever is over!"
	raise Exception("Computation of omega taking too long")


x,y = var('x,y')
assume(x,'real'); assume(y,'real')
zeta = x+I*y #local variable
t = var('t') # for parametric plotting
z = var('z') # complex variable not specified by x,y
gamma = var('gamma') #base point for 'abelmap' or prime function

circle_plot = False # If true, then 


def main():
	branch_pts = [-8,-6,-1/2,1/2,6,8] # i.e. y^2 = prod(x-e_j)
	# Check to see that the branch points are labeled monotonically. If not we
	# call an exception and ask for a monotonically increasing list.
	if ~is_increasing(branch_pts):
		raise Exception("The branch_pts list must be monotonically increasing")
	
	genus = branch_pts/2 # There are 2g branch_pts
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
	
	# Define phi_j, needed for omega still!
	phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)
    # Make this into a list if we use phi_j more than just once.
	
	# Define the prime function, omega, algebraically
	load("build_prime_function.sage")
	threshold = 100 # this is probably big enough always. Break it off it
					# takes too long!

	signal.signal(signal.SIGALRM,handler)
	signal.alarm(200) #Let it take 200 seconds at most!
	try:
		omega = build_prime_function(threshold,genus) #STILL HAVE TO WRITE THIS
	except Expection, exc
		print exc

	# Define the slit map, algebraically again
	load("slitmap.sage")
	slitmap = slitmap(blah) #NEED TO PUT THIS IN THERE

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
	if circle_plot == True:
		define_circle(delta,q)
		# I really don't need to shade. That's only for presentation.
		call("plot_circles.sage")

	



# This function defines group data algebraically
def define_group_data(genus):
	delta = list(var('delta_%d' % j) for j in xrange(1,genus+1)) 
	q = list(var('q_%d' % j) for j in xrange(1,genus+1)) 
							# start at 1 to agree with the paper.
	return delta, q
	
def is_increasing(list):
	dx = np.diff(list)
	return np.all(dx>=0)

def define_circles(delta,q):
	global C0, Cj, Cjp
    C0 = exp(I*t)
    Cj = lambda j: delta[j] + q[j]*exp(I*t)
    Cjp = lambda j: 1/(Cj(j).conjugate()) #Reflection of Cj about the unit
							#circle.
	return None

def define_plotting_circles(delta,q):
    global C0_fill, Cj_fill, Cjp_fill
    ## Define circles for filling regions D_zeta and D_zeta' as well.
    C0_fill = abs(zeta)^2-1
    Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
    Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2

    return None







































if __name__ == '__main__':
    main()
