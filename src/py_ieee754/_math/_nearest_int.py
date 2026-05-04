"""Nearest integer functions from <math.h>: ceil, floor, trunc, round_, nearbyint, rint,
lround, llround, lrint, llrint."""

from __future__ import annotations

import ctypes as ct

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import bind_1d, bind_1f, bind_d_l, bind_d_ll, bind_f_l, bind_f_ll


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_ceil = bind_1d("ceil")
_ceilf = bind_1f("ceil")
_floor = bind_1d("floor")
_floorf = bind_1f("floor")
_trunc = bind_1d("trunc")
_truncf = bind_1f("trunc")
_round_c = bind_1d("round")
_roundf = bind_1f("round")
_nearbyint = bind_1d("nearbyint")
_nearbyintf = bind_1f("nearbyint")
_rint = bind_1d("rint")
_rintf = bind_1f("rint")
_lround = bind_d_l("lround")
_lroundf = bind_f_l("lround")
_llround = bind_d_ll("llround")
_llroundf = bind_f_ll("llround")
_lrint = bind_d_l("lrint")
_lrintf = bind_f_l("lrint")
_llrint = bind_d_ll("llrint")
_llrintf = bind_f_ll("llrint")


def ceil[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _ceilf(x, rnd)
    else:
        result, excepts = _ceil(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def floor[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _floorf(x, rnd)
    else:
        result, excepts = _floor(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def trunc[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _truncf(x, rnd)
    else:
        result, excepts = _trunc(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def round_[T: (ct.c_float, ct.c_double)](  # noqa: A001
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _roundf(x, rnd)
    else:
        result, excepts = _round_c(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def nearbyint[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _nearbyintf(x, rnd)
    else:
        result, excepts = _nearbyint(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def rint[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _rintf(x, rnd)
    else:
        result, excepts = _rint(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def lround[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_long:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _lroundf(x, rnd)
    else:
        result, excepts = _lround(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def llround[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_longlong:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _llroundf(x, rnd)
    else:
        result, excepts = _llround(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def lrint[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_long:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _lrintf(x, rnd)
    else:
        result, excepts = _lrint(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


def llrint[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_longlong:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _llrintf(x, rnd)
    else:
        result, excepts = _llrint(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result
