"""Tests for hyperbolic functions."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import acosh, asinh, atanh, cosh, sinh, tanh


def test_sinh_double():
    assert sinh(ct.c_double(1.0)).value == pytest.approx(math.sinh(1))


def test_sinh_float():
    assert isinstance(sinh(ct.c_float(1.0)), ct.c_float)


def test_cosh_double():
    assert cosh(ct.c_double(1.0)).value == pytest.approx(math.cosh(1))


def test_cosh_float():
    assert isinstance(cosh(ct.c_float(1.0)), ct.c_float)


def test_tanh_double():
    assert tanh(ct.c_double(1.0)).value == pytest.approx(math.tanh(1))


def test_tanh_float():
    assert isinstance(tanh(ct.c_float(1.0)), ct.c_float)


def test_asinh_double():
    assert asinh(ct.c_double(1.0)).value == pytest.approx(math.asinh(1))


def test_asinh_float():
    assert isinstance(asinh(ct.c_float(1.0)), ct.c_float)


def test_acosh_double():
    assert acosh(ct.c_double(2.0)).value == pytest.approx(math.acosh(2))


def test_acosh_float():
    assert isinstance(acosh(ct.c_float(2.0)), ct.c_float)


def test_atanh_double():
    assert atanh(ct.c_double(0.5)).value == pytest.approx(math.atanh(0.5))


def test_atanh_float():
    assert isinstance(atanh(ct.c_float(0.5)), ct.c_float)
