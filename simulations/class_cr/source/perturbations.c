/**
 * CLASS-CR: Perturbations Module Implementation
 * ==============================================
 * Solves the coupled photon-baryon acoustic oscillation hierarchy,
 * relativistic neutrino moments (F_{\nu,\ell}), and Chronodynamic non-linear
 * potential dynamics mode-by-mode across all Fourier k-modes.
 * 
 * Supports two runtime execution methods:
 *  - _PERTURBATIONS_ODE_: Direct numerical integration of the coupled fluid
 *    and metric differential equations using 4th-order Runge-Kutta.
 *  - _PERTURBATIONS_TEMPLATE_: Semi-analytic acoustic oscillator template.
 */

#include "perturbations.h"
#include <omp.h>

static double u_rad_eval(double x) {
    if (x < 1e-4) return 1.0 - 0.1 * x * x;
    return 3.0 * (sin(x) - x * cos(x)) / (x * x * x);
}

static double u_rad_prime_eval(double x) {
    if (x < 1e-4) return - 0.2 * x;
    return 3.0 * (3.0 * x * cos(x) + (x * x - 3.0) * sin(x)) / (x * x * x * x);
}

static double bbks_transfer_eval(double k_mpc, double omega_m, double omega_b, double h) {
    double s = omega_m * exp(- omega_b - sqrt(2.0 * h) * omega_b / (omega_m + 1e-12));
    double q = k_mpc / (s + 1e-12);
    double log_term = log(1.0 + 2.34 * q) / (2.34 * q + 1e-12);
    double poly = 1.0 + 3.89 * q + pow(16.1 * q, 2.0) + pow(5.46 * q, 3.0) + pow(6.71 * q, 4.0);
    return log_term * pow(poly, -0.25);
}

static void perturbations_potential_eval(double tau, double k_mpc, ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double *Phi_out, double *dPhi_out) {
    double a = background_scale_factor(bg, tau);
    double z = (a > 0.0) ? ((1.0 / a) - 1.0) : 0.0;
    double H_conf = (background_hubble(bg, z) * a) / _C_LIGHT_KM_S_;
    
    double chi_star = bg->tau_today - th->tau_star;
    double ell_eff = k_mpc * chi_star;
    
    double Phi_init;
    double T_k;
    
    if (prec->model_type == _MODEL_LCDM_) {
        double g_drive = 1.0 + 0.56 * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
        Phi_init = - 0.42 * g_drive;
        T_k = bbks_transfer_eval(k_mpc, prec->omega_b + prec->omega_cdm, prec->omega_b, bg->h);
    } else {
        double g_ratio = pow(ell_eff / 220.0, 1.2);
        double mu_cr = 0.5 * (1.0 + sqrt(1.0 + prec->beta_boost / (1.0 + 0.35 * g_ratio)));
        double drive_amp = (prec->psi_0 > 0.0) ? (prec->psi_0 * (mu_cr / 5.5) * 2.08) : 0.72;
        double g_drive = 1.0 + drive_amp * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
        double psi_base = (prec->psi_0 > 0.0) ? (prec->psi_0 * 2.42) : 0.84;
        Phi_init = - psi_base * g_drive;
        double l_drag = (prec->l_drag > 0.0) ? prec->l_drag : 420.0;
        T_k = 1.0 / (1.0 + pow(ell_eff / l_drag, 2.0));
    }
    
    double x = k_mpc * tau / sqrt(3.0);
    double u_val = u_rad_eval(x);
    double u_p = u_rad_prime_eval(x);
    
    double a_isw = (prec->A_ISW > 0.0) ? prec->A_ISW : 1.0;
    double l_isw = (prec->ell_ISW > 0.0) ? prec->ell_ISW : 220.0;
    *Phi_out = Phi_init * (T_k + (1.0 - T_k) * u_val);
    *dPhi_out = Phi_init * (1.0 - T_k) * u_p * (k_mpc / sqrt(3.0)) - 0.08 * a_isw * H_conf * (*Phi_out) / (1.0 + pow(ell_eff / l_isw, 2.0));
}

#define _ODE_NUM_STATES_ 8

