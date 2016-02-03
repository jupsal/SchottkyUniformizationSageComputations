###############################################################################
# This sagefile uses user specified group-data (circles in the complex plane)
# and produces a hyperelliptic curve as well as some plots for verification.
###############################################################################


# Preamble, this should not be touched for different R.S.
x,y = var('x,y')
assume(x,'real'); assume(y,'real')
zeta = x+I*y #local variable
t = var('t') # for parametric plotting
z = var('z') # complex variable not specified by x,y

# On-off switches for variable functionality
product_threshold_test = True # For testing convergence as a function of
				# the parameter product_threshold
genus_test = False # For testing this program under a change of genus
hyperbolic_test = False # For testing this program under a change that may
			# POSSIBLY make the surface non-hyperbolic, not sure
			# yet though how this works
full_diagnostic = False # This is the very slow method. Includes:
			# (a) Doing each mapping in (5.18) individually.
			# (b) ...


# Group data and stuff to be changed for different R.S.
delta = [-1/2,1/2] #Center of circle C_j
q = [1/4, 1/4] #radius of circule C_j
genus = len(q) #genus of surface.
colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
			  #multiply the first one by 0.6 so nothing is TOO red
product_threshold = 2 #the threshold for the finite product to define SK prime function
xplot_range = 4.5 #to plot for x \in [-xplot_range,xplot_range]
yplot_range = 2 #to plot for y \in [-yplot_range,yplot_range]

# Define our circles.
C0 = exp(I*t) #Unit circle.
Cj = lambda j: delta[j] + q[j]*exp(I*t) #circles within the unit circle
Cjp = lambda j: 1/(Cj(j).conjugate()) #Reflection of Cj about the unit circle.
## Define circles for filling regions D_zeta and D_zeta' as well.
C0_fill = abs(zeta)^2-1
Cj_fill = lambda j: abs(zeta-delta[j])^2 - q[j]^2
Cjp_fill = lambda j: abs(1/zeta.conjugate()-delta[j])^2 - q[j]^2

