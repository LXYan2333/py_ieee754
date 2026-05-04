"""Tests for exception handling and FE_* bindings."""

import pytest

from py_ieee754 import (
    FloatDivByZeroError,
    FloatException,
    FloatInexactError,
    FloatOverflowError,
    RoundingMode,
)
from py_ieee754._exceptions import _EXCEPTION_MAP, DEFAULT_UNSUPPRESSED, check_exceptions
from py_ieee754._fenv_bindings import (
    FE_DIVBYZERO,
    FE_DOWNWARD,
    FE_INEXACT,
    FE_INVALID,
    FE_OVERFLOW,
    FE_TONEAREST,
    FE_TOWARDZERO,
    FE_UNDERFLOW,
    FE_UPWARD,
)


class TestFloatException:
    def test_values(self):
        assert isinstance(FE_DIVBYZERO, int)
        assert isinstance(FE_OVERFLOW, int)
        assert FloatException.DIVBYZERO == FE_DIVBYZERO

    def test_all(self):
        expected = FE_DIVBYZERO | FE_OVERFLOW | FE_UNDERFLOW | FE_INEXACT | FE_INVALID
        assert expected == FloatException.ALL


class TestExceptionClasses:
    def test_inheritance(self):
        assert issubclass(FloatDivByZeroError, FloatingPointError)
        assert issubclass(FloatOverflowError, FloatingPointError)

    def test_exception_map(self):
        assert _EXCEPTION_MAP[FloatException.DIVBYZERO] is FloatDivByZeroError
        assert _EXCEPTION_MAP[FloatException.OVERFLOW] is FloatOverflowError


class TestCheckExceptions:
    def test_no_exception_when_masked(self):
        # FE_INEXACT with default mask (only DivByZero + Overflow) should not raise
        check_exceptions(FE_INEXACT, DEFAULT_UNSUPPRESSED)

    def test_raises_div_by_zero(self):
        with pytest.raises(FloatDivByZeroError):
            check_exceptions(FE_DIVBYZERO, DEFAULT_UNSUPPRESSED)

    def test_raises_multiple(self):
        flags = FE_DIVBYZERO | FE_INEXACT
        # Only DivByZero should raise (Inexact not in DEFAULT_UNSUPPRESSED)
        with pytest.raises(FloatDivByZeroError):
            check_exceptions(flags, DEFAULT_UNSUPPRESSED)


class TestDefaultUnsuppressed:
    def test_default_set(self):
        assert FloatDivByZeroError in DEFAULT_UNSUPPRESSED
        assert FloatOverflowError in DEFAULT_UNSUPPRESSED
        assert FloatInexactError not in DEFAULT_UNSUPPRESSED


class TestRoundingModeEnum:
    def test_values(self):
        assert RoundingMode.TONEAREST == FE_TONEAREST
        assert RoundingMode.DOWNWARD == FE_DOWNWARD
        assert RoundingMode.UPWARD == FE_UPWARD
        assert RoundingMode.TOWARDZERO == FE_TOWARDZERO

    def test_names(self):
        names = {m.name for m in RoundingMode}
        assert names == {"TONEAREST", "DOWNWARD", "UPWARD", "TOWARDZERO"}

    def test_negative_one_not_a_rounding_mode(self):
        assert -1 not in {m.value for m in RoundingMode}
        # -1 means "don't change" in C wrappers, should never match a real mode
