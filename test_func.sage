#####
import time

#def compute_omega(method):
#	

@parallel(4)
def updateOmegap(letters):
#Works! Must call "reduce(operator.mul, OUTPUT,1)"
	output = 1
	W = Words(genus, letters)
	for w in W.list():
        	indexlist = [int(nn) for nn in str(w)] # Make this list actually an
                                                  # indexing list
        	wordlyfe = G(indexlist) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
        	phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
		output *= (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))
	return output
 

#@parallel
def updateOmegap2(letters):
#Works! Must call "reduce(operator.mul, OUTPUT,1)"
	W = Words(genus, letters)
	output = iterate_words(W)
	from operator import itemgetter
	output = map(itemgetter(-1),output)
	return reduce(operator.mul, output,1)
 
@parallel
def iterate_words(w):
	wordlyfe = G(w) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
	phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
	return (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))

#time1 = time.time()
#reduce(operator.mul,map(updateOmegap,range(1,product_threshold+1)),1)
#time2 = time.time()
#print str(time2-time1)

time1 = time.time()
reduce(operator.mul,map(updateOmegap2,range(1,product_threshold+1)),1)
time2 = time.time()
print str(time2-time1)


