"""Floating-point manipulation functions from <math.h>: frexp, ldexp, modf, scalbn,
ilogb, logb, nextafter, copysign."""

from __future__ import annotations

import ctypes as ct
from typing import overload

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import (
    bind_1d,
    bind_1dd_d,
    bind_1di_d,
    bind_1f,
    bind_1ff_f,
    bind_1fi_f,
    bind_2d,
    bind_2f,
    bind_d_i,
    bind_di_d,
    bind_f_i,
    bind_fi_f,
)


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_frexp = bind_1di_d("frexp")
_frexpf = bind_1fi_f("frexp")
_ldexp = bind_di_d("ldexp")
_ldexpf = bind_fi_f("ldexp")
_modf = bind_1dd_d("modf")
_modff = bind_1ff_f("modf")
_scalbn = bind_di_d("scalbn")
_scalbnf = bind_fi_f("scalbn")
_ilogb = bind_d_i("ilogb")
_ilogbf = bind_f_i("ilogb")
_logb = bind_1d("logb")
_logbf = bind_1f("logb")
_nextafter = bind_2d("nextafter")
_nextafterf = bind_2f("nextafter")
_copysign = bind_2d("copysign")
_copysignf = bind_2f("copysign")


def frexp[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> tuple[ct.c_double | ct.c_float, ct.c_int]:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, exp, excepts = _frexpf(x, rnd)
    else:
        result, exp, excepts = _frexp(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result, ct.c_int(exp)


@overload
def ldexp(
    x: ct.c_float,
    exp: ct.c_int,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def ldexp(
    x: ct.c_double,
    exp: ct.c_int,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def ldexp[T: (ct.c_float, ct.c_double)](
    x: T,
    exp: ct.c_int,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _ldexpf(x, exp, rnd)
    else:
        result, excepts = _ldexp(x, exp, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def modf[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> tuple[ct.c_double | ct.c_float, ct.c_double | ct.c_float]:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, intpart, excepts = _modff(x, rnd)
    else:
        result, intpart, excepts = _modf(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result, intpart


@overload
def scalbn(
    x: ct.c_float,
    n: ct.c_int,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def scalbn(
    x: ct.c_double,
    n: ct.c_int,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def scalbn[T: (ct.c_float, ct.c_double)](
    x: T,
    n: ct.c_int,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _scalbnf(x, n, rnd)
    else:
        result, excepts = _scalbn(x, n, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def ilogb[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_int:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _ilogbf(x, rnd)
    else:
        result, excepts = _ilogb(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def logb[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _logbf(x, rnd)
    else:
        result, excepts = _logb(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def nextafter(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def nextafter(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def nextafter[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _nextafterf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _nextafter(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def copysign(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def copysign(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def copysign[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _copysignf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _copysign(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result
