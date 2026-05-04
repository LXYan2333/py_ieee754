"""Basic operations from <math.h>: fabs, fmod, remainder, remquo, fma, fmax, fmin, fdim, nan."""

from __future__ import annotations

import ctypes as ct
from typing import overload

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._math._common import (
    bind_1d,
    bind_1f,
    bind_2d,
    bind_2di_d,
    bind_2f,
    bind_2fi_f,
    bind_3d,
    bind_3f,
    bind_s_d,
    bind_s_f,
)


def _rnd(mode: RoundingMode | None) -> int:
    return -1 if mode is None else int(mode)


_fabs = bind_1d("fabs")
_fabsf = bind_1f("fabs")
_fmod = bind_2d("fmod")
_fmodf = bind_2f("fmod")
_remainder = bind_2d("remainder")
_remainderf = bind_2f("remainder")
_fma = bind_3d("fma")
_fmaf = bind_3f("fma")
_fmax = bind_2d("fmax")
_fmaxf = bind_2f("fmax")
_fmin = bind_2d("fmin")
_fminf = bind_2f("fmin")
_fdim = bind_2d("fdim")
_fdimf = bind_2f("fdim")
_nan = bind_s_d("nan")
_nanf = bind_s_f("nan")

_remquo = bind_2di_d("remquo")
_remquof = bind_2fi_f("remquo")


def fabs[T: (ct.c_float, ct.c_double)](
    x: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float):
        result, excepts = _fabsf(x, rnd)
    else:
        result, excepts = _fabs(x, rnd)
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def fmod(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def fmod(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def fmod[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _fmodf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _fmod(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def remainder(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def remainder(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def remainder[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _remainderf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _remainder(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def remquo(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> tuple[ct.c_float, ct.c_int]: ...
@overload
def remquo(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> tuple[ct.c_double, ct.c_int]: ...
def remquo[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> tuple[ct.c_double | ct.c_float, ct.c_int]:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, quo, excepts = _remquof(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, quo, excepts = _remquo(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result, ct.c_int(quo)


@overload
def fma(
    x: ct.c_float,
    y: ct.c_float,
    z: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def fma(
    x: ct.c_double,
    y: ct.c_double,
    z: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def fma[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    z: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float) and isinstance(z, ct.c_float):
        result, excepts = _fmaf(x, y, z, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double) and isinstance(z, ct.c_double):
        result, excepts = _fma(x, y, z, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def fmax(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def fmax(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def fmax[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _fmaxf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _fmax(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def fmin(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def fmin(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def fmin[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _fminf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _fmin(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


@overload
def fdim(
    x: ct.c_float,
    y: ct.c_float,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_float: ...
@overload
def fdim(
    x: ct.c_double,
    y: ct.c_double,
    *,
    round_mode: RoundingMode | None = ...,
    unsuppressed: set[type[FloatingPointError]] = ...,
) -> ct.c_double: ...
def fdim[T: (ct.c_float, ct.c_double)](
    x: T,
    y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _fdimf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _fdim(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result


def nan(
    tag: str = "",
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_double:
    result, excepts = _nan(ct.c_char_p(tag.encode()), _rnd(round_mode))
    check_exceptions(excepts, unsuppressed)
    return result


def nanf(
    tag: str = "",
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> ct.c_float:
    result, excepts = _nanf(ct.c_char_p(tag.encode()), _rnd(round_mode))
    check_exceptions(excepts, unsuppressed)
    return result
