###############################################################################
# Builds the prime function. 
G = FreeGroup(genus) #G is a free group on number = genus generators.
omegap = 1 #Initial choice for omegap, multiply by stuff laters
for k in range(1,product_threshold+1):
    W = Words(genus,k) # This is our indexing set, gives all words with alphabet
                       # 1,2,...,genus of length k
    for j in range(len(W.list())):
        indexlist = [int(nn) for nn in str(W[j])] # Make this list actually an
                                                  # indexing list
        wordlyfe = G(indexlist) # for elements x0,x1,...,xn of the free group
                                # and if indexlist=[1,2,...,p] (for p<n) this
                                # gives x0*x1*...*xp for example.
        phi_i = wordlyfe([phi_j(nn) for nn in range(genus)]) # Now we replace
                                                # x0 with phi_j(0), (i.e.
                                                # theta_0). This is now a
                                                # function of z
        omegap *= (phi_i - gamma)*(phi_i(z=gamma)-z)/((phi_i -
                        z)*(phi_i(z = gamma) - gamma))
                #This is formula (5.13) in "Computational approach..." - Bobenko
                #etc. Chap 5

## Now form the SK prime function,
omega = (z - gamma)*omegap
### The above product is OBVIOUSLY very costly. Boooooo

if (prime_function_tests): attach("prime_function_tests.sage")
