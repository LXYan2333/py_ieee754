"""Bindings to ``<fenv.h>`` macro values (FE_* flags and rounding directions).

All macro values are fetched at import time from the C wrapper library — no
hard-coded assumptions about platform-specific values.
"""

import ctypes as ct
import enum

from py_ieee754._lib import clib


def _get(name: str) -> int:
    f = clib[f"py_ieee754_get_{name}"]
    f.argtypes = []
    f.restype = ct.c_int
    return f()


FE_DIVBYZERO = _get("FE_DIVBYZERO")
"""C ``FE_DIVBYZERO`` — division by zero exception flag."""

FE_OVERFLOW = _get("FE_OVERFLOW")
"""C ``FE_OVERFLOW`` — overflow exception flag."""

FE_UNDERFLOW = _get("FE_UNDERFLOW")
"""C ``FE_UNDERFLOW`` — underflow exception flag."""

FE_INEXACT = _get("FE_INEXACT")
"""C ``FE_INEXACT`` — inexact result exception flag."""

FE_INVALID = _get("FE_INVALID")
"""C ``FE_INVALID`` — invalid operation exception flag."""


FE_TONEAREST = _get("FE_TONEAREST")
"""C ``FE_TONEAREST`` — round to nearest, ties to even."""

FE_DOWNWARD = _get("FE_DOWNWARD")
"""C ``FE_DOWNWARD`` — round toward :math:`-\\infty`."""

FE_UPWARD = _get("FE_UPWARD")
"""C ``FE_UPWARD`` — round toward :math:`+\\infty`."""

FE_TOWARDZERO = _get("FE_TOWARDZERO")
"""C ``FE_TOWARDZERO`` — round toward zero (truncation)."""


class RoundingMode(enum.IntEnum):
    """IEEE 754 rounding direction.

    Values match the C ``FE_TONEAREST`` / ``FE_DOWNWARD`` / ``FE_UPWARD`` /
    ``FE_TOWARDZERO`` macros fetched at import time.

    .. attribute:: TONEAREST
        Round to nearest, ties to even (default).

    .. attribute:: DOWNWARD
        Round toward :math:`-\\infty`.

    .. attribute:: UPWARD
        Round toward :math:`+\\infty`.

    .. attribute:: TOWARDZERO
        Round toward zero (truncation).
    """

    TONEAREST = FE_TONEAREST
    DOWNWARD = FE_DOWNWARD
    UPWARD = FE_UPWARD
    TOWARDZERO = FE_TOWARDZERO
