###############################################################################
# This file should hold all of the stuff to do the forward problem, i.e. from
# group data construct branch places and hence the algebraic curve.
###############################################################################

# Group data and stuff to be changed for different R.S.
delta = [-1/2,1/2] #Center of circle C_j
q = [1/4, 1/4] #radius of circule C_j
genus = len(q) #genus of surface.
product_threshold = 2 #the threshold for the finite product to define SK prime
			#function

# Weird genus 3 example
delta = [-3/4, -1/4, 1/2]
q = [1/18,1/18,1/4]

# Define our circles.
C0 = exp(I*t) #Unit circle.
Cj = lambda j: delta[j] + q[j]*exp(I*t) #circles within the unit circle
Cjp = lambda j: 1/(Cj(j).conjugate()) #Reflection of Cj about the unit circle.
## Define circles for filling regions D_zeta and D_zeta' as well.
C0_fill = abs(zeta)^2-1
Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2

# Define the "theta_j" function as in "Computational approach..." We will call
# it phi_j to eliminate confusion with the R. Theta function. This specifies the
# Schottky group.
phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)


#True/falses

#Tests:
test_product_threshold = False # For testing convergence as a function of
                                # the parameter product_threshold
test_product_threshold_single = False # For testing with one value of
				#product_threshold


if(test_product_threshold):
	attach("test_product_threshold.sage") # Nice! It has access to the
					      # variables in this script!

if(test_product_threshold_single):
	attach("test_product_threshold_single.sage") 