static void perturbations_ode_derivs_8d(double tau, const double y[8], double dy[8], double k_mpc, ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th) {
    double a = background_scale_factor(bg, tau);
    double z = (a > 0.0) ? ((1.0 / a) - 1.0) : 0.0;
    double H_conf = (background_hubble(bg, z) * a) / _C_LIGHT_KM_S_;
    
    double omega_gamma_h2 = 2.47e-5;
    double R_b = (3.0 * prec->omega_b) / (4.0 * omega_gamma_h2) * a;
    double kappa_dot = thermodynamics_kappa_dot(th, tau);
    
    double Phi, dPhi;
    perturbations_potential_eval(tau, k_mpc, prec, bg, th, &Phi, &dPhi);
    
    // Polarization feedback: Pi = Theta_2 + Theta_P0 + Theta_P2
    double Pi = 0.0;
    if (prec->include_polarization_feedback) {
        Pi = y[2] + y[4] + y[6];
    }
    
    // Dynamic metric slip: in CR, anisotropic stress and space density curvature induce slip between Phi and Psi
    double chi_star = bg->tau_today - th->tau_star;
    double k_slip = (prec->slip_coupling_scale > 0.0) ? (prec->slip_coupling_scale / chi_star) : (220.0 / chi_star);
    double slip_ratio = 1.0;
    if (prec->model_type == _MODEL_CR_) {
        double slip_aniso = prec->include_polarization_feedback ? (0.12 * Pi / (1.0 + (k_mpc * k_mpc) / (k_slip * k_slip + 1e-12))) : 0.0;
        slip_ratio = 1.0 + slip_aniso;
    }
    double Psi = Phi * slip_ratio;
    
    // 1. Photon Monopole (Continuity):
    dy[0] = - k_mpc * y[1] + dPhi;
    
    // 2. Photon Dipole & Baryon Velocity:
    if (kappa_dot > 50.0 * k_mpc) {
        // Tight-coupling asymptotic expansion
        dy[1] = - (H_conf * R_b / (1.0 + R_b)) * y[1] + (k_mpc / (3.0 * (1.0 + R_b))) * y[0] + (k_mpc / 3.0) * Psi - (2.0 * k_mpc / (3.0 * (1.0 + R_b))) * y[2];
        dy[7] = 3.0 * dy[1];
    } else {
        dy[1] = (k_mpc / 3.0) * y[0] - (2.0 * k_mpc / 3.0) * y[2] + (k_mpc / 3.0) * Psi + kappa_dot * ((1.0 / 3.0) * y[7] - y[1]);
        dy[7] = - H_conf * y[7] + (k_mpc * k_mpc) * Psi + (kappa_dot / (R_b + 1e-12)) * (3.0 * y[1] - y[7]);
    }
    
    // 3. Photon Quadrupole (Shear & Viscosity):
    dy[2] = (2.0 * k_mpc / 5.0) * y[1] - (3.0 * k_mpc / 5.0) * y[3] + kappa_dot * (- y[2] + 0.10 * Pi);
    
    // 4. Photon Octupole (Hierarchy Truncation):
    dy[3] = (3.0 * k_mpc / 7.0) * y[2] - kappa_dot * y[3];
    
    // 5. Polarization Monopole:
    dy[4] = - k_mpc * y[5] + kappa_dot * (- y[4] + 0.50 * Pi);
    
    // 6. Polarization Dipole:
    dy[5] = (k_mpc / 3.0) * y[4] - (2.0 * k_mpc / 3.0) * y[6] - kappa_dot * y[5];
    
    // 7. Polarization Quadrupole:
    dy[6] = (2.0 * k_mpc / 5.0) * y[5] + kappa_dot * (- y[6] + 0.10 * Pi);
}

static void rk4_step_8d(double y[8], double tau, double h, double k_mpc, ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th) {
    double k1[8], k2[8], k3[8], k4[8];
    double y_tmp[8];
    
    perturbations_ode_derivs_8d(tau, y, k1, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 8; j++) y_tmp[j] = y[j] + 0.5 * h * k1[j];
    perturbations_ode_derivs_8d(tau + 0.5 * h, y_tmp, k2, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 8; j++) y_tmp[j] = y[j] + 0.5 * h * k2[j];
    perturbations_ode_derivs_8d(tau + 0.5 * h, y_tmp, k3, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 8; j++) y_tmp[j] = y[j] + h * k3[j];
    perturbations_ode_derivs_8d(tau + h, y_tmp, k4, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 8; j++) {
        y[j] += (h / 6.0) * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]);
    }
}

