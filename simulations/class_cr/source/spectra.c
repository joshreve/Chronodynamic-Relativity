/**
 * CLASS-CR: Spectra & Line-of-Sight Transfer Module Dispatcher
 * =============================================================
 * Dispatches to either the exact line-of-sight Bessel projection engine
 * (spectra_exact_init) or the fast semi-analytic engine (spectra_fast_init)
 * based on the precision setting prec->transfer_method.
 */

#include "spectra.h"

int spectra_init(ClassCRPrecision *prec, ClassCRBackground *bg, ClassCRThermodynamics *th, ClassCRPerturbations *pert, ClassCRSpectra *sp) {
    printf("DEBUG_SPECTRA: l_max=%d\n", prec->l_max);
    sp->l_max = prec->l_max;
    sp->n_ell = prec->l_max - 1;
    printf("DEBUG_SPECTRA: n_ell=%d\n", sp->n_ell);
    
    sp->ell_list = (int *)malloc(sp->n_ell * sizeof(int));
    sp->cl_tt = (double *)malloc(sp->n_ell * sizeof(double));
    sp->cl_ee = (double *)malloc(sp->n_ell * sizeof(double));
    sp->cl_te = (double *)malloc(sp->n_ell * sizeof(double));
    sp->cl_pp = (double *)malloc(sp->n_ell * sizeof(double));
    sp->dl_tt = (double *)malloc(sp->n_ell * sizeof(double));
    sp->dl_ee = (double *)malloc(sp->n_ell * sizeof(double));
    sp->dl_te = (double *)malloc(sp->n_ell * sizeof(double));
    sp->dl_pp = (double *)malloc(sp->n_ell * sizeof(double));
    
    if (!sp->ell_list || !sp->cl_tt || !sp->cl_ee || !sp->cl_te || !sp->cl_pp ||
        !sp->dl_tt || !sp->dl_ee || !sp->dl_te || !sp->dl_pp) {
        return _FAILURE_;
    }
    
    for (int i = 0; i < sp->n_ell; i++) {
        sp->ell_list[i] = i + 2;
    }
    
    printf("   * Using Exact Line-of-Sight Bessel Integral Solver...\n");
    return spectra_exact_init(prec, bg, th, pert, sp);
}

int spectra_free(ClassCRSpectra *sp) {
    if (sp->ell_list) free(sp->ell_list);
    if (sp->cl_tt) free(sp->cl_tt);
    if (sp->cl_ee) free(sp->cl_ee);
    if (sp->cl_te) free(sp->cl_te);
    if (sp->cl_pp) free(sp->cl_pp);
    if (sp->dl_tt) free(sp->dl_tt);
    if (sp->dl_ee) free(sp->dl_ee);
    if (sp->dl_te) free(sp->dl_te);
    if (sp->dl_pp) free(sp->dl_pp);
    return _SUCCESS_;
}

int spectra_output_to_file(ClassCRSpectra *sp, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) return _FAILURE_;
    
    fprintf(fp, "# CLASS-CR Angular Power Spectra (TT, EE, TE, phiphi)\n");
    fprintf(fp, "# 1:ell  2:C_ell^TT  3:C_ell^EE  4:C_ell^TE  5:C_ell^phiphi  6:D_ell^TT  7:D_ell^EE  8:D_ell^TE  9:[L^2(L+1)^2/2pi]C_L^phiphi\n");
    for (int i = 0; i < sp->n_ell; i++) {
        fprintf(fp, "%6d  %15.6e  %15.6e  %15.6e  %15.6e  %14.5f  %14.5f  %14.5f  %15.6e\n",
            sp->ell_list[i], sp->cl_tt[i], sp->cl_ee[i], sp->cl_te[i], sp->cl_pp[i],
            sp->dl_tt[i], sp->dl_ee[i], sp->dl_te[i], sp->dl_pp[i]);
    }
    
    fclose(fp);
    return _SUCCESS_;
}
