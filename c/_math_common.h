/* Shared macros for math.h function wrappers.
 *
 * Each wrapper follows the FP-safe pattern:
 *   save round → set round (if rnd >= 0) → clear except → compute →
 *   test except → clear except → restore round
 *
 * The rnd parameter: -1 means "don't change rounding".
 */

#ifndef PY_IEEE754_MATH_COMMON_H
#define PY_IEEE754_MATH_COMMON_H

#include <fenv.h>

#ifdef _MSC_VER
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#define ARITH_BEGIN                                                            \
  int _saved = fegetround();                                                   \
  if (rnd >= 0)                                                                \
    fesetround(rnd);                                                           \
  feclearexcept(FE_ALL_EXCEPT)
#define ARITH_END                                                              \
  *except = fetestexcept(FE_ALL_EXCEPT);                                       \
  feclearexcept(FE_ALL_EXCEPT);                                                \
  fesetround(_saved)

/* 1-arg: void → float/double output */
#define WRAP_1D(name)                                                          \
  DLL_EXPORT void py_ieee754_##name(double x, double *output, int rnd,         \
                                    int *except) {                             \
    ARITH_BEGIN;                                                               \
    *output = name(x);                                                         \
    ARITH_END;                                                                 \
  }

#define WRAP_1F(name)                                                          \
  DLL_EXPORT void py_ieee754_##name##f(float x, float *output, int rnd,        \
                                       int *except) {                          \
    ARITH_BEGIN;                                                               \
    *output = name##f(x);                                                      \
    ARITH_END;                                                                 \
  }

/* 2-arg: void → float/double output */
#define WRAP_2D(name)                                                          \
  DLL_EXPORT void py_ieee754_##name(double x, double y, double *output,        \
                                    int rnd, int *except) {                    \
    ARITH_BEGIN;                                                               \
    *output = name(x, y);                                                      \
    ARITH_END;                                                                 \
  }

#define WRAP_2F(name)                                                          \
  DLL_EXPORT void py_ieee754_##name##f(float x, float y, float *output,        \
                                       int rnd, int *except) {                 \
    ARITH_BEGIN;                                                               \
    *output = name##f(x, y);                                                   \
    ARITH_END;                                                                 \
  }

/* 3-arg: void → float/double output (for fma) */
#define WRAP_3D(name)                                                          \
  DLL_EXPORT void py_ieee754_##name(double x, double y, double z,              \
                                    double *output, int rnd, int *except) {    \
    ARITH_BEGIN;                                                               \
    *output = name(x, y, z);                                                   \
    ARITH_END;                                                                 \
  }

#define WRAP_3F(name)                                                          \
  DLL_EXPORT void py_ieee754_##name##f(float x, float y, float z,              \
                                       float *output, int rnd, int *except) {  \
    ARITH_BEGIN;                                                               \
    *output = name##f(x, y, z);                                                \
    ARITH_END;                                                                 \
  }

/* 1-arg: void → long / long long output */
#define WRAP_1D_L(name)                                                        \
  DLL_EXPORT void py_ieee754_##name(double x, long *output, int rnd,           \
                                    int *except) {                             \
    ARITH_BEGIN;                                                               \
    *output = name(x);                                                         \
    ARITH_END;                                                                 \
  }

#define WRAP_1F_L(name)                                                        \
  DLL_EXPORT void py_ieee754_##name##f(float x, long *output, int rnd,         \
                                       int *except) {                          \
    ARITH_BEGIN;                                                               \
    *output = name##f(x);                                                      \
    ARITH_END;                                                                 \
  }

#define WRAP_1D_LL(name)                                                       \
  DLL_EXPORT void py_ieee754_##name(double x, long long *output, int rnd,      \
                                    int *except) {                             \
    ARITH_BEGIN;                                                               \
    *output = name(x);                                                         \
    ARITH_END;                                                                 \
  }

#define WRAP_1F_LL(name)                                                       \
  DLL_EXPORT void py_ieee754_##name##f(float x, long long *output, int rnd,    \
                                       int *except) {                          \
    ARITH_BEGIN;                                                               \
    *output = name##f(x);                                                      \
    ARITH_END;                                                                 \
  }

/* 1-arg: void → int output (ilogb) */
#define WRAP_1D_I(name)                                                        \
  DLL_EXPORT void py_ieee754_##name(double x, int *output, int rnd,            \
                                    int *except) {                             \
    ARITH_BEGIN;                                                               \
    *output = name(x);                                                         \
    ARITH_END;                                                                 \
  }

#define WRAP_1F_I(name)                                                        \
  DLL_EXPORT void py_ieee754_##name##f(float x, int *output, int rnd,          \
                                       int *except) {                          \
    ARITH_BEGIN;                                                               \
    *output = name##f(x);                                                      \
    ARITH_END;                                                                 \
  }

/* 1-arg double/float + int → double/float output (ldexp, scalbn) */
#define WRAP_DI_D(name)                                                        \
  DLL_EXPORT void py_ieee754_##name(double x, int n, double *output, int rnd,  \
                                    int *except) {                             \
    ARITH_BEGIN;                                                               \
    *output = name(x, n);                                                      \
    ARITH_END;                                                                 \
  }

#define WRAP_FI_F(name)                                                        \
  DLL_EXPORT void py_ieee754_##name##f(float x, int n, float *output, int rnd, \
                                       int *except) {                          \
    ARITH_BEGIN;                                                               \
    *output = name##f(x, n);                                                   \
    ARITH_END;                                                                 \
  }

#endif /* PY_IEEE754_MATH_COMMON_H */