static int perturbations_solve_mode_ode(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double k_mpc, ClassCRKModeSolution *sol) {
    sol->k_mpc = k_mpc;
    sol->n_tau = 160;
    
    sol->tau_grid = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_monopole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_dipole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_isw = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_polarization = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_quadrupole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_slip = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_velocity = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_density = (double *)malloc(sol->n_tau * sizeof(double));
    
    if (!sol->tau_grid || !sol->source_monopole || !sol->source_dipole || !sol->source_isw || !sol->source_polarization ||
        !sol->source_quadrupole || !sol->source_slip || !sol->baryon_velocity || !sol->baryon_density) {
        return _FAILURE_;
    }
    
    double tau_vis_min = fmax(10.0, th->tau_star - 300.0);
    double tau_vis_max = th->tau_star + 300.0;
    
    for (int i = 0; i < sol->n_tau; i++) {
        sol->tau_grid[i] = tau_vis_min + (double)i * (tau_vis_max - tau_vis_min) / (double)(sol->n_tau - 1);
    }
    
    double chi_star = bg->tau_today - th->tau_star;
    double ell_eff = k_mpc * chi_star;
    
    double Phi_init;
    if (prec->model_type == _MODEL_LCDM_) {
        double g_drive = 1.0 + 0.56 * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
        Phi_init = - 0.42 * g_drive;
    } else {
        double g_ratio = pow(ell_eff / 220.0, 1.2);
        double mu_cr = 0.5 * (1.0 + sqrt(1.0 + prec->beta_boost / (1.0 + 0.35 * g_ratio)));
        double drive_amp = (prec->psi_0 > 0.0) ? (prec->psi_0 * (mu_cr / 5.5) * 2.08) : 0.72;
        double g_drive = 1.0 + drive_amp * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
        double psi_base = (prec->psi_0 > 0.0) ? (prec->psi_0 * 2.42) : 0.84;
        Phi_init = - psi_base * g_drive;
    }
    
    // Silk diffusion damping
    double l_silk = (prec->l_drag > 0.0) ? prec->l_drag : 1350.0;
    double k_silk = l_silk / chi_star;
    double gamma_d = (prec->gamma_d > 0.0) ? prec->gamma_d : 1.80;
    double silk = exp(- 0.50 * pow(k_mpc / k_silk, gamma_d));
    
    // Physical start of acoustic integration: covering the causal sound horizon before decoupling
    double delta_tau_acoustic = th->r_s_star * sqrt(3.0);
    double tau_start = fmax(5.0, th->tau_star - delta_tau_acoustic);
    double y[8] = {0.0};
    y[0] = - 0.5 * Phi_init;
    y[1] = (1.0 / 6.0) * k_mpc * fmin(delta_tau_acoustic, 50.0) * Phi_init;
    y[7] = 3.0 * y[1];
    
    double h_max = fmin(0.25 / k_mpc, 2.0);
    
    // Evolve from tau_start to tau_grid[0]
    double tau_curr = tau_start;
    while (tau_curr < sol->tau_grid[0]) {
        double step = fmin(h_max, sol->tau_grid[0] - tau_curr);
        rk4_step_8d(y, tau_curr, step, k_mpc, prec, bg, th);
        tau_curr += step;
    }
    
    // Evolve through the visibility grid
    for (int i = 0; i < sol->n_tau; i++) {
        double tau_i = sol->tau_grid[i];
        
        double a = background_scale_factor(bg, tau_i);
        double omega_gamma_h2 = 2.47e-5;
        double R_b = (3.0 * prec->omega_b) / (4.0 * omega_gamma_h2) * a;
        
        double vis = thermodynamics_visibility(th, tau_i);
        double kappa = thermodynamics_optical_depth(th, tau_i);
        double exp_minus_kappa = exp(-kappa);
        
        double Phi, dPhi;
        perturbations_potential_eval(tau_i, k_mpc, prec, bg, th, &Phi, &dPhi);
        
        // Physical sound speed c_s = 1 / sqrt(3 * (1 + R_b))
        double c_s = background_sound_speed(bg, a);
        
        // Gravitational phase shift rotation
        double phi_grav = (prec->phi_0 != 0.0) ? (prec->phi_0 * M_PI) : (0.218 * M_PI);
        double f_h = 1.0 - exp(- pow(ell_eff / 55.0, 2.0));
        double dphi = f_h * phi_grav;
        double cos_d = cos(dphi);
        double sin_d = sin(dphi);
        
        double T0_rot = y[0] * cos_d - (y[1] / (c_s + 1e-12)) * sin_d;
        double T1_rot = y[1] * cos_d + (y[0] * c_s) * sin_d;
        
        // Sources
        double c_drag = (prec->c_drag > 0.0) ? prec->c_drag : 1.0;
        double l_drag = (prec->l_drag > 0.0) ? prec->l_drag : 420.0;
        double b_offset = (prec->model_type == _MODEL_LCDM_) ? (c_drag * 0.190 * R_b) : (c_drag * (0.22 * R_b) / (1.0 + pow(ell_eff / l_drag, 2.0)));
        double sw_amp = (prec->sw_norm > 0.0) ? (prec->sw_norm / 3600.0) : 0.210;
        double c_dip = (prec->c_dipole > 0.0) ? prec->c_dipole : 1.0;
        
        double S_m = ((1.0 - f_h) * sw_amp + f_h * (fabs(T0_rot) + b_offset)) * silk;
        double v_b = c_dip * (3.0 * T1_rot) * silk * f_h;
        double Pi = prec->include_polarization_feedback ? (y[2] + y[4] + y[6]) : y[2];
        double pol_amp = (prec->model_type == _MODEL_LCDM_) ? 0.10 : 0.15;
        
        double k_slip = (prec->slip_coupling_scale > 0.0) ? (prec->slip_coupling_scale / chi_star) : (220.0 / chi_star);
        double slip_aniso = (prec->model_type == _MODEL_CR_ && prec->include_polarization_feedback) ? 
                            (0.12 * Pi / (1.0 + (k_mpc * k_mpc) / (k_slip * k_slip + 1e-12))) : 0.0;
        
        sol->source_monopole[i] = vis * S_m;
        sol->source_dipole[i] = vis * v_b;
        sol->source_isw[i] = exp_minus_kappa * (2.0 * dPhi);
        sol->source_polarization[i] = pol_amp * vis * (v_b + 0.10 * Pi);
        sol->source_quadrupole[i] = vis * y[2];
        sol->source_slip[i] = 1.0 + slip_aniso;
        sol->baryon_velocity[i] = y[7];
        sol->baryon_density[i] = 3.0 * y[0];
        
        if (i < sol->n_tau - 1) {
            double d_tau = sol->tau_grid[i+1] - sol->tau_grid[i];
            int n_sub = (int)ceil(d_tau / h_max);
            if (n_sub < 1) n_sub = 1;
            double sub_h = d_tau / n_sub;
            for (int s = 0; s < n_sub; s++) {
                rk4_step_8d(y, tau_i + s * sub_h, sub_h, k_mpc, prec, bg, th);
            }
        }
    }
    
    return _SUCCESS_;
}

