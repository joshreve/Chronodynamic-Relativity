/**
 * CLASS-CR: Background Module Implementation
 */

#include "background.h"

int background_init(ClassCRPrecision *prec, ClassCRBackground *bg) {
    bg->model_type = prec->model_type;
    bg->H0 = prec->H0;
    bg->h = prec->H0 / 100.0;
    bg->Omega_b = prec->omega_b / (bg->h * bg->h);
    bg->n_space = prec->n_space;
    
    // Radiation density
    bg->Omega_gamma = 2.47e-5 / (bg->h * bg->h);
    bg->Omega_nu = 3.044 * (7.0 / 8.0) * pow(4.0 / 11.0, 4.0 / 3.0) * bg->Omega_gamma;
    bg->Omega_r = bg->Omega_gamma + bg->Omega_nu;
    
    if (bg->model_type == _MODEL_LCDM_) {
        bg->Omega_cdm = prec->omega_cdm / (bg->h * bg->h);
        bg->Omega_m = bg->Omega_b + bg->Omega_cdm;
        bg->Omega_Lambda = 1.0 - bg->Omega_m - bg->Omega_r;
    } else {
        bg->Omega_cdm = 0.0;
        bg->Omega_m = bg->Omega_b;
        bg->Omega_Lambda = 0.0;
    }
    
    bg->n_points = 2000;
    bg->a_grid = (double *)malloc(bg->n_points * sizeof(double));
    bg->z_grid = (double *)malloc(bg->n_points * sizeof(double));
    bg->tau_grid = (double *)malloc(bg->n_points * sizeof(double));
    bg->H_grid = (double *)malloc(bg->n_points * sizeof(double));
    
    if (!bg->a_grid || !bg->z_grid || !bg->tau_grid || !bg->H_grid) {
        return _FAILURE_;
    }
    
    // Logarithmic scale factor grid from a = 1e-9 to a = 1.0
    double log_a_min = -9.0;
    double log_a_max = 0.0;
    double dlog_a = (log_a_max - log_a_min) / (bg->n_points - 1);
    
    for (int i = 0; i < bg->n_points; i++) {
        double log_a = log_a_min + i * dlog_a;
        bg->a_grid[i] = pow(10.0, log_a);
        bg->z_grid[i] = (1.0 / bg->a_grid[i]) - 1.0;
        bg->H_grid[i] = background_hubble(bg, bg->z_grid[i]);
    }
    
    // Conformal time integration \tau(a) = \int_0^a c da / (a^2 H(a))
    bg->tau_grid[0] = (_C_LIGHT_KM_S_ * bg->a_grid[0]) / (bg->H0 * sqrt(bg->Omega_r));
    for (int i = 1; i < bg->n_points; i++) {
        double da = bg->a_grid[i] - bg->a_grid[i-1];
        double f_prev = _C_LIGHT_KM_S_ / (bg->a_grid[i-1] * bg->a_grid[i-1] * bg->H_grid[i-1]);
        double f_curr = _C_LIGHT_KM_S_ / (bg->a_grid[i] * bg->a_grid[i] * bg->H_grid[i]);
        bg->tau_grid[i] = bg->tau_grid[i-1] + 0.5 * (f_prev + f_curr) * da;
    }
    
    bg->tau_today = bg->tau_grid[bg->n_points - 1];
    return _SUCCESS_;
}

int background_free(ClassCRBackground *bg) {
    if (bg->a_grid) free(bg->a_grid);
    if (bg->z_grid) free(bg->z_grid);
    if (bg->tau_grid) free(bg->tau_grid);
    if (bg->H_grid) free(bg->H_grid);
    return _SUCCESS_;
}

double background_z_exp(ClassCRBackground *bg, double z_obs) {
    if (bg->model_type == _MODEL_LCDM_) return z_obs;
    return pow(1.0 + z_obs, 1.0 / (1.0 + bg->n_space / 2.0)) - 1.0;
}

double background_hubble(ClassCRBackground *bg, double z) {
    if (bg->model_type == _MODEL_LCDM_) {
        double one_plus_z = 1.0 + z;
        double z2 = one_plus_z * one_plus_z;
        double z3 = z2 * one_plus_z;
        double z4 = z3 * one_plus_z;
        return bg->H0 * sqrt(bg->Omega_r * z4 + bg->Omega_m * z3 + bg->Omega_Lambda);
    }
    double z_exp = background_z_exp(bg, z);
    return bg->H0 * (1.0 + z_exp) * pow(1.0 + z_exp, bg->n_space / 2.0);
}

double background_conformal_time(ClassCRBackground *bg, double a) {
    if (a <= bg->a_grid[0]) return bg->tau_grid[0];
    if (a >= bg->a_grid[bg->n_points - 1]) return bg->tau_today;
    
    // Linear interpolation
    int idx = 0;
    while (idx < bg->n_points - 1 && bg->a_grid[idx+1] < a) idx++;
    double t = (a - bg->a_grid[idx]) / (bg->a_grid[idx+1] - bg->a_grid[idx]);
    return bg->tau_grid[idx] + t * (bg->tau_grid[idx+1] - bg->tau_grid[idx]);
}

double background_scale_factor(ClassCRBackground *bg, double tau) {
    if (tau <= bg->tau_grid[0]) return bg->a_grid[0];
    if (tau >= bg->tau_today) return 1.0;
    
    int idx = 0;
    while (idx < bg->n_points - 1 && bg->tau_grid[idx+1] < tau) idx++;
    double t = (tau - bg->tau_grid[idx]) / (bg->tau_grid[idx+1] - bg->tau_grid[idx]);
    return bg->a_grid[idx] + t * (bg->a_grid[idx+1] - bg->a_grid[idx]);
}

double background_sound_speed(ClassCRBackground *bg, double a) {
    double R_b = (3.0 * bg->Omega_b) / (4.0 * bg->Omega_gamma) * a;
    return 1.0 / sqrt(3.0 * (1.0 + R_b));
}
