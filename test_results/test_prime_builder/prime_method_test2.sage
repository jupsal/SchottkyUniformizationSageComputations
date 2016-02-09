###############################################################################
# This file tests different methods for calculating the prime function from
# group data. It compares speed and accuracy.

###
# Only test methods6 and 7,  use all test_nums and all the product_thresholds
from operator import itemgetter
import time
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

#methods = {'method1': method1, 'method2': method2, 'method3': method3,
#'method4': method4, 'method5': method5, 'method6': method6, 'method7': method7}
# now if we add a new method just add it to the dictionary, or, if we decide a
# method is bad take it out!

def main():
#	global omega1, omega6, omega7
	global G, genus

	for test_num in xrange(5):
		choose_test(test_num)
		print 'Using test \# '+str(test_num)+' .........'
		for threshold in xrange(3,11):
			print 'product_threshold = ', str(threshold)

			# -- Method 1 -- # # for comparison -- NOPE. I am convinced this
			# other method is fine. This one just slows things down too much.
		#	signal.signal(signal.SIGALRM,handler)
		#	signal.alarm(300)
		#	try:
		#		t0 = time.time() #initial time
		#		omega1 = (z-gamma)*method1(len(q),threshold)
		#		t1 = time.time()
		#		print 'time to complete method1:        ', str(t1-t0)
		#	except Exception, exc:
		#		print 'method1'
		#		print exc

			genus = len(q)
			G = FreeGroup(genus)
				# -- Method 6 --  This badboy speaks for herself.
			signal.signal(signal.SIGALRM,handler)
			signal.alarm(300)
			try:
				t0 = time.time() #initial time
				#omegap = \
				#method6(zip(range(1,threshold+1),[len(q)]*len(range(1,threshold+1))))
				omegap = method6(range(1,threshold+1))
				omegap = map(itemgetter(-1), omegap)
				omega6 = (z-gamma)*reduce(operator.mul, omegap, 1)
				t1 = time.time()
				print 'time to complete method6:		', str(t1-t0)
			except Exception, exc:
				print 'method6'
				print exc

				# -- Method 7 - New guy on the block.
			signal.signal(signal.SIGALRM,handler)
			signal.alarm(300)
			try:
				t0 = time.time() #initial time
				#omegap = \
				#method7(zip(range(1,threshold+1),[len(q)]*len(range(1,threshold+1))))
				omegap = method7(range(1,threshold+1))
				omegap = map(itemgetter(-1), omegap)
				omega7 = (z-gamma)*reduce(operator.mul, omegap, 1)
				t1 = time.time()
				print 'time to complete method7:		', str(t1-t0)
			except Exception, exc:
				print 'method7'
				print exc

		#	print 'omega1 - omega2a=		', simplify(omega1-omega2a)
			#print 'omega1 - omega3=		', simplify(omega1-omega3)
			#print 'omega1 - omega4=		', simplify(omega1-omega4)
			#print 'omega1 - omega5=		', simplify(omega1-omega5)
			#print 'omega1 - omega6=		', simplify(omega1-omega6)
			#print 'omega1 - omega7=		', simplify(omega1-omega7)


def choose_test(test_number):
	global delta
	global q
	global phi_j2
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

	phi_j2 = [ delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) for j in
		xrange(len(q)) ]
	return None

#phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)
    # Make this into a list if we use phi_j more than just once.

#First look at the original, straight double loop method
#def method1(genus, product_threshold):
#	G22 = FreeGroup(genus)
#	omegap22 = 1
#	for k in range(1,product_threshold+1):
#		W22 = Words(genus,k) 
#		for j in xrange(len(W22)):
#			wordlyfe22 = G22(W22[j])
			#phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we
#			phi_i = wordlyfe22([phi_j2[nn] for nn in range(genus)]) #
#			omegap *= (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
#					z)*(phi_i(z = gamma) - gamma))
#	omegap22 = 4+5+9+3
#	return omegap22



# The big difference with this new method6 is in iterate_words. (a) we don't
# need genus. (b) instead of looping the phi_i and calculating each time we do
# it once then apply wordlyfe to the list directly.

@parallel
#def method6(word_length, genus):
def method6(word_length):
	#G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = map(iterate_words,W)
#map(lambda x: iterate_words(x,G),W) # I think this is okay. W is an iterable
    # Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output,1)

# The big difference between this method and the method6 above is in
# iterate_words as well. Here we call iterate words with the whole Words group
# instead of with each element at a time. We then map G onto the words group
# giving a list of words. We then have to define the group element as a list
# where each word is replaced with the correct group element, again from the
# precreated list. We again return a list then multiply out l8ers.

@parallel
def method7(word_length):
	#G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = iterate_words2(W)
	#output = map(lambda x: iterate_words(x,G),W) # I think this is okay. W is an iterable
    # Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output,1)


def iterate_words(w):
	wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
	phi_i = wordlyfe(phi_j2) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
	return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))

def iterate_words2(W):
	wordlyfe = map(G,W) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
	phi_i = [ word(phi_j2) for word in wordlyfe ] # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
	return [ (phi-gamma)*(phi(z=gamma)-z)/( (phi - z)*(phi(z=gamma)-gamma) ) for
phi in phi_i ]

#def iterate_words(w,G):
#	genus = len(G.generators())
#	wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
#                                # and if indexlist=[1,2,...,p] (for p<n) this
#                                # gives x0*x1*...*xp for example.
#	phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
#                                                # x0 with phi_j(0), (i.e.
#                                                # theta_0). This is now a
#                                                # function of z
#	return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
#                        z)*(phi_i(z = gamma) - gamma))
#
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