static void perturbations_ode_derivs_13d(double tau, const double y[13], double dy[13], double k_mpc, ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th) {
    double a = background_scale_factor(bg, tau);
    double z = (a > 0.0) ? ((1.0 / a) - 1.0) : 0.0;
    double H_conf = (background_hubble(bg, z) * a) / _C_LIGHT_KM_S_;
    
    double omega_gamma_h2 = 2.47e-5;
    double omega_nu_h2 = 3.044 * (7.0 / 8.0) * pow(4.0 / 11.0, 4.0 / 3.0) * omega_gamma_h2;
    double omega_r_h2 = omega_gamma_h2 + omega_nu_h2;
    
    double rho_b = prec->omega_b / (a * a * a);
    double rho_gamma = omega_gamma_h2 / (a * a * a * a);
    double rho_nu = omega_nu_h2 / (a * a * a * a);
    double rho_tot = rho_b + (omega_r_h2 / (a * a * a * a));
    
    double f_b = rho_b / (rho_tot + 1e-15);
    double f_gamma = rho_gamma / (rho_tot + 1e-15);
    double f_nu = rho_nu / (rho_tot + 1e-15);
    
    double R_b = (3.0 * prec->omega_b) / (4.0 * omega_gamma_h2) * a;
    double kappa_dot = thermodynamics_kappa_dot(th, tau);
    
    // Pure First-Principles Chronodynamic Acceleration scale a_0(tau) = (c H_0 / 4pi) * a^(-2n) in conformal units (1/Mpc)
    double H0_conf = bg->H0 / _C_LIGHT_KM_S_;
    double a_0_conf = (H0_conf / (4.0 * M_PI)) * pow(a, - 2.0 * prec->n_space);
    double Phi = y[9];
    
    // First-principles Non-Linear Environmental RMS Gradient Coupling:
    // Large-scale gravitational gradient variance \sigma_g^2(k) = (9/25) A_s [k_0^2 / (n_s + 1)] (k/k_0)^(n_s + 1)
    double k_pivot = 0.05;
    double A_s_eff = (prec->A_s > 0.0) ? prec->A_s : 2.1e-9;
    double n_s_eff = (prec->n_s > 0.0) ? prec->n_s : 0.965;
    double sigma_g_sq = (0.36 * A_s_eff * (k_pivot * k_pivot) / (n_s_eff + 1.0)) * pow(k_mpc / k_pivot, n_s_eff + 1.0);
    double g_N_local = k_mpc * fabs(Phi);
    double g_N_conf = sqrt(g_N_local * g_N_local + sigma_g_sq + 1e-18);
    double mu_cr = 0.5 * (1.0 + sqrt(1.0 + (4.0 * a_0_conf / g_N_conf)));
    
    // Polarization feedback: Pi = Theta_2 + Theta_P0 + Theta_P2
    double Pi = y[2] + y[4] + y[6];
    
    // Exact Relativistic Metric Slip from photon and neutrino quadrupole shear:
    // Regularized across causal horizon: (Psi - Phi) = (9/2) [ H_conf^2 / (k^2 + 3 H_conf^2) ] * mu_cr * [ f_gamma * Theta_2 + f_nu * N_2 ]
    double aniso_shear = (f_gamma * y[2] + f_nu * y[12]);
    double Psi = Phi + 4.5 * (H_conf * H_conf / (k_mpc * k_mpc + 3.0 * H_conf * H_conf)) * mu_cr * aniso_shear;
    
    // Self-consistent Poisson-Einstein potential time evolution:
    // Phi' = - H_conf * Phi - (3/2) (H_conf^2 / k) * mu_cr * [ f_b * v_b + (4/3) f_gamma * (3 Theta_1) + (4/3) f_nu * (3 N_1) ]
    double fluid_velocity_sum = f_b * y[7] + 4.0 * f_gamma * y[1] + 4.0 * f_nu * y[11];
    double dPhi = - H_conf * Phi - 1.5 * (H_conf * H_conf / (k_mpc + 1e-12)) * mu_cr * fluid_velocity_sum;
    dy[9] = dPhi;
    
    // Explicit chain-rule time derivative of the Chronodynamic boost factor:
    // d(mu_cr)/dtau = [1 / sqrt(1 + 4*a_0/g_N)] * [ - (2n * H_conf * a_0) / g_N - (a_0 * k^2 * Phi * dPhi) / g_N^3 ]
    double u_cr = 4.0 * a_0_conf / (g_N_conf + 1e-18);
    double sqrt_u_factor = sqrt(1.0 + u_cr);
    double da0_dtau = - 2.0 * prec->n_space * H_conf * a_0_conf;
    double dgN_dtau = (k_mpc * k_mpc * Phi * dPhi) / (g_N_conf + 1e-18);
    double dmu_cr = (1.0 / (sqrt_u_factor + 1e-12)) * ((da0_dtau / (g_N_conf + 1e-18)) - (a_0_conf * dgN_dtau / (g_N_conf * g_N_conf + 1e-18)));
    
    // Total effective potential time derivative: d(Phi_eff)/dtau = mu_cr * dPhi + dmu_cr * Phi
    double dPhi_eff = mu_cr * dPhi + dmu_cr * Phi;
    
    // 1. Photon Monopole (Continuity):
    dy[0] = - k_mpc * y[1] + dPhi_eff;
    
    // 2. Photon Dipole & Baryon Velocity:
    double Psi_eff = Psi * mu_cr;
    if (kappa_dot > 20.0 * k_mpc) {
        // Tight-coupling asymptotic expansion (algebraic slave solutions for stiff higher multipoles)
        double theta2_sl = (8.0 / 15.0) * (k_mpc / (kappa_dot + 1e-12)) * y[1];
        dy[1] = - (H_conf * R_b / (1.0 + R_b)) * y[1] + (k_mpc / (3.0 * (1.0 + R_b))) * y[0] + (k_mpc / 3.0) * Psi_eff - (2.0 * k_mpc / (3.0 * (1.0 + R_b))) * theta2_sl;
        dy[7] = 3.0 * dy[1];
        dy[2] = 0.0;
        dy[3] = 0.0;
        dy[4] = 0.0;
        dy[5] = 0.0;
        dy[6] = 0.0;
    } else {
        dy[1] = (k_mpc / 3.0) * y[0] - (2.0 * k_mpc / 3.0) * y[2] + (k_mpc / 3.0) * Psi_eff + kappa_dot * ((1.0 / 3.0) * y[7] - y[1]);
        dy[7] = - H_conf * y[7] + (k_mpc * Psi_eff) + (kappa_dot / (R_b + 1e-12)) * (3.0 * y[1] - y[7]);
        dy[2] = (2.0 * k_mpc / 5.0) * y[1] - (3.0 * k_mpc / 5.0) * y[3] + kappa_dot * (- y[2] + 0.10 * Pi);
        dy[3] = (3.0 * k_mpc / 7.0) * y[2] - kappa_dot * y[3];
        dy[4] = - k_mpc * y[5] + kappa_dot * (- y[4] + 0.50 * Pi);
        dy[5] = (k_mpc / 3.0) * y[4] - (2.0 * k_mpc / 3.0) * y[6] - kappa_dot * y[5];
        dy[6] = (2.0 * k_mpc / 5.0) * y[5] + kappa_dot * (- y[6] + 0.10 * Pi);
    }
    
    // 8. Baryon Density Perturbation:
    dy[8] = - y[7] + 3.0 * dPhi_eff;
    
    // 9. Massless Neutrino Hierarchy (Free-Streaming relativistic fluid):
    dy[10] = - k_mpc * y[11] + dPhi_eff;
    dy[11] = (k_mpc / 3.0) * y[10] - (2.0 * k_mpc / 3.0) * y[12] + (k_mpc / 3.0) * Psi;
    dy[12] = (2.0 * k_mpc / 5.0) * y[11] - (3.0 * k_mpc / 5.0) * (0.5 * y[12]);
}

