/**
 * CLASS-CR: Perturbations Module Header
 */

#ifndef __PERTURBATIONS_CR_H__
#define __PERTURBATIONS_CR_H__

#include "common.h"
#include "background.h"
#include "thermodynamics.h"

typedef struct {
    double k_mpc;
    int n_tau;
    double *tau_grid;
    double *source_monopole;      /* Monopole source: g * (Theta_0 + Psi) */
    double *source_dipole;        /* Dipole velocity source: g * (v_b / 3) */
    double *source_isw;           /* ISW potential decay: exp(-tau_c) * (dPhi/dtau + dPsi/dtau) */
    double *source_polarization;  /* Polarization quadrupole source: g * Pi */
    double *source_quadrupole;    /* Viscous shear quadrupole: g * Theta_2 */
    double *source_slip;          /* Metric slip function: eta_slip(tau) = Phi / Psi */
    double *baryon_velocity;      /* Baryon fluid velocity: theta_b(tau) */
    double *baryon_density;       /* Baryon density perturbation: delta_b(tau) */
} ClassCRKModeSolution;

typedef struct {
    int l_max;
    int l_max_nu;
    int n_k;
    double *k_grid;
    ClassCRKModeSolution *k_solutions;
} ClassCRPerturbations;

int perturbations_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert);
int perturbations_free(ClassCRPerturbations *pert);
int perturbations_solve_mode(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double k_mpc, ClassCRKModeSolution *sol);

#endif /* __PERTURBATIONS_CR_H__ */
