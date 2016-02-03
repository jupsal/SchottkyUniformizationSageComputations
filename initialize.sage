###############################################################################
# This should be run at the start of every run, it resets everything and
# redefines variables.
###############################################################################

reset() #Reset everything, start from scratch.

# Preamble, this should not be touched for different R.S.
x,y = var('x,y')
assume(x,'real'); assume(y,'real')
zeta = x+I*y #local variable
t = var('t') # for parametric plotting
z = var('z') # complex variable not specified by x,y
gamma = var('gamma') #base point for 'abelmap' or prime function

