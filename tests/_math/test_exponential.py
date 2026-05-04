"""Tests for exponential/logarithmic functions."""

from __future__ import annotations

import ctypes as ct
import math

import pytest

from py_ieee754._math import exp, exp2, expm1, log, log1p, log2, log10


def test_exp_double():
    assert exp(ct.c_double(1.0)).value == pytest.approx(math.e, rel=1e-10)


def test_exp_float():
    assert exp(ct.c_float(1.0)).value == pytest.approx(math.e, rel=1e-5)


def test_exp2_double():
    assert exp2(ct.c_double(3.0)).value == pytest.approx(8.0)


def test_exp2_float():
    assert isinstance(exp2(ct.c_float(3.0)), ct.c_float)


def test_expm1_double():
    assert expm1(ct.c_double(0.0)).value == pytest.approx(0.0)


def test_expm1_float():
    assert isinstance(expm1(ct.c_float(0.0)), ct.c_float)


def test_log_double():
    assert log(ct.c_double(math.e)).value == pytest.approx(1.0)


def test_log_float():
    assert isinstance(log(ct.c_float(math.e)), ct.c_float)


def test_log10_double():
    assert log10(ct.c_double(100.0)).value == pytest.approx(2.0)


def test_log10_float():
    assert isinstance(log10(ct.c_float(100.0)), ct.c_float)


def test_log2_double():
    assert log2(ct.c_double(8.0)).value == pytest.approx(3.0)


def test_log2_float():
    assert isinstance(log2(ct.c_float(8.0)), ct.c_float)


def test_log1p_double():
    assert log1p(ct.c_double(0.0)).value == pytest.approx(0.0)


def test_log1p_float():
    assert isinstance(log1p(ct.c_float(0.0)), ct.c_float)
