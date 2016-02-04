###############################################################################
# Run various tests on the prime function to see that it is calculated well.
# Right now we only have very basic tests. Add more complex ones later?
#
# requires: omega, gamma, z, phi_j, q, delta, 
##############################################################################

print '------------------Prime Function Tests ---------------------'
## First, we better have omega(gamma1,gamma2)=0
test = 'Failed'
if (simplify( omega(z=gamma) ) == 0): test='Passed' #Check!
print 'prime function test 1:			', test

## We better also have omega vanishing at the image of gamma under phi_j
test = 'Failed'
if (sum( [simplify( omega(z=phi_j[k](z=gamma)) ) for k in range(genus)] )==0):
	test='Passed'  #should=0
print 'prime function test 2:			', test

## There should be a pole at the fixed points of phi_j. These are given
## analytically by
pole_pt1 = lambda k: (1+abs(delta[k])^2 - q[k]^2 + sqrt(-4*abs(delta[k])^2 +
(1+abs(delta[k])^2 - q[k]^2)^2))/(2*delta[k].conjugate())
pole_pt2 = lambda k: (1+abs(delta[k])^2 - q[k]^2 - sqrt(-4*abs(delta[k])^2 +
(1+abs(delta[k])^2 - q[k]^2)^2))/(2*delta[k].conjugate())
## First make sure that these are in fact fixed points of phi_j
test = 'Failed'
pole_sum1 = sum( [N( phi_j[k](z=pole_pt1(k)) - pole_pt1(k)) for k in range(genus)] )
pole_sum2 = sum( [N( phi_j[k](z=pole_pt2(k)) - pole_pt2(k)) for k in range(genus)] )
if abs( pole_sum1 + pole_sum2 ) < exp(-28): test='Passed'
print 'Pole points verified:			', test

## If we just plug these in we should get an error. To check let's perturb a
## little and plug in a particular value of gamma!
test = 'Failed'
sum1 = sum( [N( omega(z = pole_pt1(k) + 1e-10, gamma = 1) + omega(z =
pole_pt2(k) + 1e-10, gamma = 1) ) for k in range(genus)] )
sum2 = sum( [N( omega(z = pole_pt1(k) + 1e-13, gamma = 1) + omega(z = 
pole_pt2(k) + 1e-13, gamma = 1) ) for k in range(genus)] )
sum3 = sum( [N( omega(z = pole_pt1(k) + 1e-15, gamma = 1) + omega(z = 
pole_pt2(k) + 1e-15, gamma = 1) ) for k in range(genus)] )
if ( (abs(sum3)>abs(sum2))&(abs(sum2)>abs(sum1)) ): test = 'Passed'
print 'test3:					', test

### The above sequence should be increasing, check!
test = 'Failed'
sum1 = sum( [N( omega(z = pole_pt1(k) + 1e-10, gamma = 1) + omega(z = 
pole_pt2(k) + 1e-10, gamma = -1) ) for k in range(genus)] )
sum2 = sum( [N( omega(z = pole_pt1(k) + 1e-13, gamma = 1) + omega(z = 
pole_pt2(k) + 1e-13, gamma = -1) ) for k in range(genus)] )
sum3 = sum( [N( omega(z = pole_pt1(k) + 1e-15, gamma = 1) + omega(z = 
pole_pt2(k) + 1e-15, gamma = -1) ) for k in range(genus)] )
### This one too! check!
if ( (abs(sum3)>abs(sum2))&(abs(sum2)>abs(sum1)) ): test = 'Passed'
print 'test4:					', test

# We also check to see if (5.17) holds, it doesn't unless we take the infinite
# product, but should approach it as the product_threshold increases! Again
# choose a number for gamma
fiveone7a = omega(z = 1/z.conjugate(), gamma = 1/gamma.conjugate())
fiveone7 = fiveone7a.conjugate() + omega/(z*gamma)
#fiveone7 = omega( z = 1/z.conjugate(), gamma=1/gamma.conjugate()).conjugate() + 1/(gamma*z)*omega
fiveone7test = abs(N(fiveone7(z=3+I*3,gamma=1)) )
print 'test5, (5.17) should be as small as possible:	', str(fiveone7test)
fiveone7testb = abs(N(fiveone7(z=0.7+0.1*I,gamma=1)) )
print 'test6, (5.17) should be as small as possible:	', str(fiveone7testb)


# The SK-prime function should also be symmetric in its arguments. I.e. one
# should have omega(zeta,gamma) = -omega(gamma,zeta). Test this algebraically
test = 'Failed'
pvar = var('pvar'); qvar = var('qvar')
if ( simplify(omega(z=pvar,gamma=qvar)+omega(z=qvar,gamma=pvar)) ) == 0:
	test = 'Passed'
print 'test7:					', test



print '---------------- End Prime Function Tests --------------------'
