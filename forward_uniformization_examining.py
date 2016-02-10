###############################################################################
# This file holds some examples for examining the forward problem, i.e. by
# plotting some points or lines or both and looking at their image under the
# slitmap
###############################################################################

import uniformization
from uniformization.forward_problem import forward_problem_on_points_and_lines
#import forward_problem

plot_circles = True
plot_F = False
prime_function_tests = False
slitmap_tests = False
slitmap_full = True
slitmap_direct = False
prec = 'double' # inf precision takes just a little bit longer for example 2
example_number = 1 #choose from the examples below.

def main():
    delta, q = define_group_data(example_number)

    points = [I/2, -I/2]

    forward_problem_on_points_and_lines(
        delta, q, points, plot_circles=True, slitmap_full=slitmap_full,
        slitmap_direct=slitmap_direct, prec=prec, product_threshold=3,
        max_time=200, prime_function_tests=prime_function_tests,
        slitmap_tests=slitmap_tests
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


if __name__ == '__main__':
    main()

