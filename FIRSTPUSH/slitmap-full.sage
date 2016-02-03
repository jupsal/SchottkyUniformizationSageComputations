##############################################################################
# This does the full slit map, step by step. For diagnostics.
#############################################################################

tstep = 0.01 #step for parametric plotting, smaller is finer.

# Now plot these, start with zeta1
zeta1 = -omega(gamma=1)/omega(gamma=-1)
zeta1dataC0 = [CC(zeta1(z=C0(t=v))) for v in srange(0.0,2*pi+2*tstep,tstep)] #CC turns
                                      #it from symbolic to complex for plotting!
#zeta1dataCj = lambda k: [CC(zeta1(z=Cj(k)(t=v))) for v in
#srange(0.0,2*pi+0.2,0.1)]
zeta1dataCj = [ [CC(zeta1(z=Cj(k)(t=v))) for v in srange(0.0,2*pi+2*tstep,tstep)] for
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
#D#zeta2dataCj = lambda k: [ (1-zeta1dataCj(k)[j])/(1+zeta1dataCj(k)[j]) for j 
#D# in range(len(zeta1dataCj(k))) ] 
zeta2dataCj = [ [(1-zeta1dataCj[k][j])/(1+zeta1dataCj[k][j]) for j in
range(len(zeta1dataCj[k])) ] for k in range(genus) ]
zeta2plot = line(zeta2dataC0, rgbcolor=(1,0,0), legend_label='C_0')
#D#zeta2plot += sum( [line( zeta2dataCj(k), rgbcolor = colors[k],
#D#legend_label='C_'+str(k+1) ) for k in range(genus)] )
zeta2plot += sum( [line( zeta2dataCj[k], rgbcolor = colors[k],
legend_label='C_'+str(k+1) ) for k in range(genus)] )
zeta2plot.show(title='zeta2plot', aspect_ratio = 1)

# Now do it for zed (the last eqn in (5.18))
zeddataC0 = [ 0.5*(1/zeta2dataC0[k] + zeta2dataC0[k]) for k in
range(len(zeta2dataC0)) ]
zeddataCj = [ [ 0.5*(1/zeta2dataCj[k][j] + zeta2dataCj[k][j]) for j in
range(len(zeta2dataCj[k])) ] for k in range(genus) ]
#D#zeddataCj = lambda k: [ 0.5*(1/zeta2dataCj(k)[j] + zeta2dataCj(k)[j]) for j
#D# in range(len(zeta2dataCj(k))) ]
zedplot = line(zeddataC0, rgbcolor=(1,0,0), legend_label='C_0')
zedplot.show(title='zedplot C_0')
#D#zedplot += sum( [line( zeddataCj[k], rgbcolor = colors[k],
#D#legend_label='C_'+str(k+1) ) for k in range(genus)] )
zedplot += sum( [line( zeddataCj[k], rgbcolor = colors[k],
legend_label='C_'+str(k+1) ) for k in range(genus)] )
zedplot.show(title='zedplot')
