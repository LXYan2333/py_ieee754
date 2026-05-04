/* Error and gamma function wrappers from <math.h>: erf, erfc, tgamma, lgamma.
 */

#include "_math_common.h"
#include <math.h>

WRAP_1D(erf)
WRAP_1F(erf)
WRAP_1D(erfc)
WRAP_1F(erfc)
WRAP_1D(tgamma)
WRAP_1F(tgamma)
WRAP_1D(lgamma)
WRAP_1F(lgamma)