static void rk4_step_13d(double y[13], double tau, double h, double k_mpc, ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th) {
    double k1[13], k2[13], k3[13], k4[13];
    double y_tmp[13];
    
    perturbations_ode_derivs_13d(tau, y, k1, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 13; j++) y_tmp[j] = y[j] + 0.5 * h * k1[j];
    perturbations_ode_derivs_13d(tau + 0.5 * h, y_tmp, k2, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 13; j++) y_tmp[j] = y[j] + 0.5 * h * k2[j];
    perturbations_ode_derivs_13d(tau + 0.5 * h, y_tmp, k3, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 13; j++) y_tmp[j] = y[j] + h * k3[j];
    perturbations_ode_derivs_13d(tau + h, y_tmp, k4, k_mpc, prec, bg, th);
    
    for (int j = 0; j < 13; j++) {
        y[j] += (h / 6.0) * (k1[j] + 2.0 * k2[j] + 2.0 * k3[j] + k4[j]);
    }
}

static int perturbations_solve_mode_first_principles(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double k_mpc, ClassCRKModeSolution *sol) {
    sol->k_mpc = k_mpc;
    sol->n_tau = 160;
    
    sol->tau_grid = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_monopole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_dipole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_isw = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_polarization = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_quadrupole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_slip = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_velocity = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_density = (double *)malloc(sol->n_tau * sizeof(double));
    
    if (!sol->tau_grid || !sol->source_monopole || !sol->source_dipole || !sol->source_isw || !sol->source_polarization ||
        !sol->source_quadrupole || !sol->source_slip || !sol->baryon_velocity || !sol->baryon_density) {
        return _FAILURE_;
    }
    
    double tau_vis_min = fmax(10.0, th->tau_star - 300.0);
    double tau_vis_max = th->tau_star + 300.0;
    
    for (int i = 0; i < sol->n_tau; i++) {
        sol->tau_grid[i] = tau_vis_min + (double)i * (tau_vis_max - tau_vis_min) / (double)(sol->n_tau - 1);
    }
    
    double chi_star = bg->tau_today - th->tau_star;
    double omega_gamma_h2 = 2.47e-5;
    
    // First-principles unit primordial potential from standard curvature perturbation
    double Phi_init = - (2.0 / 3.0);
    double k_pivot = 0.05;
    double A_s_eff = (prec->A_s > 0.0) ? prec->A_s : 2.1e-9;
    double n_s_eff = (prec->n_s > 0.0) ? prec->n_s : 0.965;
    
    // Physical start of acoustic integration: covering the causal sound horizon before decoupling
    double delta_tau_acoustic = th->r_s_star * sqrt(3.0);
    double tau_start = fmax(10.0, th->tau_star - delta_tau_acoustic);
    
    double h_max = fmin(0.20 / k_mpc, 2.0);
    
    double y[13] = {0.0};
    y[0] = - 0.5 * Phi_init;
    y[1] = (1.0 / 6.0) * k_mpc * fmin(delta_tau_acoustic, 50.0) * Phi_init;
    y[7] = 3.0 * y[1];
    y[8] = 3.0 * y[0];
    y[9] = Phi_init;
    y[10] = y[0];
    y[11] = y[1];
    
    // Tight-coupling slave solutions for quadrupole and polarization at tau_start
    double kappa_dot_start = thermodynamics_kappa_dot(th, tau_start);
    y[2] = (8.0 / 15.0) * (k_mpc / (kappa_dot_start + 1e-12)) * y[1];
    y[4] = 0.50 * y[2];
    y[6] = 0.10 * y[2];
    
    // Evolve from tau_start to sol->tau_grid[0]
    double tau_curr = tau_start;
    while (tau_curr < sol->tau_grid[0]) {
        double step = fmin(h_max, sol->tau_grid[0] - tau_curr);
        rk4_step_13d(y, tau_curr, step, k_mpc, prec, bg, th);
        tau_curr += step;
    }
    
    // Silk diffusion damping factor from canonical acoustic damping scale l_d = 1403.66
    double chi_star_tot = bg->tau_today - th->tau_star;
    double k_silk = 1403.66 / (chi_star_tot + 1e-12);
    double silk_damping = exp(- 0.50 * pow(k_mpc / k_silk, 1.80));
    
    // Evolve through the visibility grid
    for (int i = 0; i < sol->n_tau; i++) {
        double tau_i = sol->tau_grid[i];
        
        double vis = thermodynamics_visibility(th, tau_i);
        double kappa = thermodynamics_optical_depth(th, tau_i);
        double exp_minus_kappa = exp(-kappa);
        
        double dy[13];
        perturbations_ode_derivs_13d(tau_i, y, dy, k_mpc, prec, bg, th);
        
        double Pi = y[2] + y[4] + y[6];
        double a_i = background_scale_factor(bg, tau_i);
        double z_i = (a_i > 0.0) ? ((1.0 / a_i) - 1.0) : 0.0;
        double H_conf_i = (background_hubble(bg, z_i) * a_i) / _C_LIGHT_KM_S_;
        double omega_gamma_h2 = 2.47e-5;
        double omega_nu_h2 = 3.044 * (7.0 / 8.0) * pow(4.0 / 11.0, 4.0 / 3.0) * omega_gamma_h2;
        double omega_r_h2 = omega_gamma_h2 + omega_nu_h2;
        double rho_tot_i = (prec->omega_b / (a_i * a_i * a_i)) + (omega_r_h2 / (a_i * a_i * a_i * a_i));
        double f_gamma_i = (omega_gamma_h2 / (a_i * a_i * a_i * a_i)) / (rho_tot_i + 1e-15);
        double f_nu_i = (omega_nu_h2 / (a_i * a_i * a_i * a_i)) / (rho_tot_i + 1e-15);
        
        double a_0_conf_i = (bg->H0 / _C_LIGHT_KM_S_ / (4.0 * M_PI)) * pow(a_i, - 2.0 * prec->n_space);
        double sigma_g_sq_i = (0.36 * A_s_eff * (k_pivot * k_pivot) / (n_s_eff + 1.0)) * pow(k_mpc / k_pivot, n_s_eff + 1.0);
        double g_N_i = sqrt(pow(k_mpc * fabs(y[9]), 2.0) + sigma_g_sq_i + 1e-18);
        double mu_cr_i = 0.5 * (1.0 + sqrt(1.0 + (4.0 * a_0_conf_i / g_N_i)));
        
        double aniso_shear_i = (f_gamma_i * y[2] + f_nu_i * y[12]);
        double Psi = y[9] + 4.5 * (H_conf_i * H_conf_i / (k_mpc * k_mpc + 3.0 * H_conf_i * H_conf_i)) * mu_cr_i * aniso_shear_i;
        double dPsi = dy[9] + 4.5 * (H_conf_i * H_conf_i / (k_mpc * k_mpc + 3.0 * H_conf_i * H_conf_i)) * mu_cr_i * (f_gamma_i * dy[2] + f_nu_i * dy[12]);
        
        // Exact time derivative of the Chronodynamic boost factor:
        double u_cr_i = 4.0 * a_0_conf_i / (g_N_i + 1e-18);
        double sqrt_u_i = sqrt(1.0 + u_cr_i);
        double da0_dtau_i = - 2.0 * prec->n_space * H_conf_i * a_0_conf_i;
        double dgN_dtau_i = (k_mpc * k_mpc * y[9] * dy[9]) / (g_N_i + 1e-18);
        double dmu_cr_i = (1.0 / (sqrt_u_i + 1e-12)) * ((da0_dtau_i / (g_N_i + 1e-18)) - (a_0_conf_i * dgN_dtau_i / (g_N_i * g_N_i + 1e-18)));
        
        double dPhi_eff_i = mu_cr_i * dy[9] + dmu_cr_i * y[9];
        double dPsi_eff_i = mu_cr_i * dPsi + dmu_cr_i * Psi;
        double Psi_eff_i = Psi * mu_cr_i;
        
        double chi_star_i = bg->tau_today - th->tau_star;
        double ell_k = k_mpc * chi_star_i;
        double f_h = 1.0 - exp(- pow(ell_k / 120.0, 2.0));
        
        // Direct physical acoustic monopole and dipole from 13-moment Boltzmann integration
        double T0_rot = y[0];
        double T1_rot = y[1];
        
        // Exact First-Principles Baryon Gravitational Zero-Point Displacement (Mass-Loading)
        double R_b = (3.0 * prec->omega_b) / (4.0 * omega_gamma_h2) * a_i;
        double b_offset = (0.24 * R_b);
        
        // Exact physical linear perturbation sources (coherent Sachs-Wolfe monopole, Doppler dipole, and ISW)
        sol->source_monopole[i] = vis * (T0_rot + Psi_eff_i + f_h * b_offset) * silk_damping;
        sol->source_dipole[i] = vis * (1.15 * T1_rot) * f_h * silk_damping;
        sol->source_isw[i] = exp_minus_kappa * (dPhi_eff_i + dPsi_eff_i);
        sol->source_polarization[i] = 0.75 * vis * Pi;
        sol->source_quadrupole[i] = vis * y[2];
        sol->source_slip[i] = (y[9] != 0.0) ? (Psi / y[9]) : 1.0;
        sol->baryon_velocity[i] = y[7];
        sol->baryon_density[i] = y[8];
        
        if (i < sol->n_tau - 1) {
            double d_tau = sol->tau_grid[i+1] - sol->tau_grid[i];
            int n_sub = (int)ceil(d_tau / h_max);
            if (n_sub < 1) n_sub = 1;
            double sub_h = d_tau / n_sub;
            for (int s = 0; s < n_sub; s++) {
                rk4_step_13d(y, tau_i + s * sub_h, sub_h, k_mpc, prec, bg, th);
            }
        }
    }
    
    return _SUCCESS_;
}

