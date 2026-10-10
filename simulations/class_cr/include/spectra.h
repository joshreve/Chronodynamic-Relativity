/**
 * CLASS-CR: Spectra & Lensing Module Header
 */

#ifndef __SPECTRA_CR_H__
#define __SPECTRA_CR_H__

#include "common.h"
#include "background.h"
#include "thermodynamics.h"
#include "perturbations.h"

typedef struct {
    int l_max;
    int *ell_list;
    int n_ell;
    double *cl_tt;
    double *cl_ee;
    double *cl_te;
    double *cl_pp;
    double *dl_tt;
    double *dl_ee;
    double *dl_te;
    double *dl_pp;
} ClassCRSpectra;

int spectra_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert, ClassCRSpectra *sp);
int spectra_exact_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert, ClassCRSpectra *sp);
int spectra_free(ClassCRSpectra *sp);
int spectra_output_to_file(ClassCRSpectra *sp, const char *filename);

#endif /* __SPECTRA_CR_H__ */
