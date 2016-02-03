###############################################################################
# This sagefile is the main file for uniformization as done in chapter 5 of "A
# computational approach..." - Bobenko. From here we can test various things.
# Right now these include:
# (a) Go from group data to real hyperbolic algebraic curve by specifying
# centers and radii of circles contained within the unit circle (i.e. the
# classical schottky group).
# (b) Testing the convergence of the product formula (5.13) for the prime
# function by examining the result of the slit mapping.
# 	(b) (i) We can choose to output further diagnostics if we want to look
# 	at only one of the conformal mappings in (5.18)  -- THIS IS VERY VERY
# 	slow right now!! If we need to do it more in the future that little
# 	section needs to be implemented better which wouldn't be hard but is
# 	currently not a priority since this will probably rarely be used.
# (c) Testing what happens for different genera.
# (d) Testing what happens if group data is not forced to be real data, is this
# the non-hyperelliptic case??
#
# A few things that NEED to be done in the near future:
# (a) Setup the algebraic equations so that this can be done in reverse. I.e.
# from branch-point data go to group data.
# 
# Ongoing questions that arise from and might be answered by this tool:
# (a) What happens if the circles are not on the real line in terms of the
# branch point data we reproduce?
# (b) Given two algebraic curves with the SAME branching structure but actually
# that look a lot different, what happens? The group data obviously doesn't
# change. Are the Riemann Surfaces the same?
# (c) What happens if two circles, in the group data, touch slightly or are just
# very close? What is the image under the slit map?
# (d) What happens for a line, in the image of the slit map, going from the
# upper-half to the lower-half plane through the interval [-1,1]?
#
# Other notes:
# (a) The convention of #D# commenting out deprecated code is used throughout
# for code that is being currently developed. There should always be a note at
# the beginning of the section where a bunch of stuff is deprecated to explain
# why it is now not used in case it has later use. The explanation shall be
# additionally blocked off as:
# #D# --Stuff---
# #D# --Stuff--- etc.
# (b) ...
###############################################################################

load("initialize.sage")

#Which problem?
forward_problem = True


if forward_problem: load("forward_problem.sage")

