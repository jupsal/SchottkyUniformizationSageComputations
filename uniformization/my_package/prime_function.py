###############################################################################
# Defines functions for building and testing the prime function.
###############################################################################

from sage.all import *
# this also imports operator.mul and operator.itemgetter


def build_prime_function(delta, q, product_threshold):
	# input:
	#	delta = center points of circles (list)
	# 	q = radii of circles (list)
	# 	product_threshold = max number of terms used in product
	#
	# output:
	#	the prime function

	global genus # make global so we don't have to pass to helper funcs
	global phi_j # ""
	global GGroup # this one makes sense. You don't want to call it a bunch in
					# the parallel thang

	z = var('z')
	gamma = var('gamma')
	genus = len(q)
	GGroup = FreeGroup(genus)
	# Define phi as a list. A ton of function calls are made to it in
	# iterate_words
	# so this should speed things up.
	phi_j = [ delta[j] + q[j]**2*z/(1-z*delta[j].conjugate()) for j in
			xrange(genus)]

	omegap = build_omegap(range(1,product_threshold))
	omegap = map(operator.itemgetter(-1), omegap)
	return (z-gamma)*reduce(operator.mul, omegap, 1)

# Helper function for build_prime_function
@parallel
def build_omegap(word_length):

	gamma = var('gamma')
	z = var('z')
	W = Words(genus, word_length) # Get all words of word_length over genus
									# elements
	output = map(iterate_words,W) # Map the function iterate_words below onto W.
								# The output is a list, multiply all of the
								# elements associated with different WORDS
								# then return
	return reduce(operator.mul, output, 1)

# This is the workhorse helper function
def iterate_words(w):

	gamma = var('gamma')
	z = var('z')
	wordlyfe = GGroup(w) # Get the word in the free group associated with the
					# right elements
	phi_i = wordlyfe(phi_j) # Turn the free group elements and their composition
							# into products of the phi_j
	return (phi_i - gamma)*(phi_i(z=gamma)-z)/( (phi_i - z)*(phi_i(z=gamma) -\
				gamma) )
