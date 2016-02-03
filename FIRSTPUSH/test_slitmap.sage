###############################################################################
# Test slit map diagnostics

print '------------------------- Slit map tests ---------------------------'

# The first test consists of seeing if the left endpoint of our interval is -1
# and the right endpoint is 1. We also allow the alternative for "flipped" .i.e.
# t=0 maps to the left endpoint and t=pi maps to the right endpoint, though this
# should certainly not occur. If it does we need to examine.

test = 'Passed'
if (slitmap(z=C0(t=0)) != 1): #make sure we map to 1 or -1
	if (slitmap(z=C0(t=0)) == -1):
		test = 'Passed but FLIPPED'
	else: test = 'Failed' #else test fails
print 'test1:					', test

#Do the same thing at t=pi
test = 'Passed'
if (slitmap(z=C0(t=pi)) != -1):
	if(slitmap(z=C0(t=pi))==1):
		test = 'Passed but FLIPPED'
	else: test = 'Failed'
print 'test2:					', test
	
print '------------------------ End slit map tests ------------------------------'

