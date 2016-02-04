###############################################################################
# Builds the Schottky group elements, phi_j, and the prime function using
# "method6" of "test_prime_method"
# 
# Requires: genus, phi, z, delta, q
#
###############################################################################

from operator import itemgetter
import time

# Define phi as a list. A ton of function calls are made to it in iterate_words
# so this should speed things up.
#D#phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z)
phi_j = [ delta[j] + q[j]^2*z/(1-z*delta[j].conjugate()) for j in xrange(genus)
]

@parallel
def build_prime_function(word_length, genus)
	G = FreeGroup(genus)
	W = Words(genus, word_length)
	output = map(lambda x: iterate_words(x,G),W)
	# Now this is a vector, multiply all the elements and return
	return reduce(operator.mul, output, 1)

def iterate_words(w,G):
	wordlyfe = G(w)
	phi_i = 

	return 
	






































G = FreeGroup(genus) #G is a free group on number = genus generators.

time1 = time.time()
#first just get it
omegap = map(updateOmegap,range(1,product_threshold+1))
#Then sum it up
omegap = reduce(operator.mul,omegap,1)
# We could do this all together once things are ready. Like this for now for
# testing
time2 = time.time()
print str(time2-time1)

## Now form the SK prime function,
omega = (z - gamma)*omegap




# This function, "updateOmegap2" should be replaced by something in which I
# generate all possible words, i.e. x0, x1, x0x1,... in one list and then just
# throw that straight into iterate_words

####!! Compare this to the old method which you will have to find on github. This
####!! one appears slow for the weird genus 3 example?

def updateOmegap(word_length):
#Works! Must call "reduce(operator.mul, OUTPUT,1)"
        W = Words(genus, word_length) #Generator of words of length word_length
					#over "genus" elements
        output = iterate_words(W.list())
	# Would really like to do iterate_words(W) in the above function call,
	# i.e. throw in the generator. However, the parallelizer does not do
	# what we want with that. It wants a list.
        output = map(itemgetter(-1),output)
        return reduce(operator.mul, output,1)

@parallel
def iterate_words(w):
        wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
        phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
        return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))


### The above product is OBVIOUSLY very costly. Boooooo

if (prime_function_tests): attach("prime_function_tests.sage")
