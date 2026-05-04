/* Nearest integer function wrappers from <math.h>: ceil, floor, trunc, round,
 * nearbyint, rint, lround, llround, lrint, llrint. */

#include "_math_common.h"
#include <math.h>

WRAP_1D(ceil)
WRAP_1F(ceil)
WRAP_1D(floor)
WRAP_1F(floor)
WRAP_1D(trunc)
WRAP_1F(trunc)
WRAP_1D(round)
WRAP_1F(round)
WRAP_1D(nearbyint)
WRAP_1F(nearbyint)
WRAP_1D(rint)
WRAP_1F(rint)
WRAP_1D_L(lround)
WRAP_1F_L(lround)
WRAP_1D_LL(llround)
WRAP_1F_LL(llround)
WRAP_1D_L(lrint)
WRAP_1F_L(lrint)
WRAP_1D_LL(llrint)
WRAP_1F_LL(llrint)
