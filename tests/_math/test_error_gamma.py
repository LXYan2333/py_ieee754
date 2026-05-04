"""Tests for error and gamma functions."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import erf, erfc, lgamma, tgamma


def test_erf_double():
    assert erf(ct.c_double(1.0)).value == pytest.approx(math.erf(1))


def test_erf_float():
    assert isinstance(erf(ct.c_float(1.0)), ct.c_float)


def test_erfc_double():
    assert erfc(ct.c_double(1.0)).value == pytest.approx(math.erfc(1))


def test_erfc_float():
    assert isinstance(erfc(ct.c_float(1.0)), ct.c_float)


def test_tgamma_double():
    assert tgamma(ct.c_double(5.0)).value == pytest.approx(math.gamma(5))


def test_tgamma_float():
    assert isinstance(tgamma(ct.c_float(5.0)), ct.c_float)


def test_lgamma_double():
    assert lgamma(ct.c_double(5.0)).value == pytest.approx(math.lgamma(5))


def test_lgamma_float():
    assert isinstance(lgamma(ct.c_float(5.0)), ct.c_float)
