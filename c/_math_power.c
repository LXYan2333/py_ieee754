/* Power function wrappers from <math.h>: pow, sqrt, cbrt, hypot. */

#include "_math_common.h"
#include <math.h>

WRAP_2D(pow)
WRAP_2F(pow)
WRAP_1D(sqrt)
WRAP_1F(sqrt)
WRAP_1D(cbrt)
WRAP_1F(cbrt)
WRAP_2D(hypot)
WRAP_2F(hypot)
