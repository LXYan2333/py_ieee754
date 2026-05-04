"""Error and gamma functions from <math.h>: erf, erfc, tgamma, lgamma."""

from __future__ import annotations

import ctypes as ct

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_erf = bind_1d("erf")
_erff = bind_1f("erf")
_erfc = bind_1d("erfc")
_erfcf = bind_1f("erfc")
_tgamma = bind_1d("tgamma")
_tgammaf = bind_1f("tgamma")
_lgamma = bind_1d("lgamma")
_lgammaf = bind_1f("lgamma")


def erf[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _erff(x, rnd)
    else:
        result, excepts = _erf(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def erfc[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _erfcf(x, rnd)
    else:
        result, excepts = _erfc(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def tgamma[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _tgammaf(x, rnd)
    else:
        result, excepts = _tgamma(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def lgamma[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _lgammaf(x, rnd)
    else:
        result, excepts = _lgamma(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result
