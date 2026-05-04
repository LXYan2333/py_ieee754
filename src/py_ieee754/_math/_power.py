"""Power functions from <math.h>: pow, sqrt, cbrt, hypot."""

from __future__ import annotations

import ctypes as ct
from typing import overload

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f, bind_2d, bind_2f


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_pow = bind_2d("pow")
_powf = bind_2f("pow")
_sqrt = bind_1d("sqrt")
_sqrtf = bind_1f("sqrt")
_cbrt = bind_1d("cbrt")
_cbrtf = bind_1f("cbrt")
_hypot = bind_2d("hypot")
_hypotf = bind_2f("hypot")


@overload
def pow_(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def pow_(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def pow_[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _powf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _pow(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


def sqrt[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _sqrtf(x, rnd)
    else:
        result, excepts = _sqrt(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def cbrt[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _cbrtf(x, rnd)
    else:
        result, excepts = _cbrt(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def hypot(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_float: ...
@overload
def hypot(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatExceptionError]] = ...,
) -> ct.c_double: ...
def hypot[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _hypotf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _hypot(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result
