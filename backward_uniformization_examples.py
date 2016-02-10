##########################################################################
# This file holds some examples for the backward problem. It is the starting
# place
#########################################################################

import uniformization
from uniformization.backward_problem import backward_problem

plot_circles = True
plot_F = True
prime_function_tests = True
slitmap_tests = True
slitmap_full = False
plot_branch_pts = True
product_threshold = 2
prec = 'double' #
example_number = 0 # Choose from examples below

def main():
	branch_pts = define_branch_pts(example_number)
	backward_problem(branch_pts, prime_function_tests=prime_function_tests,
                slitmap_tests=slitmap_tests, slitmap_full=slitmap_full,
                plot_circles=plot_circles, plot_F=plot_F,
                plot_branch_pts=plot_branch_pts, prec=prec,
                product_threshold=product_threshold)

def define_branch_pts(example_num):
	if example_num == 0: # start with genus 1, i.e. 2 branch pts
		return [-1,1]
	if example_num == 1: # the example from "A computational approach..."
		return [-8, -6, -1/2, 1/2, 6, 8]


if __name__ == '__main__':
    main()

