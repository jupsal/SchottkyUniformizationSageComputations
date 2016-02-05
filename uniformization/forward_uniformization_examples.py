##########################################################################
# This file holds some examples for the forward problem. It is the starting
# place.
#########################################################################

import uniformization
from uniformization.forward_problem import forward_problem
#import forward_problem

plot_circles = True
plot_F = False
prime_function_tests = False
plot_branch_pts = True

def main():
	[delta, q] = define_group_data(0) #change example number here
	forward_problem(delta,q, plot_circles=plot_circles, plot_F=plot_F,
	prime_function_tests=prime_function_tests, plot_brannch_pts=plot_branch_pts,
	product_threshold=12, max_time=200)


def define_group_data(example_num):
	if example_num == 0: # start with genus 1
		return [0], [1/2] # delta, q
	
	if example_num == 1: # another genus 0, but more interesting
		return [1/2], [1/8] # delta, q

	if example_num == 2: #genus 2,
		return [-1/2,1/2], [1/4,1/4] # delta, q


if __name__ == '__main__':
    main()

