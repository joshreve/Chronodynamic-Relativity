/**
 * CLASS-CR: Fast Spherical Bessel Function Header
 * ===============================================
 * Computes spherical Bessel functions j_ell(x) and derivatives j'_ell(x)
 * with high numerical stability and speed.
 */

#ifndef __BESSEL_CR_H__
#define __BESSEL_CR_H__

#include <math.h>

/* Compute spherical Bessel j_l(x) */
double bessel_jl(int l, double x);

/* Compute derivative of spherical Bessel j'_l(x) */
double bessel_jl_prime(int l, double x);

/* Compute array of j_l(x) for all l from 0 to l_max at fixed x */
void bessel_jl_array(int l_max, double x, double *jl_out);

#endif /* __BESSEL_CR_H__ */