# Plot the circles, identifying edges with like colors.
## First plot C_0
D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
## Plot the C_j
D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
range(genus)] )
## Plot the C_j'
D_zeta += sum( [line( [CC(Cjp(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3 ) for j in range(genus)] )
## Fill the two regions, D_\zeta and D_zeta'
D_zeta += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill(k))>0 for k in
range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
incol='red', borderwidth=0, alpha=0.2 )
D_zeta += region_plot([real_part(C0_fill)>0]+[real_part(Cjp_fill(k))>0 for k in
range(0,genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
incol='blue', borderwidth=0, alpha=0.2 )
## Show the graphic
D_zeta.show(axes = True, title='D_zeta')

# Define the "theta_j" function as in "Computational approach..." We will call
# it phi_j to eliminate confusion with the R. Theta function.
phi_j = lambda j: delta[j] + q[j]^2*z/(1-delta[j].conjugate()*z) #phi_j(z)

########## We only do this in genus/hyperbolic test mode! See above

# Check to see that in fact the image of Cjp under phi_j is Cj
## Plot C0
D_zeta_check = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)],
linestyle='--', rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
## Plot Cjp
D_zeta_check += sum( [line( [CC(Cjp(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
range(genus)] )
## Plot the image of Cjp under phi
D_zeta_check += sum( [line( [CC(phi_j(j)(z=Cjp(j)(t=v))) for v in
srange(0,2*pi+0.2,0.1)], rgbcolor=colors[j], thickness=3 ) for j in
range(genus)] )
## Fill in the regions as before
D_zeta_check += region_plot( [real_part(C0_fill)<0]+[real_part(Cj_fill(k))>0 for
k in range(genus)], (x,-xplot_range,xplot_range), (y,-yplot_range,yplot_range),
incol='red', borderwidth=0, alpha=0.2 )
D_zeta_check += region_plot( [real_part(C0_fill)>0]+[real_part(Cjp_fill(k))>0
for k in range(genus)], (x,-xplot_range,xplot_range),
(y,-yplot_range,yplot_range), incol='blue', borderwidth=0, alpha=0.2 )

D_zeta_check.show(axes = True, title='D_zeta_check')

# Define gamma to be a variable which we will choose later for the prime
# function omega(z,gamma)
gamma = var('gamma') #base point for 'abelmap'

# Use the infinite product formula (5.13) to define omegap (= omega')
G = FreeGroup(genus) #G is a free group on number = genus generators.
omegap = 1 #Initial choice for omegap, multiply by stuff laters
for k in range(1,product_threshold+1):
    W = Words(genus,k) # This is our indexing set, gives all words with alphabet
		       # 1,2,...,genus of length k
    for j in range(len(W.list())):
        indexlist = [int(nn) for nn in str(W[j])] # Make this list actually an
						  # indexing list
        wordlyfe = G(indexlist) # for elements x0,x1,...,xn of the free group
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

## Now form the SK prime function,
omega = (z - gamma)*omegap
### The above product is OBVIOUSLY very costly. Boooooo
 
# Do some quick checks on the prime function...
## First, we better have omega(gamma1,gamma2)=0
simplify( omega(z=gamma) ) #Check!
## We better also have omega vanishing at the image of gamma under phi_j
sum( [simplify( omega(z=phi_j(k)(z=gamma)) ) for k in range(genus)] ) #should=0
## There should be a pole at the fixed points of phi_j. These are given
## analytically by
pole_pt1 = lambda k: (1+abs(delta[k])^2 - q[k]^2 + sqrt(-4*abs(delta[k])^2 +
(1+abs(delta[k])^2 - q[k]^2)^2))/(2*delta[k].conjugate())
pole_pt2 = lambda k: (1+abs(delta[k])^2 - q[k]^2 - sqrt(-4*abs(delta[k])^2 +
(1+abs(delta[k])^2 - q[k]^2)^2))/(2*delta[k].conjugate())
## First make sure that these are in fact fixed points of phi_j
sum( [N( phi_j(k)(z=pole_pt1(k)) - pole_pt1(k)) for k in range(genus)] )
sum( [N( phi_j(k)(z=pole_pt2(k)) - pole_pt2(k)) for k in range(genus)] )


## If we just plug these in we should get an error. To check let's perturb a
## little and plug in a particular value of gamma!
sum( [N( omega(z = pole_pt1(k) + 1e-10, gamma = 1) + omega(z = pole_pt2(k) +
1e-10, gamma = 1) ) for k in range(genus)] )
sum( [N( omega(z = pole_pt1(k) + 1e-13, gamma = 1) + omega(z = pole_pt2(k) +
1e-13, gamma = 1) ) for k in range(genus)] )
sum( [N( omega(z = pole_pt1(k) + 1e-15, gamma = 1) + omega(z = pole_pt2(k) +
1e-15, gamma = 1) ) for k in range(genus)] )
### The above sequence should be increasing, check!
sum( [N( omega(z = pole_pt1(k) + 1e-10, gamma = 1) + omega(z = pole_pt2(k) +
1e-10, gamma = -1) ) for k in range(genus)] )
sum( [N( omega(z = pole_pt1(k) + 1e-13, gamma = 1) + omega(z = pole_pt2(k) +
1e-13, gamma = -1) ) for k in range(genus)] )
sum( [N( omega(z = pole_pt1(k) + 1e-15, gamma = 1) + omega(z = pole_pt2(k) +
1e-15, gamma = -1) ) for k in range(genus)] )
### This one too! check!

# We also check to see if (5.17) holds, it doesn't unless we take the infinite
# product, but should approach it as the product_threshold increases! Again
# choose a number for gamma
fiveone7 = omega( z = 1/z, gamma=1/gamma).conjugate() + 1/(gamma*z)*omega
N( fiveone7(z=3+I*3,gamma=1) ) #Not that small!

# Before going straight to (5.19), plot zeta_1, zeta_2, z (5.18) to maybe give
# an idea of which step is the least accurate

# Now plot these, start with zeta1
zeta1 = -omega(gamma=1)/omega(gamma=-1)
zeta1dataC0 = [CC(zeta1(z=C0(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] #CC turns
				      #it from symbolic to complex for plotting!
#zeta1dataCj = lambda k: [CC(zeta1(z=Cj(k)(t=v))) for v in
#srange(0.0,2*pi+0.2,0.1)]
zeta1dataCj = [ [CC(zeta1(z=Cj(k)(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] for
k in range(genus) ] #Produces something such that zeta1dataCj[k] gives the image
		#of C_k under zeta1 as a long list with (2*pi+0.2)/0.1 elements.
zeta1plot = line(zeta1dataC0, rgbcolor=(1,0,0), legend_label='C_0')
#zeta1plot += sum( [line( zeta1dataCj(k), rgbcolor = colors[k],
zeta1plot += sum( [line( zeta1dataCj[k], rgbcolor = colors[k],
legend_label='C_'+str(k+1) ) for k in range(genus)] )
zeta1plot.show(title='zeta1plot')
# The above method works way better!

## If we want to examine the image of each circle more, plot one at a time:
for k in range(genus):
	analyze_plot = line(zeta1dataCj[k], rgbcolor=colors[k],
		legend_label='C_'+str(k+1))
	analyze_plot.show(title='Image of C_'+str(k+1)+' under zeta_1')


# Now do it for zeta2
#D# The code deprecated in this section was removed because of how slow it was
#D# going. The choice to use function calls to build the zeta2 data uses less
#D# memory and might be useful if we only need ONE of these maps but if we use
#D# them all it's not worth it. The following notes hold about the old method:
#D# (a) it does not scale with product_threshold. (b) it DOES scale with genus,
#D# so that sucks (c) in practice this step would be skipped, it's only for 
#D# diagnostics. It is worth it to save the memory in this case since we may be
#D# running large test suites on this.

zeta2dataC0 = [ (1-zeta1dataC0[k])/(1+zeta1dataC0[k]) for k in
range(len(zeta1dataC0)) ]
#D#zeta2dataCj = lambda k: [ (1-zeta1dataCj(k)[j])/(1+zeta1dataCj(k)[j]) for j in
#D#range(len(zeta1dataCj(k))) ] 
zeta2dataCj = [ [(1-zeta1dataCj[k][j])/(1+zeta1dataCj[k][j]) for j in
range(len(zeta1dataCj[k])) ] for k in range(genus) ]
zeta2plot = line(zeta2dataC0, rgbcolor=(1,0,0), legend_label='C_0')
#D#zeta2plot += sum( [line( zeta2dataCj(k), rgbcolor = colors[k],
#D#legend_label='C_'+str(k+1) ) for k in range(genus)] )
zeta2plot += sum( [line( zeta2dataCj[k], rgbcolor = colors[k],
legend_label='C_'+str(k+1) ) for k in range(genus)] )
zeta2plot.show(title='zeta2plot')

# Now do it for zed (the last eqn in (5.18))
zeddataC0 = [ 0.5*(1/zeta2dataC0[k] + zeta2dataC0[k]) for k in
range(len(zeta2dataC0)) ]
zeddataCj = [ [ 0.5*(1/zeta2dataCj[k][j] + zeta2dataCj[k][j]) for j in
range(len(zeta2dataCj[k])) ] for k in range(genus) ]
#D#zeddataCj = lambda k: [ 0.5*(1/zeta2dataCj(k)[j] + zeta2dataCj(k)[j]) for j in
#D#range(len(zeta2dataCj(k))) ]
zedplot = line(zeddataC0, rgbcolor=(1,0,0), legend_label='C_0')
#D#zedplot += sum( [line( zeddataCj[k], rgbcolor = colors[k],
#D#legend_label='C_'+str(k+1) ) for k in range(genus)] )
zedplot += sum( [line( zeddataCj[k], rgbcolor = colors[k],
legend_label='C_'+str(k+1) ) for k in range(genus)] )
zedplot.show(title='zedplot')

# Now we want to map the circles to a slit map. We use the composed map (5.19)
# to check!
slitmap = (omega(gamma=-1)^2 + omega(gamma=1)^2)/(omega(gamma=-1)^2 -
omega(gamma=1)^2) #(5.19)
## First plot the image of the unit circle.
#slit_plot = parametric_plot( (real_part(slitmap(z = C0)), imag_part(slitmap(z =
#C0))), (t,0,2*pi), color='red', thickness=3)
## This is the right way to do it, the other one is too slow!
slitdataC0 = [CC(slitmap(z=C0(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] #CC turns it
					#from symbolic to complex for plotting!
#D# slitdataCj = lambda k: [CC(slitmap(z=Cj(k)(t=v))) for v in 
#D# srange(0.0,2*pi+0.2,0.1)]
slitdataCj = [ [CC(slitmap(z=Cj(k)(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] for
k in range(genus) ]
slit_plot = line(slitdataC0, rgbcolor=(1,0,0), legend_label='C_0')
slit_plot += sum( [line( slitdataCj[k], rgbcolor = colors[k],
#D#slit_plot += sum( [line( slitdataCj(k), rgbcolor = colors[k],
legend_label='C_'+str(k) ) for k in range(genus)] )

slit_plot.show(title='slit_plot (5.19)')