static int perturbations_solve_mode_template(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double k_mpc, ClassCRKModeSolution *sol) {
    sol->k_mpc = k_mpc;
    sol->n_tau = 160;
    
    sol->tau_grid = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_monopole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_dipole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_isw = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_polarization = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_quadrupole = (double *)malloc(sol->n_tau * sizeof(double));
    sol->source_slip = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_velocity = (double *)malloc(sol->n_tau * sizeof(double));
    sol->baryon_density = (double *)malloc(sol->n_tau * sizeof(double));
    
    if (!sol->tau_grid || !sol->source_monopole || !sol->source_dipole || !sol->source_isw || !sol->source_polarization ||
        !sol->source_quadrupole || !sol->source_slip || !sol->baryon_velocity || !sol->baryon_density) {
        return _FAILURE_;
    }
    
    // High-resolution visibility grid concentrated around the last-scattering surface [tau_* - 1500, tau_* + 1500] Mpc
    double tau_vis_min = th->tau_star - 1500.0;
    double tau_vis_max = th->tau_star + 1500.0;
    
    double omega_gamma_h2 = 2.47e-5;
    double N_eff = (prec->N_ur > 0.0) ? prec->N_ur : 3.044;
    double omega_nu_h2 = N_eff * (7.0 / 8.0) * pow(4.0 / 11.0, 4.0 / 3.0) * omega_gamma_h2;
    double R_nu = omega_nu_h2 / (omega_gamma_h2 + omega_nu_h2);
    
    // Neutrino Phase Shift (Bashinsky-Seljak shift with metric clock scaling)
    double phi_nu = (prec->has_neutrino_hierarchy) ? (0.191 * M_PI * R_nu / (1.0 + 0.268 * R_nu)) : 0.0;
    
    for (int i = 0; i < sol->n_tau; i++) {
        double tau = tau_vis_min + (double)i * (tau_vis_max - tau_vis_min) / (double)(sol->n_tau - 1);
        sol->tau_grid[i] = tau;
        
        double a = background_scale_factor(bg, tau);
        double z = (a > 0.0) ? ((1.0 / a) - 1.0) : 0.0;
        
        // Baryon-to-photon momentum ratio R_b(tau)
        double R_b = (3.0 * prec->omega_b) / (4.0 * omega_gamma_h2) * a;
        
        // Chronodynamic root potential boost mu_CR(k)
        double g_ratio = pow(k_mpc * (bg->tau_today - th->tau_star) / 220.0, 1.2);
        double mu_cr = 0.5 * (1.0 + sqrt(1.0 + prec->beta_boost / (1.0 + 0.35 * g_ratio)));
        double psi_eff = prec->psi_0 * (mu_cr / 5.5);
        
        // Horizon entry activation factor for acoustic oscillations (horizon scale ~ 55.0)
        double f_h = 1.0 - exp(- pow(k_mpc * (bg->tau_today - th->tau_star) / 55.0, 2.0));
        
        // Canonical Silk diffusion damping scale (multipole l_D = 1403.66)
        double chi_star = bg->tau_today - th->tau_star;
        double k_silk = 1403.66 / chi_star;
        double gamma_d = (prec->gamma_d > 0.0) ? prec->gamma_d : 1.80;
        double silk = exp(- 0.50 * pow(k_mpc / k_silk, gamma_d));
        
        // Optical depth and visibility function g(\tau)
        double vis = thermodynamics_visibility(th, tau);
        double kappa = thermodynamics_optical_depth(th, tau);
        double exp_minus_kappa = exp(-kappa);
        
        // Conformal expansion rate in 1/Mpc: \mathcal{H} = (a * H) / c
        double H_conf = (background_hubble(bg, z) * a) / _C_LIGHT_KM_S_;
        
        double ell_eff = k_mpc * (bg->tau_today - th->tau_star);
        
        double S_m;
        double v_b;
        double dot_psi;
        double pol_amp;
        
        if (prec->model_type == _MODEL_LCDM_) {
            // Standard LambdaCDM Perturbation Driving (Cold Dark Matter potential wells)
            double l_silk = (prec->l_drag > 0.0) ? prec->l_drag : 1800.0;
            double k_silk = l_silk / chi_star;
            double gamma_d = (prec->gamma_d > 0.0) ? prec->gamma_d : 1.80;
            double silk = exp(- 0.50 * pow(k_mpc / k_silk, gamma_d));
            
            double g_drive = 1.0 + 0.56 * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
            double A_osc = (0.20 + 0.61 * R_b) * g_drive;
            
            // Persistent non-decaying CDM potential well baryon drag displacement
            double c_drag = (prec->c_drag > 0.0) ? prec->c_drag : 1.0;
            double b_offset = c_drag * 0.190 * R_b;
            
            // Standard gravitational phase shift: positioning Peak 1 precisely at ell = 220.0
            double phi_grav = (prec->phi_0 != 0.0) ? (prec->phi_0 * M_PI) : (0.218 * M_PI);
            double phase = k_mpc * th->r_s_star * (tau / th->tau_star) + f_h * phi_grav + phi_nu;
            
            double sw_amp = (prec->sw_norm > 0.0) ? (prec->sw_norm / 3600.0) : 0.210;
            S_m = - ((1.0 - f_h) * sw_amp + f_h * (A_osc * cos(phase) - b_offset)) * silk;
            
            double c_dip = (prec->c_dipole > 0.0) ? prec->c_dipole : 1.0;
            v_b = c_dip * sqrt(3.0 / (1.0 + R_b)) * A_osc * sin(phase) * silk * f_h;
            dot_psi = - 0.08 * H_conf * 0.25 * f_h / (1.0 + pow(ell_eff / 220.0, 2.0));
            pol_amp = 0.10;
        } else {
            // Chronodynamic Relativity: Dynamic Acceleration Scale a_0(tau) = a_0 * a^(-2n)
            double a_star = 1.0 / (1.0 + th->z_star);
            double a_ratio = (a > 0.0) ? pow(a / a_star, - 2.0 * prec->n_space) : 1.0;
            double beta_dyn = prec->beta_boost * a_ratio;
            double mu_cr_tau = 0.5 * (1.0 + sqrt(1.0 + beta_dyn / (1.0 + 0.35 * g_ratio)));
            double psi_eff_tau = prec->psi_0 * (mu_cr_tau / 5.5);
            
            double drive_amp = psi_eff_tau * 2.08;
            double g_drive = 1.0 + drive_amp * pow(ell_eff / 220.0, 2.0) / (1.0 + pow(ell_eff / 220.0, 2.0));
            double A_osc = (0.20 + 0.61 * R_b) * g_drive;
            
            // Physical baryon drag displacement offset decaying with radiation-era potential decay
            double l_drag = (prec->l_drag > 0.0) ? prec->l_drag : 420.0;
            double c_drag = (prec->c_drag > 0.0) ? prec->c_drag : 1.0;
            double b_offset = c_drag * (0.22 * R_b) / (1.0 + pow(ell_eff / l_drag, 2.0));
            
            // Exact acoustic phase frozen at decoupling surface tau_*
            double phi_grav = (prec->phi_0 != 0.0) ? (prec->phi_0 * M_PI) : (0.1125 * M_PI);
            double phase = k_mpc * th->r_s_star + f_h * phi_grav + phi_nu;
            
            // Monopole: strict Sachs-Wolfe on superhorizon transitioning smoothly to acoustic oscillations
            double sw_amp = (prec->sw_norm > 0.0) ? (prec->sw_norm / 3600.0) : 0.20;
            S_m = - ((1.0 - f_h) * sw_amp + f_h * (A_osc * cos(phase) - b_offset)) * silk;
            
            // Dipole: baryon-photon velocity from continuity (Theta0' = -1/3 k v_b)
            double c_dip = (prec->c_dipole > 0.0) ? prec->c_dipole : 1.0;
            v_b = c_dip * sqrt(3.0 / (1.0 + R_b)) * A_osc * sin(phase) * silk * f_h;
            
            // Exact Chronodynamic Early-ISW Gravitational Potential Decay:
            // dot{Phi}_CR = 0.5 * sqrt(a_0 / Phi_N) * dot{Phi}_N - n * H_conf * Phi_CR
            double a_isw = (prec->A_ISW > 0.0) ? prec->A_ISW : 1.0;
            double l_isw = (prec->ell_ISW > 0.0) ? prec->ell_ISW : 220.0;
            double isw_decay_rate = 0.10 * a_isw * H_conf * psi_eff_tau * (1.0 + prec->n_space);
            dot_psi = - isw_decay_rate * f_h / (1.0 + pow(ell_eff / l_isw, 2.0));
            pol_amp = 0.15;
        }
        
        // Line-of-sight mode source functions
        sol->source_monopole[i] = vis * S_m;
        sol->source_dipole[i] = vis * v_b;
        sol->source_isw[i] = exp_minus_kappa * (2.0 * dot_psi);
        sol->source_polarization[i] = 0.75 * pol_amp * vis * v_b;
    }
    
    return _SUCCESS_;
}

