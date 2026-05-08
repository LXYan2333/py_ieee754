"""Arithmetic operations on IEEE 754 types.

Free functions (add, sub, mul, div) accept IEEE754 objects and Python floats,
promoting to the appropriate type, and call C wrappers with optional
*round_mode* and *unsuppressed* parameters.

Operator overloads are added to the IEEE754 base class via late imports.
"""

from __future__ import annotations

from collections.abc import Callable
import ctypes as ct
from typing import TYPE_CHECKING, overload

from py_ieee754._exceptions import DEFAULT_UNSUPPRESSED, FloatExceptionError, check_exceptions
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._lib import clib

if TYPE_CHECKING:
    from py_ieee754._types import IEEE754


@overload
def _bind(
    float_type: type[ct.c_float],
    name: str,
) -> Callable[[ct.c_float, ct.c_float, int], tuple[ct.c_float, int]]: ...
@overload
def _bind(
    float_type: type[ct.c_double],
    name: str,
) -> Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int]]: ...
def _bind[T: ct.c_double | ct.c_float](
    float_type: type[T],
    name: str,
) -> Callable[[T, T, int], tuple[T, int]]:
    f = clib[name]
    f.argtypes = [float_type, float_type, ct.POINTER(float_type), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def ret_func(x: T, y: T, rnd: int) -> tuple[T, int]:
        output = float_type()
        excepts = ct.c_int()
        f(x, y, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return ret_func


_addf = _bind(ct.c_float, "py_ieee754_addf")
_add = _bind(ct.c_double, "py_ieee754_add")
_subf = _bind(ct.c_float, "py_ieee754_subf")
_sub = _bind(ct.c_double, "py_ieee754_sub")
_mulf = _bind(ct.c_float, "py_ieee754_mulf")
_mul = _bind(ct.c_double, "py_ieee754_mul")
_divf = _bind(ct.c_float, "py_ieee754_divf")
_div = _bind(ct.c_double, "py_ieee754_div")


def promote(a: IEEE754 | float, b: IEEE754 | float) -> type[IEEE754]:
    """Determine the result type for a binary operation.

    Type promotion rules:

    * If both are IEEE754 and same width → that type.
    * If both are IEEE754 but different widths → the wider type.
    * If only one is IEEE754 → that type.
    * If neither is IEEE754 (both plain ``float``) → :class:`F64`.
    """
    from py_ieee754._types import F64, IEEE754

    a_ieee = isinstance(a, IEEE754)
    b_ieee = isinstance(b, IEEE754)
    if a_ieee and b_ieee:
        if type(a) is type(b):
            return type(a)
        if a.size_bits > b.size_bits:
            return type(a)
        return type(b)
    if a_ieee:
        return type(a)
    if b_ieee:
        return type(b)
    return F64


def to_type(value: IEEE754 | float, cls: type[IEEE754]) -> IEEE754:
    """Convert *value* to *cls*."""
    import py_ieee754._types

    if isinstance(value, cls):
        return value
    if isinstance(value, py_ieee754._types.IEEE754):
        return cls(value.value)
    return cls(value)


def _bin_op(
    a: IEEE754 | float,
    b: IEEE754 | float,
    f32_func: Callable[[ct.c_float, ct.c_float, int], tuple[ct.c_float, int]],
    f64_func: Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int]],
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> IEEE754:
    """Promote operands, call the C wrapper, check exceptions, and return result."""
    from py_ieee754._types import F32

    result_type = promote(a, b)
    fa = to_type(a, result_type)
    fb = to_type(b, result_type)
    rnd = -1 if round_mode is None else int(round_mode)

    if result_type is F32:
        output, excepts = f32_func(ct.c_float(fa.value), ct.c_float(fb.value), rnd)
    else:
        output, excepts = f64_func(ct.c_double(fa.value), ct.c_double(fb.value), rnd)

    check_exceptions(excepts, unsuppressed)
    return result_type._from_float(output.value)  # type: ignore[union-attr]


def add(
    a: IEEE754 | float,
    b: IEEE754 | float,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> IEEE754:
    """Return ``a + b`` computed with IEEE 754 rounding.

    Parameters
    ----------
    a, b:
        Operands.  Python :class:`float` values are promoted to
        :class:`F32` or :class:`F64` according to the :func:`_promote` rules.
    round_mode:
        Desired :class:`~py_ieee754.RoundingMode`.  ``None`` leaves the
        current C rounding direction unchanged.
    unsuppressed:
        Set of exception classes to raise.  Defaults to
        :data:`~py_ieee754._exceptions.DEFAULT_UNSUPPRESSED`
        (``DivByZero`` and ``Overflow``).

    Returns
    -------
    IEEE754
        An :class:`~py_ieee754.IEEE754` instance of the promoted result type.
    """
    return _bin_op(a, b, _addf, _add, round_mode, unsuppressed)


def sub(
    a: IEEE754 | float,
    b: IEEE754 | float,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> IEEE754:
    """Return ``a - b`` computed with IEEE 754 rounding.

    Parameters
    ----------
    a, b:
        Operands.
    round_mode:
        Desired :class:`~py_ieee754.RoundingMode`.  ``None`` means "don't change".
    unsuppressed:
        Set of exception classes to raise.

    Returns
    -------
    IEEE754
        An :class:`~py_ieee754.IEEE754` instance of the promoted result type.
    """
    return _bin_op(a, b, _subf, _sub, round_mode, unsuppressed)


def mul(
    a: IEEE754 | float,
    b: IEEE754 | float,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> IEEE754:
    """Return ``a * b`` computed with IEEE 754 rounding.

    Parameters
    ----------
    a, b:
        Operands.
    round_mode:
        Desired :class:`~py_ieee754.RoundingMode`.  ``None`` means "don't change".
    unsuppressed:
        Set of exception classes to raise.

    Returns
    -------
    IEEE754
        An :class:`~py_ieee754.IEEE754` instance of the promoted result type.
    """
    return _bin_op(a, b, _mulf, _mul, round_mode, unsuppressed)


def div(
    a: IEEE754 | float,
    b: IEEE754 | float,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatExceptionError]] = DEFAULT_UNSUPPRESSED,
) -> IEEE754:
    """Return ``a / b`` computed with IEEE 754 rounding.

    Raises
    ------
    FloatDivByZeroError
        If *b* is zero and :exc:`FloatDivByZeroError` is not suppressed.

    Parameters
    ----------
    a, b:
        Operands.
    round_mode:
        Desired :class:`~py_ieee754.RoundingMode`.  ``None`` means "don't change".
    unsuppressed:
        Set of exception classes to raise.

    Returns
    -------
    IEEE754
        An :class:`~py_ieee754.IEEE754` instance of the promoted result type.
    """
    return _bin_op(a, b, _divf, _div, round_mode, unsuppressed)
