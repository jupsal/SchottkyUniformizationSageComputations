###############################################################################
# Now we want to map the circles to a slit map. We use the composed map (5.19)
# to check!

slitmap = (omega(gamma=-1)^2 + omega(gamma=1)^2)/(omega(gamma=-1)^2 -
omega(gamma=1)^2) #(5.19)
## First plot the image of the unit circle.
#slit_plot = parametric_plot( (real_part(slitmap(z = C0)), imag_part(slitmap(z =
#C0))), (t,0,2*pi), color='red', thickness=3)
## This is the right way to do it, the other one is too slow!
slitdataC0 = [CC(slitmap(z=C0(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] # CC
					# turns it from symbolic to complex
					# for plotting!
#D# slitdataCj = lambda k: [CC(slitmap(z=Cj(k)(t=v))) for v in 
#D# srange(0.0,2*pi+0.2,0.1)]
slitdataCj = [ [CC(slitmap(z=Cj(k)(t=v))) for v in srange(0.0,2*pi+0.2,0.1)] for
k in range(genus) ]
slit_plot = line(slitdataC0, rgbcolor=(1,0,0), legend_label='C_0')
slit_plot += sum( [line( slitdataCj[k], rgbcolor = colors[k],
#D#slit_plot += sum( [line( slitdataCj(k), rgbcolor = colors[k],
legend_label='C_'+str(k) ) for k in range(genus)] )

if (show_slit_plot): slit_plot.show(title='slit_plot (5.19)')

if (test_slit_map): attach("test_slitmap.sage")

Cdisp = ComplexField(26) #Displays ~ 6 decimals of precision for output
root_approx = [ (Cdisp(slitmap(z=Cj(k)(t=0))),Cdisp(slitmap(z=Cj(k)(t=pi)))) for
k in range(genus) ]


