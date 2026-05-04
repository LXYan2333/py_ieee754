/* Trigonometric function wrappers from <math.h>: sin, cos, tan, asin, acos,
 * atan, atan2. */

#include "_math_common.h"
#include <math.h>

WRAP_1D(sin)
WRAP_1F(sin)
WRAP_1D(cos)
WRAP_1F(cos)
WRAP_1D(tan)
WRAP_1F(tan)
WRAP_1D(asin)
WRAP_1F(asin)
WRAP_1D(acos)
WRAP_1F(acos)
WRAP_1D(atan)
WRAP_1F(atan)
WRAP_2D(atan2)
WRAP_2F(atan2)
