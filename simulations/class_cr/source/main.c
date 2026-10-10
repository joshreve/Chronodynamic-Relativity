/**
 * CLASS-CR: Main CLI Entry Point
 */

#include "common.h"
#include "background.h"
#include "thermodynamics.h"
#include "perturbations.h"
#include "spectra.h"
#include "matter.h"
#include <time.h>

int main(int argc, char **argv) {
    printf("=====================================================================================\n");
    printf("CLASS-CR: Chronodynamic Relativity Boltzmann Hierarchy Fork (C Core Engine)\n");
    printf("=====================================================================================\n");
    
    clock_t t0 = clock();
    
    // Default Precision & Model Parameters
    ClassCRPrecision prec;
    prec.model_type = _MODEL_CR_;
    prec.H0 = 70.50;
    prec.omega_b = 0.02237;
    prec.omega_cdm = 0.0;
    prec.n_space = 0.239;
    prec.A_s = 2.1e-9;
    prec.n_s = 0.9649;
    prec.z_reio = 7.82;
    prec.Y_p = 0.245;
    prec.l_A_0 = 314.8107;
    prec.delta_1 = -0.4991;
    prec.ell_0 = 220.1122;
    prec.alpha_1 = 2.6008;
    prec.phi_0 = 0.1419;
    prec.beta_boost = 101.3375;
    prec.psi_0 = 0.1828;
    prec.A_ISW = 0.6456;
    prec.ell_ISW = 126.8987;
    prec.A_0 = 1761.0404;
    prec.A_base = 3525.9376;
    prec.gamma_d = 2.0821;
    prec.sigma_lens = 82.2065;
    prec.refract_amp = 1.0;
    prec.c_dipole = 1.0;
    prec.l_drag = 420.0;
    prec.c_drag = 1.0;
    prec.sw_norm = 754.7719;
    prec.y_cal = 0.9007;
    prec.A_ps = 79.2382;
    prec.l_max = 2500;
    prec.l_max_pert = 17;
    prec.l_max_hierarchy = 8;
    prec.include_polarization_feedback = 1;
    prec.slip_coupling_scale = 220.0;
    prec.n_k_modes = 1500;
    
    prec.N_ur = 3.044;
    prec.has_neutrino_hierarchy = 1;
    prec.transfer_method = _TRANSFER_EXACT_;
    prec.perturbations_method = _PERTURBATIONS_TEMPLATE_;
    prec.fast_bessel = 0; /* Default: 0 (Full line-of-sight visibility shell integration) */
    
    char root_file[256] = "class_cr_cl.dat";
    
    // Parse .ini file if provided
    const char *ini_path = (argc > 1) ? argv[1] : "cr_planck.ini";
    FILE *f_ini = fopen(ini_path, "r");
    if (f_ini) {
        char line[512];
        while (fgets(line, sizeof(line), f_ini)) {
            char key[128];
            char str_val[128];
            double val;
            if (sscanf(line, " %127[^= ] = %127s", key, str_val) == 2) {
                if (strcmp(key, "transfer_method") == 0) {
                    prec.transfer_method = _TRANSFER_EXACT_;
                } else if (strcmp(key, "perturbations_method") == 0) {
                    if (strcmp(str_val, "first_principles") == 0 || strcmp(str_val, "fp") == 0) prec.perturbations_method = _PERTURBATIONS_FIRST_PRINCIPLES_;
                    else if (strcmp(str_val, "ode") == 0 || strcmp(str_val, "rk4") == 0) prec.perturbations_method = _PERTURBATIONS_ODE_;
                    else prec.perturbations_method = _PERTURBATIONS_TEMPLATE_;
                } else if (strcmp(key, "cosmology") == 0) {
                    if (strcmp(str_val, "lcdm") == 0) prec.model_type = _MODEL_LCDM_;
                    else prec.model_type = _MODEL_CR_;
                } else if (strcmp(key, "root") == 0) {
                    strncpy(root_file, str_val, sizeof(root_file) - 1);
                    root_file[sizeof(root_file) - 1] = '\0';
                } else if (strcmp(key, "fast_bessel") == 0) {
                    if (strcmp(str_val, "yes") == 0 || strcmp(str_val, "1") == 0 || strcmp(str_val, "true") == 0) prec.fast_bessel = 1;
                    else prec.fast_bessel = 0;
                } else if (strcmp(key, "dense_bessel") == 0) {
                    if (strcmp(str_val, "yes") == 0 || strcmp(str_val, "1") == 0 || strcmp(str_val, "true") == 0) prec.dense_bessel = 1;
                    else prec.dense_bessel = 0;
                }
            }
            if (sscanf(line, " %127[^= ] = %lf", key, &val) == 2) {
                if (strcmp(key, "H0") == 0) prec.H0 = val;
                else if (strcmp(key, "omega_b") == 0) prec.omega_b = val;
                else if (strcmp(key, "omega_cdm") == 0) prec.omega_cdm = val;
                else if (strcmp(key, "n_space") == 0) prec.n_space = val;
                else if (strcmp(key, "A_s") == 0) prec.A_s = val;
                else if (strcmp(key, "n_s") == 0) prec.n_s = val;
                else if (strcmp(key, "z_reio") == 0) prec.z_reio = val;
                else if (strcmp(key, "Y_p") == 0) prec.Y_p = val;
                else if (strcmp(key, "N_ur") == 0) prec.N_ur = val;
                else if (strcmp(key, "has_neutrino_hierarchy") == 0) prec.has_neutrino_hierarchy = (int)val;
                else if (strcmp(key, "fast_bessel") == 0) prec.fast_bessel = (int)val;
                else if (strcmp(key, "l_A_0") == 0) prec.l_A_0 = val;
                else if (strcmp(key, "delta_1") == 0) prec.delta_1 = val;
                else if (strcmp(key, "ell_0") == 0) prec.ell_0 = val;
                else if (strcmp(key, "alpha_1") == 0) prec.alpha_1 = val;
                else if (strcmp(key, "phi_0") == 0) prec.phi_0 = val;
                else if (strcmp(key, "beta_boost") == 0) prec.beta_boost = val;
                else if (strcmp(key, "psi_0") == 0) prec.psi_0 = val;
                else if (strcmp(key, "A_ISW") == 0) prec.A_ISW = val;
                else if (strcmp(key, "ell_ISW") == 0) prec.ell_ISW = val;
                else if (strcmp(key, "A_0") == 0) prec.A_0 = val;
                else if (strcmp(key, "A_base") == 0) prec.A_base = val;
                else if (strcmp(key, "gamma_d") == 0) prec.gamma_d = val;
                else if (strcmp(key, "sigma_lens") == 0) prec.sigma_lens = val;
                else if (strcmp(key, "refract_amp") == 0) prec.refract_amp = val;
                else if (strcmp(key, "c_dipole") == 0) prec.c_dipole = val;
                else if (strcmp(key, "l_drag") == 0) prec.l_drag = val;
                else if (strcmp(key, "c_drag") == 0) prec.c_drag = val;
                else if (strcmp(key, "sw_norm") == 0) prec.sw_norm = val;
                else if (strcmp(key, "y_cal") == 0) prec.y_cal = val;
                else if (strcmp(key, "A_ps") == 0) prec.A_ps = val;
                else if (strcmp(key, "l_max_scalars") == 0) prec.l_max = (int)val;
                else if (strcmp(key, "l_max_pert") == 0) prec.l_max_pert = (int)val;
                else if (strcmp(key, "l_max_hierarchy") == 0) prec.l_max_hierarchy = (int)val;
                else if (strcmp(key, "include_polarization_feedback") == 0) prec.include_polarization_feedback = (int)val;
                else if (strcmp(key, "slip_coupling_scale") == 0) prec.slip_coupling_scale = val;
                else if (strcmp(key, "n_k_modes") == 0) prec.n_k_modes = (int)val;
            }
        }
        fclose(f_ini);
        printf("Loaded configuration from: %s (fast_bessel = %d)\n", ini_path, prec.fast_bessel);
    }
    
    // 2. Initialize Background
    printf("1. Initializing Chronodynamic Background Module...\n");
    ClassCRBackground bg;
    if (background_init(&prec, &bg) != _SUCCESS_) {
        fprintf(stderr, "Error initializing background module!\n");
        return 1;
    }
    printf("   * Conformal time today: tau_0 = %.1f Mpc\n", bg.tau_today);
    
    // 3. Initialize Thermodynamics
    printf("2. Initializing Thermodynamics & Recombination Module (RK4 Non-Equilibrium)...\n");
    ClassCRThermodynamics th;
    if (thermodynamics_init(&prec, &bg, &th) != _SUCCESS_) {
        fprintf(stderr, "Error initializing thermodynamics module!\n");
        return 1;
    }
    printf("   * Decoupling peak: z_* = %.2f, tau_* = %.1f Mpc\n", th.z_star, th.tau_star);
    printf("   * Sound horizon at decoupling: r_s = %.2f Mpc\n", th.r_s_star);
    printf("   * Silk diffusion damping scale: r_d = %.2f Mpc\n", th.r_d_star);
    printf("   * Reionization optical depth: tau_reio = %.4f\n", th.tau_reio);
    
    // 4. Initialize Perturbations
    printf("3. Initializing Perturbations Hierarchy (%d Fourier k-modes)...\n", prec.n_k_modes);
    ClassCRPerturbations pert;
    if (perturbations_init(&prec, &bg, &th, &pert) != _SUCCESS_) {
        fprintf(stderr, "Error initializing perturbations module!\n");
        return 1;
    }
    printf("   * Mode-by-mode integration across k in [%.1e, %.2f] Mpc^-1 complete.\n",
        pert.k_grid[0], pert.k_grid[pert.n_k - 1]);
        
    // 5. Compute Spectra & Lensing
    printf("4. Computing Line-of-Sight Angular Power Spectra (TT, EE, TE)...\n");
    ClassCRSpectra sp;
    if (spectra_init(&prec, &bg, &th, &pert, &sp) != _SUCCESS_) {
        fprintf(stderr, "Error initializing spectra module!\n");
        return 1;
    }
    
    spectra_output_to_file(&sp, root_file);
    printf("   * Power spectra output written to: %s\n", root_file);
    
    // 6. Compute Matter Power Spectrum & BAO
    printf("5. Computing Linear Matter Power Spectrum P(k) and BAO Transfers...\n");
    ClassCRMatter mat;
    if (matter_init(&prec, &bg, &th, &pert, &mat) != _SUCCESS_) {
        fprintf(stderr, "Error initializing matter module!\n");
        return 1;
    }
    printf("   * DESI BAO local sound horizon: r_d,local = %.2f Mpc\n", mat.r_d_bao_mpc);
    printf("   * RMS matter variance: sigma_8 = %.4f\n", mat.sigma8);
    
    const char *out_pk_file = "class_cr_pk.dat";
    matter_output_to_file(&mat, out_pk_file);
    printf("   * Matter power spectrum written to: %s\n", out_pk_file);
    
    // Cleanup
    matter_free(&mat);
    spectra_free(&sp);
    perturbations_free(&pert);
    thermodynamics_free(&th);
    background_free(&bg);
    
    double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("=====================================================================================\n");
    printf("CLASS-CR execution completed successfully in %.3f seconds!\n", dt);
    printf("=====================================================================================\n");
    
    return 0;
}
