/**
 * CLASS-CR: Thermodynamics Module Header
 */

#ifndef __THERMODYNAMICS_CR_H__
#define __THERMODYNAMICS_CR_H__

#include "common.h"
#include "background.h"

typedef struct {
    double z_star;
    double tau_star;
    double tau_reio;
    double r_s_star;
    double r_d_star;
    
    int n_points;
    double *z_grid;
    double *tau_grid;
    double *Xe_grid;
    double *kappa_dot_grid;
    double *kappa_grid;
    double *visibility_grid;
} ClassCRThermodynamics;

int thermodynamics_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th);
int thermodynamics_free(ClassCRThermodynamics *th);
double thermodynamics_visibility(ClassCRThermodynamics *th, double tau);
double thermodynamics_optical_depth(ClassCRThermodynamics *th, double tau);
double thermodynamics_kappa_dot(ClassCRThermodynamics *th, double tau);

#endif /* __THERMODYNAMICS_CR_H__ */
