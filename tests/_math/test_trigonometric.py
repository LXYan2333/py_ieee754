"""Tests for trigonometric functions."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import acos, asin, atan, atan2, cos, sin, tan


def test_sin_double():
    assert sin(ct.c_double(0.0)).value == pytest.approx(0.0)
    assert sin(ct.c_double(math.pi / 2)).value == pytest.approx(1.0)


def test_sin_float():
    assert isinstance(sin(ct.c_float(0.0)), ct.c_float)


def test_cos_double():
    assert cos(ct.c_double(0.0)).value == pytest.approx(1.0)


def test_cos_float():
    assert isinstance(cos(ct.c_float(0.0)), ct.c_float)


def test_tan_double():
    assert tan(ct.c_double(0.0)).value == pytest.approx(0.0)


def test_tan_float():
    assert isinstance(tan(ct.c_float(0.0)), ct.c_float)


def test_asin_double():
    assert asin(ct.c_double(0.0)).value == pytest.approx(0.0)


def test_asin_float():
    assert isinstance(asin(ct.c_float(0.0)), ct.c_float)


def test_acos_double():
    assert acos(ct.c_double(1.0)).value == pytest.approx(0.0)


def test_acos_float():
    assert isinstance(acos(ct.c_float(1.0)), ct.c_float)


def test_atan_double():
    assert atan(ct.c_double(0.0)).value == pytest.approx(0.0)


def test_atan_float():
    assert isinstance(atan(ct.c_float(0.0)), ct.c_float)


def test_atan2_double():
    assert atan2(ct.c_double(1.0), ct.c_double(0.0)).value == pytest.approx(math.pi / 2)


def test_atan2_float():
    r = atan2(ct.c_float(1.0), ct.c_float(1.0))
    assert isinstance(r, ct.c_float)
