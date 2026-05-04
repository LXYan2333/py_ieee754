"""IEEE 754 float number module with bit-operation and round arithmetic support.

Usage::

    from py_ieee754 import F32, F64

    a = F32(1.5)
    b = F64(2.25)

    # field access
    print(a.sign, a.exponent, a.significand)

    # arithmetic with operator overloads
    c = a + F32(3.0)

    # arithmetic with free functions
    from py_ieee754 import add, sub, mul, div
    d = add(a, b)

    # construction from ctypes
    import ctypes as ct
    e = IEEE754.from_ctypes(ct.c_float(1.5))  # → F32

    # math functions
    from py_ieee754 import math
    f = math.sqrt(ct.c_double(2.0))
"""

from py_ieee754 import _math as math
from py_ieee754._arithmetic import add, div, mul, sub
from py_ieee754._exceptions import (
    DEFAULT_UNSUPPRESSED,
    FloatDivByZeroError,
    FloatException,
    FloatExceptionError,
    FloatInexactError,
    FloatInvalidError,
    FloatOverflowError,
    FloatUnderflowError,
)
from py_ieee754._fenv_bindings import RoundingMode
from py_ieee754._types import F32, F64, IEEE754

__all__ = [
    # Types
    "IEEE754",
    "F32",
    "F64",
    # Arithmetic
    "add",
    "sub",
    "mul",
    "div",
    # Rounding
    "RoundingMode",
    # Exceptions
    "FloatException",
    "FloatExceptionError",
    "FloatDivByZeroError",
    "FloatOverflowError",
    "FloatUnderflowError",
    "FloatInexactError",
    "FloatInvalidError",
    "DEFAULT_UNSUPPRESSED",
    # <math.h> functions exposed to python, with round and exception control support.
    "math",
]
