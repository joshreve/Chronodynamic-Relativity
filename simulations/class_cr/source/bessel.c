/**
 * CLASS-CR: Fast Spherical Bessel Functions Implementation
 * ========================================================
 * Uses Miller's downward recurrence for numerical stability when x < l,
 * upward recurrence when x > l, and series/asymptotics where appropriate.
 */

#include "bessel.h"
#include <stdlib.h>
#include <stdio.h>

#define _EPS_ 1e-15

double bessel_jl(int l, double x) {
    if (x < 0.0) {
        double sign = (l % 2 == 0) ? 1.0 : -1.0;
        return sign * bessel_jl(l, -x);
    }
    if (x < 1e-5) {
        if (l == 0) return 1.0 - x * x / 6.0;
        if (l == 1) return x / 3.0 - (x * x * x) / 30.0;
        if (l == 2) return (x * x) / 15.0;
        return 0.0;
    }
    if (l == 0) {
        return sin(x) / x;
    }
    if (l == 1) {
        return (sin(x) / (x * x)) - (cos(x) / x);
    }
    
    // For x significantly smaller than l, j_l(x) is negligible
    if (x < 0.2 * l) {
        return 0.0;
    }

    // Upward recurrence is stable when x > l
    if (x > (double)l) {
        double j0 = sin(x) / x;
        double j1 = (sin(x) / (x * x)) - (cos(x) / x);
        double j_curr = 0.0;
        for (int k = 1; k < l; k++) {
            j_curr = ((2.0 * k + 1.0) / x) * j1 - j0;
            j0 = j1;
            j1 = j_curr;
        }
        return j1;
    }

    // Miller's downward recurrence when x <= l
    int l_start = l + (int)(sqrt(40.0 + 20.0 * l)) + 15;
    double j_next = 0.0;
    double j_curr = 1e-30;
    double j_prev = 0.0;
    double target_jl = 0.0;

    for (int k = l_start; k >= 1; k--) {
        j_prev = ((2.0 * k + 1.0) / x) * j_curr - j_next;
        if (k == l) {
            target_jl = j_curr;
        }
        j_next = j_curr;
        j_curr = j_prev;
        if (fabs(j_curr) > 1e100) {
            j_curr *= 1e-100;
            j_next *= 1e-100;
            target_jl *= 1e-100;
        }
    }

    // At completion of k=1, j_curr is j_0 and j_next is j_1
    double j0_true = sin(x) / x;
    double j1_true = (sin(x) / (x * x)) - (cos(x) / x);
    if (fabs(j_curr) >= fabs(j_next)) {
        if (fabs(j_curr) > _EPS_) {
            return target_jl * (j0_true / j_curr);
        }
    } else {
        if (fabs(j_next) > _EPS_) {
            return target_jl * (j1_true / j_next);
        }
    }
    return 0.0;
}

double bessel_jl_prime(int l, double x) {
    if (l == 0) {
        if (x < 1e-5) return -x / 3.0;
        return (x * cos(x) - sin(x)) / (x * x);
    }
    // Relation: j'_l(x) = (l / x) * j_l(x) - j_{l+1}(x)
    return ((double)l / x) * bessel_jl(l, x) - bessel_jl(l + 1, x);
}

void bessel_jl_array(int l_max, double x, double *jl_out) {
    if (x < 1e-5) {
        jl_out[0] = 1.0;
        for (int l = 1; l <= l_max; l++) jl_out[l] = 0.0;
        return;
    }
    
    jl_out[0] = sin(x) / x;
    if (l_max >= 1) {
        jl_out[1] = (sin(x) / (x * x)) - (cos(x) / x);
    }
    
    // Upward recurrence
    for (int l = 1; l < l_max; l++) {
        if (x > (double)l) {
            jl_out[l + 1] = ((2.0 * l + 1.0) / x) * jl_out[l] - jl_out[l - 1];
        } else {
            // Fill remaining with individual stable evaluation
            for (int k = l; k <= l_max; k++) {
                jl_out[k] = bessel_jl(k, x);
            }
            break;
        }
    }
}
