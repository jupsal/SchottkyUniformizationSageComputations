##########################################################################
# This file holds some examples for the forward problem. It is the starting
# place.
#########################################################################

import uniformization
from uniformization.forward_problem import forward_problem
#import forward_problem

plot_circles = True
plot_F = True
prime_function_tests = True
plot_branch_pts = True
slitmap_tests = True
slitmap_full = True
prec = 'double' # inf precision takes just a little bit longer for example 2
example_number = 1 #choose from the examples below.

def main():
    delta, q = define_group_data(example_number)
    branch_pts = forward_problem(delta,q, plot_circles=plot_circles,
    plot_F=plot_F, prime_function_tests=prime_function_tests, 
    plot_branch_pts=plot_branch_pts, product_threshold=3, max_time=200,
    prec = prec, slitmap_full=slitmap_full )
    # right now this fails for product_threshold > 8, for example_num = 2
    print branch_pts


def define_group_data(example_num):
    if example_num == 0: # start with genus 1
        return [0.3], [1./2] # delta, q
        # Right now we need to offset delta, i.e. we can't have delta = 0.
        # Figure this out!
    
    if example_num == 1: # another genus 0, but more interesting
        return [1./2], [1./8] # delta, q
    
    if example_num == 2: #genus 2,
        return [-1./2,1./2], [1./4,1./4] # delta, q


if __name__ == '__main__':
    main()

