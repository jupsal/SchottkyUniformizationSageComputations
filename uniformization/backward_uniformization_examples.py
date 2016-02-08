##########################################################################
# This file holds some examples for the backward problem. It is the starting
# place
#########################################################################

import uniformization
from uniformization.backward_problem import backward_problem

plot_circles = True
plot_F = False
prime_function_tests = False
plot_branch_pts = True

def main():
	branch_pts = define_branch_pts(0)
	backward_problem(branch_pts,

def define_branch_pts(example_num):
	if example_num == 0: # start with genus 1, i.e. 2 branch pts
		return [-1,1]
	if example_num == 1: # the example from "A computational approach..."
		return [-8, -6, -1/2, 1/2, 6, 8]




if __name__ == '__main__':
    main()

