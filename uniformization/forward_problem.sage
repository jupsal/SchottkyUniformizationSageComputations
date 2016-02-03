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

circle_plot = False # If true, then 


def main():
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

	# Define the "theta_j" function as in "Computational approach..." We will call
	# it phi_j to eliminate confusion with the R. Theta function. This specifies the
	# Schottky group.
	phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)

	# Define the prime function, omega
	load("build_prime_function.sage")
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

def define_circles(delta,q):
	global C0, Cj, Cjp
	C0 = exp(I*t)
	Cj = lambda j: delta[j] + q[j]*exp(I*t) #circles within the unit circle

def define_plotting_circles(delta,q):
	global C0_fill, Cj_fill, Cjp_fill, Cjp
	Cjp = lambda j: 1/(Cj(j).conjugate()) #Reflection of Cj about the unit circle.
	## Define circles for filling regions D_zeta and D_zeta' as well.
	C0_fill = abs(zeta)^2-1
	Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
	Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2
	
	return None



















if __name__ == '__main__':
    main()


