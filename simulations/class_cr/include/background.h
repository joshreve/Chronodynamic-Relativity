/**
 * CLASS-CR: Background Module Header
 */

#ifndef __BACKGROUND_CR_H__
#define __BACKGROUND_CR_H__

#include "common.h"

typedef struct {
    int model_type;
    double H0;
    double h;
    double Omega_b;
    double Omega_cdm;
    double Omega_m;
    double Omega_Lambda;
    double Omega_gamma;
    double Omega_nu;
    double Omega_r;
    double n_space;
    
    int n_points;
    double *a_grid;
    double *z_grid;
    double *tau_grid;
    double *H_grid;
    double tau_today;
} ClassCRBackground;

int background_init(ClassCRPrecision *prec, ClassCRBackground *bg);
int background_free(ClassCRBackground *bg);
double background_z_exp(ClassCRBackground *bg, double z_obs);
double background_hubble(ClassCRBackground *bg, double z);
double background_conformal_time(ClassCRBackground *bg, double a);
double background_scale_factor(ClassCRBackground *bg, double tau);
double background_sound_speed(ClassCRBackground *bg, double a);

#endif /* __BACKGROUND_CR_H__ */
