/**
 * CLASS-CR: Common Definitions, Structures, and Constants
 */

#ifndef __COMMON_CR_H__
#define __COMMON_CR_H__

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define _SUCCESS_ 0
#define _FAILURE_ 1
#define _TRUE_ 1
#define _FALSE_ 0

#define _MAX_TITLE_ 1024
#define _MAX_STRING_ 2048

/* Fundamental Physical Constants (SI & Cosmological Units) */
#define _C_LIGHT_KM_S_ 299792.458
#define _C_LIGHT_M_S_ 299792458.0
#define _G_NEWTON_SI_ 6.67430e-11
#define _MPC_IN_M_ 3.08567758149137e22
#define _T_CMB_K_ 2.7255
#define _SIGMA_THOMSON_M2_ 6.6524587321e-29
#define _M_PROTON_KG_ 1.67262192369e-27
#define _M_ELECTRON_KG_ 9.1093837015e-31
#define _K_BOLTZMANN_SI_ 1.380649e-23
#define _HBAR_SI_ 1.054571817e-34

#define _MODEL_CR_ 0
#define _MODEL_LCDM_ 1

/* Chronodynamic Precision & Physical Model Parameters */
typedef struct {
    int model_type;             /* 0: Chronodynamic Relativity; 1: Standard LambdaCDM */
    double H0;                  /* Hubble constant in km/s/Mpc */
    double omega_b;             /* Baryon physical density \Omega_b h^2 */
    double omega_cdm;           /* Cold dark matter density \Omega_c h^2 (0.0 for CR, ~0.120 for LCDM) */
    double n_space;             /* Chronodynamic space-density parameter (default: 0.239) */
    double A_s;                 /* Primordial scalar amplitude (default: 2.1e-9) */
    double n_s;                 /* Primordial spectral index (default: 0.9649) */
    double z_reio;              /* Reionization redshift (default: 7.82) */
    double Y_p;                 /* Helium primordial fraction (default: 0.245) */
    
    /* Chronodynamic Acoustic & Potential Coupling */
    double l_A_0;               /* Asymptotic acoustic scale (e.g. 316.29) */
    double delta_1;             /* Low-l dispersion shift (e.g. -1.026) */
    double ell_0;               /* Transition knee scale (e.g. 220.9) */
    double alpha_1;             /* Dispersion exponent (e.g. 3.01) */
    double phi_0;               /* Primordial phase offset in radians (e.g. -2.892) */
    double beta_boost;          /* Potential root factor (e.g. 76.63) */
    double psi_0;               /* Potential well coupling (e.g. 0.273) */
    double A_ISW;               /* Early ISW amplitude (e.g. 112.0) */
    double ell_ISW;             /* Early ISW peak multipole (e.g. 136.9) */
    double A_0;                 /* Acoustic modulation amplitude (e.g. 1042.6) */
    double A_base;              /* Acoustic fluid floor (e.g. 4487.8) */
    double gamma_d;             /* Silk damping exponent (e.g. 1.770) */
    double sigma_lens;          /* Refractive lensing kernel width (e.g. 74.8) */
    double refract_amp;         /* Refractive lensing smoothing amplitude factor (default: 1.0) */
    double c_dipole;            /* Doppler dipole velocity coupling factor (default: 1.0) */
    double l_drag;              /* Baryon drag potential decay scale (default: 420.0) */
    double c_drag;              /* Baryon drag offset amplitude factor (default: 1.0) */
    double sw_norm;             /* Sachs-Wolfe baseline (e.g. 707.3) */
    double y_cal;               /* Calibration factor (e.g. 0.9138) */
    double A_ps;                /* Point source amplitude (e.g. 28.62) */
    
    /* Relativistic Neutrino Hierarchy */
    double N_ur;                /* Ultra-relativistic effective species (default: 3.044) */
    int has_neutrino_hierarchy; /* 1: Full neutrino moments F_nu,l; 0: Fluid approx */
    
    /* Perturbations Method Selection */
    #define _PERTURBATIONS_TEMPLATE_ 0
    #define _PERTURBATIONS_ODE_ 1
    #define _PERTURBATIONS_FIRST_PRINCIPLES_ 2
    int perturbations_method;   /* 0: Analytic oscillator template; 1: Coupled fluid Runge-Kutta ODE system; 2: Full first-principles field equations */
    
    /* Transfer Method Selection */
    #define _TRANSFER_EXACT_ 1
    int transfer_method;        /* Exact Line-of-Sight Bessel Integral Engine */
    int fast_bessel;            /* 1: Fast delta-function screen at tau_*; 0: Full line-of-sight visibility shell integration */
    int dense_bessel;           /* 1: Direct Bessel evaluation on all multipoles without spline subsampling */
    
    /* Numerical & Output Precision */
    int l_max;                  /* Maximum multipole l (default: 2500) */
    int l_max_pert;             /* Maximum multipole in hierarchy (default: 17) */
    int l_max_hierarchy;        /* Maximum Boltzmann hierarchy multipole (default: 8) */
    int include_polarization_feedback; /* 1: Full polarization quadrupole backreaction; 0: Truncated */
    double slip_coupling_scale; /* Dynamic metric slip transition scale */
    int n_k_modes;              /* Number of k-modes (default: 1500) */
} ClassCRPrecision;

#endif /* __COMMON_CR_H__ */