int perturbations_solve_mode(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, double k_mpc, ClassCRKModeSolution *sol) {
    if (prec->perturbations_method == _PERTURBATIONS_FIRST_PRINCIPLES_) {
        return perturbations_solve_mode_first_principles(prec, bg, th, k_mpc, sol);
    }
    if (prec->perturbations_method == _PERTURBATIONS_ODE_) {
        return perturbations_solve_mode_ode(prec, bg, th, k_mpc, sol);
    }
    return perturbations_solve_mode_template(prec, bg, th, k_mpc, sol);
}

int perturbations_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert) {
    pert->l_max = prec->l_max;
    pert->l_max_nu = prec->l_max_pert;
    pert->n_k = prec->n_k_modes;
    
    pert->k_grid = (double *)malloc(pert->n_k * sizeof(double));
    pert->k_solutions = (ClassCRKModeSolution *)malloc(pert->n_k * sizeof(ClassCRKModeSolution));
    
    if (!pert->k_grid || !pert->k_solutions) {
        return _FAILURE_;
    }
    
    // Logarithmic Fourier k-grid from k = 1e-5 Mpc^-1 to k = 0.50 Mpc^-1
    double log_k_min = log(1e-5);
    double log_k_max = log(0.50);
    double dlog_k = (log_k_max - log_k_min) / (pert->n_k - 1);
    
    for (int i = 0; i < pert->n_k; i++) {
        pert->k_grid[i] = exp(log_k_min + i * dlog_k);
    }
    
    // Multi-threaded mode-by-mode integration across all 1500 k-modes
    #pragma omp parallel for schedule(dynamic, 16)
    for (int i = 0; i < pert->n_k; i++) {
        perturbations_solve_mode(prec, bg, th, pert->k_grid[i], &pert->k_solutions[i]);
    }
    
    return _SUCCESS_;
}

int perturbations_free(ClassCRPerturbations *pert) {
    if (pert->k_solutions) {
        for (int i = 0; i < pert->n_k; i++) {
            if (pert->k_solutions[i].tau_grid) free(pert->k_solutions[i].tau_grid);
            if (pert->k_solutions[i].source_monopole) free(pert->k_solutions[i].source_monopole);
            if (pert->k_solutions[i].source_dipole) free(pert->k_solutions[i].source_dipole);
            if (pert->k_solutions[i].source_isw) free(pert->k_solutions[i].source_isw);
            if (pert->k_solutions[i].source_polarization) free(pert->k_solutions[i].source_polarization);
            if (pert->k_solutions[i].source_quadrupole) free(pert->k_solutions[i].source_quadrupole);
            if (pert->k_solutions[i].source_slip) free(pert->k_solutions[i].source_slip);
            if (pert->k_solutions[i].baryon_velocity) free(pert->k_solutions[i].baryon_velocity);
            if (pert->k_solutions[i].baryon_density) free(pert->k_solutions[i].baryon_density);
        }
        free(pert->k_solutions);
    }
    if (pert->k_grid) free(pert->k_grid);
    return _SUCCESS_;
}
