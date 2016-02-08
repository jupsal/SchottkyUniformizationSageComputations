from sage.all import *
from nose.plugins.skip import SkipTest

from my_package.prime_function import build_prime_function



#############################################################################
# The following tests use the nosetest generator syntax. See                #
#                                                                           #
# https://nose.readthedocs.org/en/latest/writing_tests.html#test-generators #
#                                                                           #
# for more information. The "checks" used by these tests are defined below. #
#############################################################################
z = var('z')
gamma = var('gamma')

def test_prime_function():
    # run the "checks" below using the following list of (delta,q) pairs
    half = QQ(1)/2
    delta_q_pairs = [
        # ([0], [half]),
        ([half], [half/4]),
        ([-half, half], [half/2, half/2]),
    ]
    product_threshold = 10

    for delta, q in delta_q_pairs:
        genus = len(delta)
        omega = build_prime_function(delta, q, product_threshold)
        phi_j = [
            delta[j] + q[j]**2*z/(1-z*delta[j].conjugate())
            for j in range(genus)
        ]
        yield check_vanishing_gamma, omega
        yield check_vanishing_phij_gamma, omega, phi_j
        yield check_pole_fixed_points, omega, delta, q, phi_j, genus
        # yield check_equation_5_17, omega
        yield check_symmetric, omega

##########
# checks #
##########
def check_vanishing_gamma(omega):
    # Tests that omega(gamma1,gamma2) vanishes.
    value = omega(z=gamma)
    assert simplify(value) == 0

def check_vanishing_phij_gamma(omega, phi_j):
    # Tests that omega(phi_j(gamma1), phi_j(gamma2)) vanishes.
    value = sum(omega(z=phi_jk(z=gamma)) for phi_jk in phi_j)
    assert simplify(value) == 0

def check_pole_fixed_points(omega, delta, q, phi_j, genus):
    # Tests that omega has poles at the fixed points of phi_j.
    term_1 = lambda k: 1 + abs(delta[k])**2 - q[k]**2
    term_2 = lambda k: sqrt(-4*abs(delta[k])**2 + (1+abs(delta[k])**2-q[k]**2)**2)
    denom = lambda k: 2*delta[k].conjugate()
    pole_pt1 = lambda k: (term_1(k) + term_2(k)) / denom(k)
    pole_pt2 = lambda k: (term_1(k) - term_2(k)) / denom(k)

    # assert that these are, in fact, fixed poitns of phi_j
    pole_sum1 = sum(N(phi_j[k](z=pole_pt1(k)) - pole_pt1(k)) for k in range(genus))
    pole_sum2 = sum(N(phi_j[k](z=pole_pt2(k)) - pole_pt2(k)) for k in range(genus))
    value = pole_sum1 + pole_sum2
    assert abs(simplify(value)) < 1e-15

    # perturb slightly to avoid returning an error (result should be large?).
    # as we get closer to the pole the values should be increasing (towards
    # infinity)
    sum1 = sum(N(omega(z=pole_pt1(k) + 1e-10, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-10, gamma=1))
               for k in range(genus))
    sum2 = sum(N(omega(z=pole_pt1(k) + 1e-13, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-13, gamma=1))
               for k in range(genus))
    sum3 = sum(N(omega(z=pole_pt1(k) + 1e-15, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-15, gamma=1))
               for k in range(genus))
    assert abs(sum3) > abs(sum2) > abs(sum1)

    # repeat at gamma = -1
    sum1 = sum(N(omega(z=pole_pt1(k) + 1e-10, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-10, gamma=-1))
               for k in range(genus))
    sum2 = sum(N(omega(z=pole_pt1(k) + 1e-13, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-13, gamma=-1))
               for k in range(genus))
    sum3 = sum(N(omega(z=pole_pt1(k) + 1e-15, gamma=1) +
                 omega(z=pole_pt2(k) + 1e-15, gamma=-1))
               for k in range(genus))
    assert abs(sum3) > abs(sum2) > abs(sum1)

def check_equation_5_17(omega):
    # we also check to see if (5.17) holds, it doesn't unless we take the
    # infinite product, but should approach it as the product_threshold
    # increases! Again choose a number for gamma.
    fiveone7a = omega(z=1/z.conjugate(), gamma=1/gamma.conjugate())
    fiveone7 = fiveone7a.conjugate() + omega/(z*gamma)
    value = abs(N(fiveone7(z=(3+I*3),gamma=1)))
    assert simplify(value) < 1e-8

    value = abs(N(fiveone7(z=0.7+0.1*I,gamma=1)) )
    assert simplify(value) < 1e-8

def check_symmetric(omega):
    # the SK-prime function should also be symmetric in its arguments. I.e. one
    # should have omega(zeta,gamma) = -omega(gamma,zeta). Test this
    # algebraically
    p = var('p')
    q = var('q')
    value = omega(z=p,gamma=q) + omega(z=q,gamma=p)
    assert simplify(value) == 0

