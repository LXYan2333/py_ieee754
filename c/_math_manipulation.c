/* Floating-point manipulation function wrappers from <math.h>: frexp, ldexp,
 * modf, scalbn, ilogb, logb, nextafter, copysign. */

#include "_math_common.h"
#include <math.h>

/* frexp: extra int *exp output */
DLL_EXPORT void py_ieee754_frexp(double x, double *output, int *exp_out,
                                 int rnd, int *except) {
  ARITH_BEGIN;
  *output = frexp(x, exp_out);
  ARITH_END;
}

DLL_EXPORT void py_ieee754_frexpf(float x, float *output, int *exp_out, int rnd,
                                  int *except) {
  ARITH_BEGIN;
  *output = frexpf(x, exp_out);
  ARITH_END;
}

/* modf: extra double/float *intpart output */
DLL_EXPORT void py_ieee754_modf(double x, double *output, double *intpart,
                                int rnd, int *except) {
  ARITH_BEGIN;
  *output = modf(x, intpart);
  ARITH_END;
}

DLL_EXPORT void py_ieee754_modff(float x, float *output, float *intpart,
                                 int rnd, int *except) {
  ARITH_BEGIN;
  *output = modff(x, intpart);
  ARITH_END;
}

WRAP_DI_D(ldexp)
WRAP_FI_F(ldexp)
WRAP_DI_D(scalbn)
WRAP_FI_F(scalbn)
WRAP_1D_I(ilogb)
WRAP_1F_I(ilogb)
WRAP_1D(logb)
WRAP_1F(logb)
WRAP_2D(nextafter)
WRAP_2F(nextafter)
WRAP_2D(copysign)
WRAP_2F(copysign)
