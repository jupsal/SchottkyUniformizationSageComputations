###############################################################################
# Defines the function which builds the slit map (5.19).
# requires: omega, gamma
###############################################################################

def build_slitmap():
	return ( omega(gamma=-1)^2 + omega(gamma=1)^2 )/( omega(gamma = -1)^2 - omega(gamma=1)^2 )
	return None
