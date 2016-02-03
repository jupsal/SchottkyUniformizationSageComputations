###############################################################################

from timeit import time #For timing
Tdisp = RealField(10) #about 2 decimals precision for time display

product_threshold = 3 #for this particular choice of product_threshold

show_slit_plot = True 
test_slit_map = True

attach("plot_F.sage") #WORKS
prime_function_tests = True

attach("build_prime_function.sage")
attach("slitmap-full.sage")
attach("slitmap.sage")
