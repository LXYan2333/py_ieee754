"""Trigonometric functions from <math.h>: sin, cos, tan, asin, acos, atan, atan2."""

from __future__ import annotations

import ctypes as ct
from typing import overload

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f, bind_2d, bind_2f


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_sin = bind_1d("sin")
_sinf = bind_1f("sin")
_cos = bind_1d("cos")
_cosf = bind_1f("cos")
_tan = bind_1d("tan")
_tanf = bind_1f("tan")
_asin = bind_1d("asin")
_asinf = bind_1f("asin")
_acos = bind_1d("acos")
_acosf = bind_1f("acos")
_atan = bind_1d("atan")
_atanf = bind_1f("atan")
_atan2 = bind_2d("atan2")
_atan2f = bind_2f("atan2")


def sin[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _sinf(x, rnd)
    else:
        result, excepts = _sin(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def cos[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _cosf(x, rnd)
    else:
        result, excepts = _cos(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def tan[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _tanf(x, rnd)
    else:
        result, excepts = _tan(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def asin[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _asinf(x, rnd)
    else:
        result, excepts = _asin(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def acos[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _acosf(x, rnd)
    else:
        result, excepts = _acos(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def atan[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _atanf(x, rnd)
    else:
        result, excepts = _atan(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def atan2(
    y: ct.c_float,
    x: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def atan2(
    y: ct.c_double,
    x: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def atan2[T: (ct.c_float, ct.c_double)](
    y: T,
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(y, ct.c_float) and isinstance(x, ct.c_float):
        result, excepts = _atan2f(y, x, rnd)
    elif isinstance(y, ct.c_double) and isinstance(x, ct.c_double):
        result, excepts = _atan2(y, x, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result
