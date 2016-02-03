##############################################################################
# This file should do the backward problem, i.e. starting from an algebraic
# curve, get the group data.

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

circle_plot = False # If true, then 


def main():
	branch_pts = [-8,-6,-1/2,1/2,6,8] # i.e. y^2 = prod(x-e_j)
	genus = branch_pts/2
	if ~len(branch_pts)%2: raise Expection("Right now this module only works for
		hyperelliptic curves with an even number of branch points")
	
	# Define the Cj
	[delta,q] = define_group_data(genus)
	
	# Define phi_j, needed for omega still!
	phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)
    # Make this into a list if we use phi_j more than just once.
	
	# Define the prime function, omega, algebraically
	load("build_prime_function.sage")
	threshold = 100 # this is probably big enough always. Break it off it
					# takes too long!

	signal.signal(signal.SIGALRM,handler)
	signal.alarm(20) #Let it take 20 seconds at most!
	try:
		omega = build_prime_function(threshold,genus) #STILL HAVE TO WRITE THIS
	except Expection, exc
		print exc

	# Define the slit map, algebraically again
	load("slitmap.sage")
	slitmap = slitmap(blah) #NEED TO PUT THIS IN THERE
	





	[delta,q] = define_group_data(1)
	genus = len(q)
	define_circles(delta,q)
	if circle_plot == True:
		define_plotting_circles(delta,q)
		# load("plot_F.sage") # or something

	# Define the points of intersection of the Cj with the real axis. The image
	# of these points under the slitmap (5.19) are the branch points of the
	# curve.
	pre_branch_pts = [Cj[j](t=0) for j in xrange(genus)] #for t=0
	pre_branch_pts += [Cj[j](t=pi) for j in xrange(genus)] #Also for t=pi



# This function defines group data algebraically
def define_group_data(genus):
	delta = list(var('delta_%d' % j) for j in xrange(1,genus+1)) 
	q = list(var('q_%d' % j) for j in xrange(1,genus+1)) 
							# start at 1 to agree with the paper.
	return delta, q
	









































if __name__ == '__main__':
    main()
