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
#   input:
#       w = a word
#   output:
#       one term in the product of the prime function
#
    gamma = var('gamma')
    z = var('z')
    wordlyfe = GGroup(w) # Get the word in the free group associated with the
                            # right elements
    phi_i = wordlyfe(phi_j) # Turn the free group elements and their composition
                            # into products of the phi_j
    return (phi_i - gamma)*(phi_i(z=gamma)-z)/( (phi_i - z)*(phi_i(z=gamma) -\
                            gamma) )


def test_prime_function(omega, delta, q):
###############################################################################
# Run various tests on the prime function to see that it is calculated well.
# Right now we only have very basic tests. Add more complex ones later?
#
#   input:
#       omega = SK prime function
#       delta = list of center of circles from group data. Numerical or symbolic
#       q = list of radii of circles from group data. Numerical or symbolic
#   output: 
#       a bunch of printed output, returns None
##############################################################################
    z = var('z')
    gamma = var('gamma')
    # Check to see if we are given a symbolic or numeric expression for omega,
    # delta, q
    if type(z)==type(delta[0]):
        input_type = 'symbolic'
    else:
        input_type = 'numeric'
    
    genus = len(q)
    phi_j = [ delta[j] + q[j]**2*z/(1-z*delta[j].conjugate()) for j in
                                 xrange(genus)]
    
    
    print '------------------Prime Function Tests ---------------------'
    ## First, we better have omega(gamma1,gamma2)=0
    test = 'Failed'
    if (simplify( omega(z=gamma) ) == 0): test='Passed' #Check!
    print 'prime function test 1:                       ', test
    
    ## We better also have omega vanishing at the image of gamma under phi_j
    test = 'Failed'
    if sum( [ simplify( omega(z=phi_j[k](z=gamma)) ) for k in range(genus) ]
        )==0:
        test='Passed'  #should=0
    print 'prime function test 2:                       ', test
    
    ######## -- The pole tests can only be completed for numeric delta, q, omega
    if input_type=='numeric':
        ## There should be a pole at the fixed points of phi_j. These are given
        ## analytically by
        pole_pt1 = lambda k: (1+norm(delta[k]) - q[k]**2 + sqrt(-4*norm(delta[k])
            +(1+norm(delta[k]) - q[k]**2)**2))/(2*delta[k].conjugate())
        pole_pt2 = lambda k: (1+norm(delta[k]) - q[k]**2 - sqrt(-4*norm(delta[k])
            +(1+norm(delta[k]) - q[k]**2)**2))/(2*delta[k].conjugate())
        # -- Recall, above, that norm(x+I*y) = x^2 + y^2 in sage
        ## First make sure that these are in fact fixed points of phi_j
        test = 'Failed'
        pole_sum1 = sum( [N( phi_j[k](z=pole_pt1(k)) - pole_pt1(k)) for k in
                                    range(genus)] )
        pole_sum2 = sum( [N( phi_j[k](z=pole_pt2(k)) - pole_pt2(k)) for k in
                                    range(genus)] )
        if abs( pole_sum1 + pole_sum2 ) < exp(-28): test='Passed'
        print 'Pole points verified:                        ', test
        print abs(pole_sum1 + pole_sum2)
        
        ## If we just plug these in we should get an error. To check let's perturb a
        ## little and plug in a particular value of gamma!
        test = 'Failed'
        sum1 = sum( [N( omega(z = pole_pt1(k) + 1e-10, gamma = 1) + omega(z =
            pole_pt2(k) + 1e-10, gamma = 1) ) for k in range(genus)] )
        sum2 = sum( [N( omega(z = pole_pt1(k) + 1e-13, gamma = 1) + omega(z = 
            pole_pt2(k) + 1e-13, gamma = 1) ) for k in range(genus)] )
        sum3 = sum( [N( omega(z = pole_pt1(k) + 1e-15, gamma = 1) + omega(z = 
            pole_pt2(k) + 1e-15, gamma = 1) ) for k in range(genus)] )
        if ( (abs(sum3)>abs(sum2)) and (abs(sum2)>abs(sum1)) ):
            test = 'Passed'
        print 'test3:                                       ', test
        ### Something strange is happening above when product_threshold>8 ish
        
        ### The above sequence should be increasing, check!
        test = 'Failed'
        sum1 = sum( [N( omega(z = pole_pt2(k) + 1e-10, gamma = 1) + omega(z = 
            pole_pt2(k) + 1e-10, gamma = -1) ) for k in range(genus)] )
        sum2 = sum( [N( omega(z = pole_pt2(k) + 1e-13, gamma = 1) + omega(z = 
            pole_pt2(k) + 1e-13, gamma = -1) ) for k in range(genus)] )
        sum3 = sum( [N( omega(z = pole_pt2(k) + 1e-15, gamma = 1) + omega(z = 
            pole_pt2(k) + 1e-15, gamma = -1) ) for k in range(genus)] )
        ### This one too! check!
        if ( (abs(sum3)>abs(sum2)) and (abs(sum2)>abs(sum1)) ):
            test = 'Passed'
        print 'test4:                                       ', test
    
        # We also check to see if (5.17) holds, it doesn't unless we take the
        # infinite
        # product, but should approach it as the product_threshold increases! Again
        # choose a number for gamma
        fiveone7a = omega(z = 1/z.conjugate(), gamma = 1/gamma.conjugate())
        fiveone7 = fiveone7a.conjugate() + omega/(z*gamma)
        fiveone7test = abs(N(fiveone7(z=3+I*3,gamma=1)) )
        print 'test5, (5.17) should be as small as possible:        ', \
                    str(fiveone7test)
        fiveone7testb = abs(N(fiveone7(z=0.7+0.1*I,gamma=1)) )
        print 'test6, (5.17) should be as small as possible:        ', \
        			str(fiveone7testb)
    
    
    # The SK-prime function should also be symmetric in its arguments. I.e. one
    # should have omega(zeta,gamma) = -omega(gamma,zeta). Test this
    # algebraically
    test = 'Failed'
    pvar = var('pvar'); qvar = var('qvar')
    if ( simplify(omega(z=pvar,gamma=qvar)+omega(z=qvar,gamma=pvar)) ) == 0:
        test = 'Passed'
    print 'test7:                                       ', test
    
    print '---------------- End Prime Function Tests --------------------'
