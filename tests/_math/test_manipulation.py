"""Tests for floating-point manipulation functions."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import copysign, frexp, ilogb, ldexp, logb, modf, nextafter, scalbn


def test_frexp_double():
    f, e = frexp(ct.c_double(8.0))
    assert f.value == pytest.approx(0.5)
    assert e.value == 4


def test_frexp_float():
    f, e = frexp(ct.c_float(8.0))
    assert isinstance(f, ct.c_float)


def test_ldexp_double():
    assert ldexp(ct.c_double(1.5), ct.c_int(3)).value == pytest.approx(12.0)


def test_ldexp_float():
    assert isinstance(ldexp(ct.c_float(1.5), ct.c_int(3)), ct.c_float)


def test_modf_double():
    frac, intpart = modf(ct.c_double(3.14))
    assert frac.value == pytest.approx(0.14, abs=0.01)
    assert intpart.value == pytest.approx(3.0)


def test_modf_float():
    frac, intpart = modf(ct.c_float(3.14))
    assert isinstance(frac, ct.c_float)


def test_scalbn_double():
    assert scalbn(ct.c_double(1.5), ct.c_int(3)).value == pytest.approx(math.ldexp(1.5, 3))


def test_scalbn_float():
    assert isinstance(scalbn(ct.c_float(1.5), ct.c_int(3)), ct.c_float)


def test_ilogb_double():
    assert ilogb(ct.c_double(8.0)).value == 3


def test_ilogb_float():
    assert isinstance(ilogb(ct.c_float(8.0)), ct.c_int)


def test_logb_double():
    assert logb(ct.c_double(8.0)).value == pytest.approx(3.0)


def test_logb_float():
    assert isinstance(logb(ct.c_float(8.0)), ct.c_float)


def test_nextafter_double():
    r = nextafter(ct.c_double(1.0), ct.c_double(2.0))
    assert r.value > 1.0


def test_nextafter_float():
    assert isinstance(nextafter(ct.c_float(1.0), ct.c_float(2.0)), ct.c_float)


def test_copysign_double():
    assert copysign(ct.c_double(1.0), ct.c_double(-2.0)).value == pytest.approx(-1.0)


def test_copysign_float():
    assert isinstance(copysign(ct.c_float(1.0), ct.c_float(-2.0)), ct.c_float)
