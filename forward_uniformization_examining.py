###############################################################################
# This file holds some examples for examining the forward problem, i.e. by
# plotting some Points or lines or both and looking at their image under the
# slitmap
###############################################################################

import numpy as np
from warnings import warn
import uniformization
from uniformization.forward_problem import forward_problem_on_Points_and_Lines
from sage.all import *
#import forward_problem

plot_circles = True
plot_F = True
prime_function_tests = False
slitmap_tests = False
slitmap_full = True
slitmap_direct = False
prec = 'double' # inf precision takes just a little bit longer for example 2
group_example_number = 1 #choose from the examples below.
line_example_number = 2
save_plots = True # Save plots or not?

def main():
    delta, q = define_group_data(group_example_number)


    Points, Lines = place_lines_and_points(line_example_number)
        # Use capitals to avoid the weirdly used Points==point
                            # in sage
        # use capital L to be consistent with Points
    
    forward_problem_on_Points_and_Lines(
        delta, q, Points, Lines, plot_circles=True, plot_F=plot_F,
        slitmap_full=slitmap_full, slitmap_direct=slitmap_direct, prec=prec, 
        product_threshold=3, max_time=200, 
        prime_function_tests=prime_function_tests, slitmap_tests=slitmap_tests,
        save_plots=save_plots
        )

    return None


def define_group_data(example_num):
    if example_num == 0: # start with genus 1
        return [0.3], [1./2] # delta, q
        # Right now we need to offset delta, i.e. we can't have delta = 0.
        # Figure this out!
    
    if example_num == 1: # another genus 0, but more interesting
        return [1./2], [1./8] # delta, q
    
    if example_num == 2: #genus 2,
        return [-1./2,1./2], [1./4,1./4] # delta, q


def place_lines_and_points(example_num):
    if example_num == 0:

       POINT = [I/3, -I/3]
       LINE = [
                define_line(-1./4+1./2*I, 1./4+1./2*I), 
                define_line(-1./4-1./4*I, 1./4+1./2*I),
                define_line(-1./4-1./4*I, -1./4+1./2*I)
                ]          


    if example_num == 1:
        sqrt2 = 2**(-.5) 
        #POINT = [I, -I, 1, -1] # Can't do these, these are poles of the slitmap!
        POINT = [ exp(I*(pi/2-0.1)), exp(I*(-pi/2-0.1)), exp(I*(2*pi-0.1)),
                exp(I*(pi-0.1)) ] 
        POINT += [ exp(I*(pi/2+0.1)), exp(I*(-pi/2+0.1)), exp(I*(2*pi+0.1)),
                exp(I*(pi+0.1)) ] 
        POINT += [0]
        LINE = [
                define_line(-sqrt2 - I*sqrt2, sqrt2 + I*sqrt2),
                    # this line goes all the way across the circle
                define_line(-sqrt2 + I*sqrt2, sqrt2 - I*sqrt2)
                    # this line goes all the way across the circle
                                                  # circle
                ]          
    if example_num == 2:
        POINT = [-3, 2-0.5*I, 0, 3*I]
        #POINT = [2] #Gives a divide by zero error? for product_threshold=2 so I
        #imagine it does it for others?
        LINE =  [
                define_line(-2 + 1.2*I, 2+1.2*I), # this line is outside of the
                                                  # circle
                define_line(-3 - 1.2*I, 3-1.2*I), # this line is outside of the
                                                  # circle
                define_line(-1.2 - 2*I, -1.2+2*I), # this line is outside of the
                                                  # circle
                define_line(1.2 - 3*I, 1.2+3*I), # this line is outside of the
                ]
        
    return POINT, LINE


def define_line(x0, x1, field=CDF, mesh=1000):
    # 
    # Defines a line from x0 to x1 as a collection of Points.
    #
    # input:
    #   x0 = starting point
    #   x1 = ending point
    #   field = underlying field. CDF by default but CC is also allowed.
    #   mesh = how coarse?, use np.linspace(0,1,mesh)
    #
    # output:
    #   line = collection of Points
    #
    if (field != CDF and field != CC):
        warn("Using a field different from CDF or CC will result in issues "
                "with plotting these lines. Proceed with caution.",
                RuntimeWarning)

    line = [ field(x0 + t*(x1-x0)) for t in np.linspace(0,1,mesh) ]
    return line


if __name__ == '__main__':
    main()

