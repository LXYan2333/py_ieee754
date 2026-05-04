"""Tests for nearest integer functions."""

from __future__ import annotations

import ctypes as ct

import pytest

from py_ieee754._math import (
    ceil,
    floor,
    llrint,
    llround,
    lrint,
    lround,
    nearbyint,
    rint,
    round_,
    trunc,
)


def test_ceil_double():
    assert ceil(ct.c_double(1.5)).value == pytest.approx(2.0)


def test_ceil_float():
    assert isinstance(ceil(ct.c_float(1.5)), ct.c_float)


def test_floor_double():
    assert floor(ct.c_double(1.5)).value == pytest.approx(1.0)


def test_floor_float():
    assert isinstance(floor(ct.c_float(1.5)), ct.c_float)


def test_trunc_double():
    assert trunc(ct.c_double(-1.5)).value == pytest.approx(-1.0)


def test_trunc_float():
    assert isinstance(trunc(ct.c_float(-1.5)), ct.c_float)


def test_round_double():
    assert round_(ct.c_double(3.5)).value == pytest.approx(4.0)


def test_round_float():
    assert isinstance(round_(ct.c_float(3.5)), ct.c_float)


def test_nearbyint_double():
    assert nearbyint(ct.c_double(3.7)).value == pytest.approx(4.0)


def test_nearbyint_float():
    assert isinstance(nearbyint(ct.c_float(3.7)), ct.c_float)


def test_rint_double():
    assert rint(ct.c_double(3.7)).value == pytest.approx(4.0)


def test_rint_float():
    assert isinstance(rint(ct.c_float(3.7)), ct.c_float)


def test_lround_double():
    assert lround(ct.c_double(3.7)).value == 4


def test_lround_float():
    assert isinstance(lround(ct.c_float(3.7)), ct.c_long)


def test_llround_double():
    assert llround(ct.c_double(3.7)).value == 4


def test_llround_float():
    assert isinstance(llround(ct.c_float(3.7)), ct.c_longlong)


def test_lrint_double():
    assert lrint(ct.c_double(3.7)).value == 4


def test_lrint_float():
    assert isinstance(lrint(ct.c_float(3.7)), ct.c_long)


def test_llrint_double():
    assert llrint(ct.c_double(3.7)).value == 4


def test_llrint_float():
    assert isinstance(llrint(ct.c_float(3.7)), ct.c_longlong)
