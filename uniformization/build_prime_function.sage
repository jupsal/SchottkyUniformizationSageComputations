###############################################################################
# Builds the Schottky group elements, phi_j, and the prime function using
# "method6" of "test_prime_method2"
# 
# Requires: genus, phi, z, delta, q, gamma, G, product_threshold
#
###############################################################################

# Define phi as a list. A ton of function calls are made to it in iterate_words
# so this should speed things up.
#D#phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z)
phi_j = [ delta[j] + q[j]^2*z/(1-z*delta[j].conjugate()) for j in xrange(genus)
]

# Build_omegap below is a parallel function. It must be called as such, i.e. it must be called with a list input. 
# e.g. omegap = build_prime_function(range(1,threshold+1)) #- Gives a list of generators
# omegap = map(itemgetter(-1), omegap) #- need to grab the last element of the list for each generator
# omega = (z-gamma)*reduce(operator.mul, omegap, 1) #- omegap is a list of functions found from the different word lengths. We need to multiply all of these together.


# Define the main workhorse functions.

@parallel
def build_omegap(word_length)
	W = Words(genus, word_length) # Get all words of word_length over genus elements
	output = map(iterate_words,W) # Map the function iterate_words below onto W. The output is a list, multiply all of the elements associated with different WORDS then return.
	return reduce(operator.mul, output, 1)
	
def iterate_words(w):
	wordlyfe = G(w) #Get the word in the free group associated with the right elements
	phi_i = wordlyfe(phi_j) #Turn the free group elements and their composition into products of the phi_j
	

# Now actually build omega from omegap. 
def build_prime_function(product_threshold):
	omegap = build_omegap(range(1,product_threshold))
	omegap = map(itemgetter(-1), omegap)
	return (z-gamma)*reduce(operator.mul, omegap, 1)

