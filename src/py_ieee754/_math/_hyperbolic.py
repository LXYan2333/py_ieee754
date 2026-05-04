"""Hyperbolic functions from <math.h>: sinh, cosh, tanh, asinh, acosh, atanh."""

from __future__ import annotations

import ctypes as ct

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_sinh = bind_1d("sinh")
_sinhf = bind_1f("sinh")
_cosh = bind_1d("cosh")
_coshf = bind_1f("cosh")
_tanh = bind_1d("tanh")
_tanhf = bind_1f("tanh")
_asinh = bind_1d("asinh")
_asinhf = bind_1f("asinh")
_acosh = bind_1d("acosh")
_acoshf = bind_1f("acosh")
_atanh = bind_1d("atanh")
_atanhf = bind_1f("atanh")


def sinh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _sinhf(x, rnd)
    else:
        result, excepts = _sinh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def cosh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _coshf(x, rnd)
    else:
        result, excepts = _cosh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def tanh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _tanhf(x, rnd)
    else:
        result, excepts = _tanh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def asinh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _asinhf(x, rnd)
    else:
        result, excepts = _asinh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def acosh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _acoshf(x, rnd)
    else:
        result, excepts = _acosh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def atanh[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _atanhf(x, rnd)
    else:
        result, excepts = _atanh(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result
