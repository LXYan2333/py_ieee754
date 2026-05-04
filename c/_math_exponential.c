/* Exponential/logarithmic function wrappers from <math.h>: exp, exp2, expm1,
 * log, log10, log2, log1p. */

#include "_math_common.h"
#include <math.h>

WRAP_1D(exp)
WRAP_1F(exp)
WRAP_1D(exp2)
WRAP_1F(exp2)
WRAP_1D(expm1)
WRAP_1F(expm1)
WRAP_1D(log)
WRAP_1F(log)
WRAP_1D(log10)
WRAP_1F(log10)
WRAP_1D(log2)
WRAP_1F(log2)
WRAP_1D(log1p)
WRAP_1F(log1p)