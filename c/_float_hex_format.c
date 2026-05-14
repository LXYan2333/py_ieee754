#include "_math_common.h"
#include <stdio.h>

DLL_EXPORT int py_ieee754_float_hex_d(double x, char *buf, int buf_size) {
  return snprintf(buf, buf_size, "%a", x);
}

DLL_EXPORT int py_ieee754_float_hex_f(float x, char *buf, int buf_size) {
  return snprintf(buf, buf_size, "%a", (double)x);
}
