###############################################################################
# Builds the prime function. 

from operator import itemgetter
import time

prime_function_tests = False #Don't test for now.

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
