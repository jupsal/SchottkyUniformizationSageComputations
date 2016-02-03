###############################################################################
# This file tests different methods for calculating the prime function from
# group data. It compares speed and accuracy.

###
# This has now been completed for tests 0 and 1 but got hung up on method1 for
# test1. Try the next two.
###
# This has now also beet completed for tests 2,3 but got hung up on method1 for
# test3. Output in output2. Try it only on example 4
###
from operator import itemgetter
import time
import signal #For breaking up a function call if it is too slow

def handler(signum, frame): #handler for signal
	print "Forever is over!"
	raise Exception("Computation of omega taking too long")

signal.signal(signal.SIGALRM,handler)


x,y = var('x,y')
assume(x,'real'); assume(y,'real')
zeta = x+I*y #local variable
t = var('t') # for parametric plotting
z = var('z') # complex variable not specified by x,y
gamma = var('gamma') #base point for 'abelmap' or prime function

#methods = {'method1': method1, 'method2': method2, 'method3': method3,
#'method4': method4, 'method5': method5, 'method6': method6, 'method7': method7}
# now if we add a new method just add it to the dictionary, or, if we decide a
# method is bad take it out!

def main():
	global omega1, omega2, omega2a, omega3, omega4, omega5, omega6, omega7

	for test_num in xrange(4,5):
		choose_test(test_num)
		print 'Using test \# '+str(test_num)+' .........'
		for threshold in xrange(3,11):
			print 'product_threshold = ', str(threshold)

			# -- Method 1 -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omega1 = (z-gamma)*method1(len(q),threshold)
				t1 = time.time()
				print 'time to complete method1:		', str(t1-t0)
			except Exception, exc:
				print 'method1'
				print exc

			# -- Method 2 -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omegap = map(lambda x: method2(len(q),x), xrange(1,threshold+1))
				omegap = reduce(operator.mul,omegap,1)
				omega2 = (z-gamma)*omegap
				t1 = time.time()
				print 'time to complete method2:		', str(t1-t0)
			except Exception, exc:
				print 'method2'
				print exc

				# -- Method 2a, try with list comprehension instead of map -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omegap = [method2(len(q),x) for x in xrange(1,threshold+1)]
				omegap = reduce(operator.mul,omegap,1)
				omega2a = (z-gamma)*omegap
				t1 = time.time()
				print 'time to complete method2a:		', str(t1-t0)
			except Exception, exc:
				print 'method2a'
				print exc

				# -- Method 3 -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omegap = [method3(len(q),x) for x in xrange(1,threshold+1)]
				omegap = reduce(operator.mul,omegap,1)
				omega3 = (z-gamma)*omegap
				t1 = time.time()
				print 'time to complete method3:		', str(t1-t0)
			except Exception, exc:
				print 'method3'
				print exc

				# -- Method 4 -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omega4 = (z-gamma)*method4(len(q),threshold)
				t1 = time.time()
				print 'time to complete method4:		', str(t1-t0)
			except Exception, exc:
				print 'method4'
				print exc

				# -- Method 5 -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omega5 = (z-gamma)*method5(len(q),threshold)
				t1 = time.time()
				print 'time to complete method5:		', str(t1-t0)
			except Exception, exc:
				print 'method5'
				print exc

				# -- Method 6 --  This does method 2 except it parallelizes method 2
				# itself #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omegap = \
				method6(zip(range(1,threshold+1),[len(q)]*len(range(1,threshold+1))))
				omegap = map(itemgetter(-1), omegap)
				omega6 = (z-gamma)*reduce(operator.mul, omegap, 1)
				t1 = time.time()
				print 'time to complete method6:		', str(t1-t0)
			except Exception, exc:
				print 'method6'
				print exc

				# -- Method 7 - This just does method 3 except it parallelizes
				# method 3 itself -- #
			signal.alarm(200)
			try:
				t0 = time.time() #initial time
				omegap = method7(\
				zip(range(1,threshold+1),[len(q)]*len(range(1,threshold+1))))
				omegap = map(itemgetter(-1),omegap)
				omega7 = (z-gamma)*reduce(operator.mul,omegap,1)
				t1 = time.time()
				print 'time to complete method7:		', str(t1-t0)
			except Exception, exc:
				print 'method7'
				print exc

			print 'omega1 - omega2a=		', simplify(omega1-omega2a)
			print 'omega1 - omega3=		', simplify(omega1-omega3)
			print 'omega1 - omega4=		', simplify(omega1-omega4)
			print 'omega1 - omega5=		', simplify(omega1-omega5)
			print 'omega1 - omega6=		', simplify(omega1-omega6)
			print 'omega1 - omega7=		', simplify(omega1-omega7)


