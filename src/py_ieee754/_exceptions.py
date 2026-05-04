"""Floating-point exception handling.

After each C arithmetic call, raw FE_* exception flags from the C wrapper are
raised as Python exceptions for the enabled types (default: DIVBYZERO, OVERFLOW).
"""

from __future__ import annotations

import enum

from py_ieee754._fenv_bindings import (
    FE_DIVBYZERO,
    FE_INEXACT,
    FE_INVALID,
    FE_OVERFLOW,
    FE_UNDERFLOW,
)


class FloatException(enum.IntFlag):
    """Floating-point exception flags matching the C ``FE_*`` macros.

    Bits are combined with ``|`` to form masks::

        FloatException.DIVBYZERO | FloatException.OVERFLOW

    .. attribute:: DIVBYZERO
    .. attribute:: OVERFLOW
    .. attribute:: UNDERFLOW
    .. attribute:: INEXACT
    .. attribute:: INVALID
    .. attribute:: ALL
    """

    DIVBYZERO = FE_DIVBYZERO
    OVERFLOW = FE_OVERFLOW
    UNDERFLOW = FE_UNDERFLOW
    INEXACT = FE_INEXACT
    INVALID = FE_INVALID


class FloatExceptionError(FloatingPointError):
    """Base for all IEEE 754 floating-point exceptions.

    Carries the full set of exception classes that occurred, even though only
    one Python exception can be raised at a time.

    Attributes
    ----------
    excepts:
        Set of all :class:`FloatExceptionError` subclasses that occurred.
    """

    def __init__(self, excepts: set[type[FloatExceptionError]]) -> None:
        self.excepts: set[type[FloatExceptionError]] = excepts


class FloatDivByZeroError(FloatExceptionError):
    """Raised when an operation on finite numbers produces infinity as exact answer."""


class FloatOverflowError(FloatExceptionError):
    """Raised when a result has to be represented as a floating-point number, but has (much) larger
    absolute value than the largest  (finite)  floating-point number that is representable."""


class FloatUnderflowError(FloatExceptionError):
    """Raised when a result has to be represented as a floating-point number, but has smaller
    absolute value than the smallest positive normalized floating-point number (and would lose much
    accuracy when represented as a denormalized number)."""


class FloatInexactError(FloatExceptionError):
    """Raised when the rounded result of an operation is not equal to the infinite precision result.
    It may occur whenever overflow or underflow occurs."""


class FloatInvalidError(FloatExceptionError):
    """Raised when there is no well-defined result for an operation, as for 0/0 or
    infinity - infinity or sqrt(-1)."""


_EXCEPTION_MAP: dict[FloatException, type[FloatExceptionError]] = {
    FloatException.DIVBYZERO: FloatDivByZeroError,
    FloatException.OVERFLOW: FloatOverflowError,
    FloatException.UNDERFLOW: FloatUnderflowError,
    FloatException.INEXACT: FloatInexactError,
    FloatException.INVALID: FloatInvalidError,
}

# Priority order for raising when multiple exceptions occur simultaneously.
_EXCEPTION_PRIORITY: list[FloatException] = [
    FloatException.INVALID,
    FloatException.DIVBYZERO,
    FloatException.OVERFLOW,
    FloatException.UNDERFLOW,
    FloatException.INEXACT,
]

DEFAULT_UNSUPPRESSED: set[type[FloatExceptionError]] = {
    FloatDivByZeroError,
    FloatOverflowError,
}
"""Default set of exception classes that propagate to Python.

:exc:`FloatInexactError`, :exc:`FloatUnderflowError`, and
:exc:`FloatInvalidError` are suppressed by default.
"""


def check_exceptions(
    excepts: int,
    unsuppressed: set[type[FloatExceptionError]],
) -> None:
    """Raise enabled exception classes for the given raw FE_* flags.

    When multiple flags are set, the highest-priority exception is raised
    (Invalid > DivByZero > Overflow > Underflow > Inexact).  The full set of
    all exception classes that occurred is stored in ``exc.excepts``.

    Parameters
    ----------
    excepts:
        Raw exception flags returned from a C wrapper (OR of ``FE_*`` bits).
    unsuppressed:
        Set of :class:`FloatExceptionError` subclasses that are allowed to raise.
    """
    if excepts == 0:
        return
    flags = FloatException(excepts)
    all_raised_excepts = {t for f, t in _EXCEPTION_MAP.items() if flags & f}
    for flag in _EXCEPTION_PRIORITY:
        exc_type = _EXCEPTION_MAP[flag]
        if exc_type in all_raised_excepts and exc_type in unsuppressed:
            raise exc_type(all_raised_excepts)
