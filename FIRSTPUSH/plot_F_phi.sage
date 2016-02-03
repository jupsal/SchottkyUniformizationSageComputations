###############################################################################
# This script plots the fundamental region F by mapping C_j' to C_j by theta. It
# is used as a test.

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
