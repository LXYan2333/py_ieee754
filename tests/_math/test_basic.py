"""Tests for basic operations: fabs, fmod, remainder, remquo, fma, fmax, fmin, fdim, nan, nanf."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import fabs, fdim, fma, fmax, fmin, fmod, nan, nanf, remainder, remquo


def test_fabs_double():
    assert fabs(ct.c_double(-3.14)).value == pytest.approx(3.14)


def test_fabs_float():
    assert fabs(ct.c_float(-3.14)).value == pytest.approx(3.14, rel=1e-5)


def test_fmod_double():
    assert fmod(ct.c_double(10.0), ct.c_double(3.0)).value == pytest.approx(math.fmod(10, 3))


def test_fmod_float():
    assert fmod(ct.c_float(10.0), ct.c_float(3.0)).value == pytest.approx(1.0, rel=1e-5)


def test_remainder_double():
    r = remainder(ct.c_double(10.0), ct.c_double(3.0)).value
    assert abs(r - math.remainder(10, 3)) < 0.01


def test_remainder_float():
    r = remainder(ct.c_float(10.0), ct.c_float(3.0))
    assert isinstance(r, ct.c_float)


def test_fma_double():
    assert fma(ct.c_double(1.0), ct.c_double(2.0), ct.c_double(3.0)).value == pytest.approx(5.0)


def test_fma_float():
    r = fma(ct.c_float(1.0), ct.c_float(2.0), ct.c_float(3.0))
    assert isinstance(r, ct.c_float)


def test_fmax_double():
    assert fmax(ct.c_double(1.0), ct.c_double(2.0)).value == pytest.approx(2.0)


def test_fmax_float():
    r = fmax(ct.c_float(1.0), ct.c_float(2.0))
    assert isinstance(r, ct.c_float)


def test_fmin_double():
    assert fmin(ct.c_double(1.0), ct.c_double(2.0)).value == pytest.approx(1.0)


def test_fmin_float():
    r = fmin(ct.c_float(1.0), ct.c_float(2.0))
    assert isinstance(r, ct.c_float)


def test_fdim_double():
    assert fdim(ct.c_double(3.0), ct.c_double(2.0)).value == pytest.approx(1.0)
    assert fdim(ct.c_double(2.0), ct.c_double(3.0)).value == pytest.approx(0.0)


def test_fdim_float():
    r = fdim(ct.c_float(3.0), ct.c_float(2.0))
    assert isinstance(r, ct.c_float)


def test_remquo_double():
    q, r = remquo(ct.c_double(10.0), ct.c_double(3.0))
    assert q.value == pytest.approx(1.0)


def test_remquo_float():
    q, r = remquo(ct.c_float(10.0), ct.c_float(3.0))
    assert isinstance(q, ct.c_float)


def test_nan():
    assert math.isnan(nan().value)


def test_nanf():
    assert math.isnan(nanf().value)
