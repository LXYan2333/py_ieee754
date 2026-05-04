"""Tests for power functions: sqrt, pow, cbrt, hypot."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754 import RoundingMode
from py_ieee754._math import cbrt, hypot, sqrt
from py_ieee754._math import pow as pow_


def test_sqrt_double():
    assert sqrt(ct.c_double(4.0)).value == pytest.approx(2.0)


def test_sqrt_float():
    assert sqrt(ct.c_float(4.0)).value == pytest.approx(2.0, rel=1e-6)


def test_sqrt_round_down():
    result = sqrt(ct.c_double(2.0), round_mode=RoundingMode.DOWNWARD)
    assert result.value < math.sqrt(2)


def test_sqrt_none_round_mode_preserves_default():
    default_result = sqrt(ct.c_double(2.0))
    none_result = sqrt(ct.c_double(2.0), round_mode=None)
    assert default_result.value == pytest.approx(none_result.value)
    # -1 sentinel means "don't change rounding" — result matches default


def test_pow_double():
    assert pow_(ct.c_double(2.0), ct.c_double(10.0)).value == pytest.approx(1024.0)


def test_pow_float():
    assert pow_(ct.c_float(2.0), ct.c_float(10.0)).value == pytest.approx(1024.0, rel=1e-5)


def test_cbrt_double():
    assert cbrt(ct.c_double(8.0)).value == pytest.approx(2.0)


def test_cbrt_float():
    assert cbrt(ct.c_float(8.0)).value == pytest.approx(2.0, rel=1e-5)


def test_hypot_double():
    assert hypot(ct.c_double(3.0), ct.c_double(4.0)).value == pytest.approx(math.hypot(3, 4))


def test_hypot_float():
    assert hypot(ct.c_float(3.0), ct.c_float(4.0)).value == pytest.approx(5.0, rel=1e-5)
