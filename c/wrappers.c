/* Wrappers for <math.h> and <fenv.h> macros that cannot be called directly via
 * ctypes. */

#ifdef _MSC_VER
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#include <fenv.h>

/* ---- fenv.h: exception flag macros ---- */

DLL_EXPORT int py_ieee754_get_FE_DIVBYZERO(void) { return FE_DIVBYZERO; }
DLL_EXPORT int py_ieee754_get_FE_OVERFLOW(void) { return FE_OVERFLOW; }
DLL_EXPORT int py_ieee754_get_FE_UNDERFLOW(void) { return FE_UNDERFLOW; }
DLL_EXPORT int py_ieee754_get_FE_INEXACT(void) { return FE_INEXACT; }
DLL_EXPORT int py_ieee754_get_FE_INVALID(void) { return FE_INVALID; }

/* ---- fenv.h: rounding direction macros ---- */

DLL_EXPORT int py_ieee754_get_FE_TONEAREST(void) { return FE_TONEAREST; }
DLL_EXPORT int py_ieee754_get_FE_DOWNWARD(void) { return FE_DOWNWARD; }
DLL_EXPORT int py_ieee754_get_FE_UPWARD(void) { return FE_UPWARD; }
DLL_EXPORT int py_ieee754_get_FE_TOWARDZERO(void) { return FE_TOWARDZERO; }

/* ---- Arithmetic operators (FP-safe: save round, clear except, compute, test,
 * restore) ---- */

#define ARITH_BEGIN                                                            \
  int _saved = fegetround();                                                   \
  if (rnd >= 0)                                                                \
    fesetround(rnd);                                                           \
  feclearexcept(FE_ALL_EXCEPT)

#define ARITH_END                                                              \
  *except = fetestexcept(FE_ALL_EXCEPT);                                       \
  feclearexcept(FE_ALL_EXCEPT);                                                \
  fesetround(_saved)

#define ARITH_BIN_D(name, op)                                                  \
  DLL_EXPORT void py_ieee754_##name(double a, double b, double *output,        \
                                    int rnd, int *except) {                    \
    ARITH_BEGIN;                                                               \
    *output = a op b;                                                          \
    ARITH_END;                                                                 \
  }

#define ARITH_BIN_F(name, op)                                                  \
  DLL_EXPORT void py_ieee754_##name##f(float a, float b, float *output,        \
                                       int rnd, int *except) {                 \
    ARITH_BEGIN;                                                               \
    *output = a op b;                                                          \
    ARITH_END;                                                                 \
  }

ARITH_BIN_D(add, +)
ARITH_BIN_F(add, +)
ARITH_BIN_D(sub, -)
ARITH_BIN_F(sub, -)
ARITH_BIN_D(mul, *)
ARITH_BIN_F(mul, *)
ARITH_BIN_D(div, /)
ARITH_BIN_F(div, /)