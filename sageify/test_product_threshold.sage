###############################################################################

from timeit import time #For timing
Tdisp = RealField(10) #about 2 decimals precision for time display


show_slit_plot = False # Don't let the slitmap.sage file show its image. 
		  # This way we can save in the loop here.
test_slit_map = True

attach("plot_F.sage") #WORKS
D_zeta.save('product_threshold_test-FundamentalDomain.png')
prime_function_tests = True

for product_threshold in range(2,12):
	print "product_threshold:", product_threshold
	time1 = time.time()
	attach("build_prime_function.sage")
	time2 = time.time()
	prime_time = Tdisp(time2-time1)
	time1 = time.time()
	attach("slitmap.sage")
	time2 = time.time()
	slit_time = Tdisp(time2-time1)
	print str(product_threshold)+' & '+str(prime_time)+\
	' & '+str(slit_time)+' & '+str(Tdisp(fiveone7test))+\
	' & '+str(root_approx)+' \\\ \hline'
	slit_plot.save('product_threshold_test1_threshold-'+str(product_threshold)+'.png')