def choose_test(test_number):
	global delta
	global q
	if test_number==0:
		delta = [-1/2, 1/2]
		q = [1/4, 1/4]
	
	if test_number==1:
		delta = [-3/4, -1/4, 1/2]
		q = [1/18, 1/18, 1/4]
	
	if test_number==2:
		delta = [-3/4, 0]
		q = [1/18,1/9]
	
	if test_number==3:
		delta = [-3/4,-1/4,1/6,3/4]
		q = [1/18,1/19,1/20,1/30]
	
	if test_number==4:
		delta = [-n/8 for n in xrange(1,8)]
		delta += [n/8 for n in xrange(1,8)]
		q = [1/100] * len(delta)

	return None

phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)
 	# Make this into a list if we use phi_j more than just once.

#First look at the original, straight double loop method
def method1(genus, product_threshold): 
	G = FreeGroup(genus)
	omegap = 1 #Initial choice for omegap, multiply by stuff laters
	for k in range(1,product_threshold+1):
	    W = Words(genus,k) # This is our indexing set, gives all words with alphabet
	                       # 1,2,...,genus of length k
	    for j in xrange(len(W)):
	        #indexlist = [int(nn) for nn in str(W[j])] # Make this list actually an
	                                                  # indexing list
			wordlyfe = G(W[j])# for elements x0,x1,...,xn of the free group
	                                # and if indexlist=[1,2,...,p] (for p<n) this
	                                # gives x0*x1*...*xp for example.
			phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
	                                                # x0 with phi_j(0), (i.e.
	                                                # theta_0). This is now a
	                                                # function of z
			omegap *= (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
	                        z)*(phi_i(z = gamma) - gamma))
	                #This is formula (5.13) in "Computational approach..." - Bobenko
	                #etc. Chap 5
	return omegap

# Next look at the vectorized method without parallelism
def method2(genus, word_length):
	G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = map(lambda x: iterate_words(x,G), W) # I think this is okay. W is an iterable
	# Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output,1)

# Next look at the vectorized method WITH parallelism
def method3(genus, word_length):
	G = FreeGroup(genus)
	W = Words(genus, word_length)
	#output = iterate_words_p(W.list(),G)
	#tuples = zip(W,[G]*len(W))
	output = iterate_words_p(zip(W,[G]*len(W))) # @parallel functions of two
												# variables need to take tuples
    # Would really like to do iterate_words(W) in the above function call,
    # i.e. throw in the generator. However, the parallelizer does not do
    # what we want with that. It wants a list.
	output = map(itemgetter(-1),output)
	return reduce(operator.mul, output,1)

# Next look at a method that "pools" all of the possible words together.
def method4(genus, threshold):
	G = FreeGroup(genus)
	pool = []
	for k in xrange(1,threshold+1): pool += Words(genus,k)
	# Now that we have the pool, i.e. the list of all possible words of length
	# <= threshold, send it to the iterate_words function
	output = map(lambda x: iterate_words(x,G),pool)
	# Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output,1)
	
# Next look at a method that "pools" all of the possible words together, but in
# parallel. This one should speed things up!
def method5(genus, threshold):
	G = FreeGroup(genus)
	pool = []
	for k in xrange(1,threshold+1): pool += Words(genus,k)
	# Now that we have the pool, i.e. the list of all possible words of length
	# <= threshold, send it to the iterate_words function
	output = iterate_words_p(zip(pool,[G]*len(pool)))
	output = map(itemgetter(-1),output)
	return reduce(operator.mul,output,1)

# Test to see if we can make method2 or method3 faster via paralellization of
# the groups
# without parallelism of iterate_words
@parallel
def method6(word_length, genus):
	G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = map(lambda x: iterate_words(x,G),W) # I think this is okay. W is an iterable
    # Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output,1)

# Next look at the vectorized method WITH parallelism
# with parallelism of iterate_words
@parallel
def method7(word_length, genus):
	G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = iterate_words_p(zip(W,[G]*len(W)))
    # Would really like to do iterate_words(W) in the above function call,
    # i.e. throw in the generator. However, the parallelizer does not do
    # what we want with that. It wants a list.
	output = map(itemgetter(-1),output)
	return reduce(operator.mul, output,1)


def iterate_words(w,G):
	genus = len(G.generators())
	wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
	phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
	return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))

@parallel
def iterate_words_p(w,G):
	genus = len(G.generators())
	wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
	phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
	return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))














if __name__ == '__main__':
	main()
