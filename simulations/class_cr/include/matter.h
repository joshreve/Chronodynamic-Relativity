/**
 * CLASS-CR: Matter Power Spectrum & BAO Module Header
 * ===================================================
 * Computes linear matter power spectrum P(k) and BAO transfer functions
 * linked to the low-redshift DESI sound horizon r_d = 141.42 Mpc.
 */

#ifndef __MATTER_CR_H__
#define __MATTER_CR_H__

#include "common.h"
#include "background.h"
#include "thermodynamics.h"
#include "perturbations.h"

typedef struct {
    int n_k;
    double *k_grid;
    double *pk_linear;
    double *pk_bao_oscillations;
    double *transfer_matter;
    double sigma8;
    double r_d_bao_mpc;
} ClassCRMatter;

int matter_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert, ClassCRMatter *mat);
int matter_free(ClassCRMatter *mat);
int matter_output_to_file(ClassCRMatter *mat, const char *filename);

#endif /* __MATTER_CR_H__ */
