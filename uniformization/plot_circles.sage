###############################################################################
# Plots just the circles on the interior of the unit circle.
#
# Dependencies: t, delta, q, genus must be defined.
###############################################################################

# Define the C0, Cj
C0 = exp(I*t)
Cj = lambda j: delta[j] + q[j]*exp(I*t)

# Colors for plotting.
colors = [(0.6*random(),random(),random()) for k in range(genus)] #For plotting,
                          #multiply the first one by 0.6 so nothing is TOO red

# Plot the circles, identifying edges with like colors.
## First plot C_0
D_zeta = line( [CC(C0(t=v)) for v in srange(0,2*pi+0.2,0.1)], linestyle='--',
rgbcolor=(1,0,0), thickness=3, legend_label='C_0' )
## Plot the C_j
D_zeta += sum( [line( [CC(Cj(j)(t=v)) for v in srange(0,2*pi+0.2,0.1)],
rgbcolor=colors[j], thickness=3, legend_label='C_'+str(j+1) ) for j in
range(genus)] )
## Show the graphic
D_zeta.show(axes = True, title='D_zeta')

