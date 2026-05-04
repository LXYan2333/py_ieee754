/* Basic operation wrappers from <math.h>: fabs, fmod, remainder, remquo, fma,
 * fmax, fmin, fdim, nan, nanf. */

#include "_math_common.h"
#include <math.h>

WRAP_1D(fabs)
WRAP_1F(fabs)
WRAP_2D(fmod)
WRAP_2F(fmod)
WRAP_2D(remainder)
WRAP_2F(remainder)
WRAP_3D(fma)
WRAP_3F(fma)
WRAP_2D(fmax)
WRAP_2F(fmax)
WRAP_2D(fmin)
WRAP_2F(fmin)
WRAP_2D(fdim)
WRAP_2F(fdim)

/* nan: takes a const char * tag, returns a double NaN. */
DLL_EXPORT
void py_ieee754_nan(const char *tag, double *output, int rnd, int *except) {
  ARITH_BEGIN;
  *output = nan(tag);
  ARITH_END;
}

/* nanf: takes a const char * tag, returns a float NaN. */
DLL_EXPORT void py_ieee754_nanf(const char *tag, float *output, int rnd,
                                int *except) {
  ARITH_BEGIN;
  *output = nanf(tag);
  ARITH_END;
}

/* remquo: extra int *quo output. */
DLL_EXPORT void py_ieee754_remquo(double x, double y, double *output, int *quo,
                                  int rnd, int *except) {
  ARITH_BEGIN;
  *output = remquo(x, y, quo);
  ARITH_END;
}

DLL_EXPORT void py_ieee754_remquof(float x, float y, float *output, int *quo,
                                   int rnd, int *except) {
  ARITH_BEGIN;
  *output = remquof(x, y, quo);
  ARITH_END;
}
