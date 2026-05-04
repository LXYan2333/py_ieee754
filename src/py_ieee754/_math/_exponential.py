"""Exponential functions from <math.h>: exp, exp2, expm1, log, log10, log2, log1p."""

from __future__ import annotations

import ctypes as ct

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_exp = bind_1d("exp")
_expf = bind_1f("exp")
_exp2 = bind_1d("exp2")
_exp2f = bind_1f("exp2")
_expm1 = bind_1d("expm1")
_expm1f = bind_1f("expm1")
_log = bind_1d("log")
_logf = bind_1f("log")
_log10 = bind_1d("log10")
_log10f = bind_1f("log10")
_log2 = bind_1d("log2")
_log2f = bind_1f("log2")
_log1p = bind_1d("log1p")
_log1pf = bind_1f("log1p")


def exp[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _expf(x, rnd)
    else:
        result, excepts = _exp(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def exp2[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _exp2f(x, rnd)
    else:
        result, excepts = _exp2(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def expm1[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _expm1f(x, rnd)
    else:
        result, excepts = _expm1(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def log[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _logf(x, rnd)
    else:
        result, excepts = _log(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def log10[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _log10f(x, rnd)
    else:
        result, excepts = _log10(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def log2[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _log2f(x, rnd)
    else:
        result, excepts = _log2(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def log1p[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _log1pf(x, rnd)
    else:
        result, excepts = _log1p(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result
