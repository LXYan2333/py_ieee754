"""Test that mismatched argument types raise TypeError in multi-arg functions."""

from __future__ import annotations

import ctypes as ct

import pytest

from py_ieee754._math._basic import fdim, fma, fmax, fmin, fmod, remainder, remquo
from py_ieee754._math._manipulation import copysign, nextafter
from py_ieee754._math._power import hypot, pow_
from py_ieee754._math._trigonometric import atan2


def test_fmod_mismatch():
    with pytest.raises(TypeError):
        fmod(ct.c_float(1.0), ct.c_double(2.0))


def test_remainder_mismatch():
    with pytest.raises(TypeError):
        remainder(ct.c_float(1.0), ct.c_double(2.0))


def test_remquo_mismatch():
    with pytest.raises(TypeError):
        remquo(ct.c_float(1.0), ct.c_double(2.0))


def test_fma_mismatch():
    with pytest.raises(TypeError):
        fma(ct.c_float(1.0), ct.c_float(2.0), ct.c_double(3.0))


def test_fmax_mismatch():
    with pytest.raises(TypeError):
        fmax(ct.c_float(1.0), ct.c_double(2.0))


def test_fmin_mismatch():
    with pytest.raises(TypeError):
        fmin(ct.c_float(1.0), ct.c_double(2.0))


def test_fdim_mismatch():
    with pytest.raises(TypeError):
        fdim(ct.c_float(1.0), ct.c_double(2.0))


def test_pow_mismatch():
    with pytest.raises(TypeError):
        pow_(ct.c_float(1.0), ct.c_double(2.0))


def test_hypot_mismatch():
    with pytest.raises(TypeError):
        hypot(ct.c_float(1.0), ct.c_double(2.0))


def test_atan2_mismatch():
    with pytest.raises(TypeError):
        atan2(ct.c_float(1.0), ct.c_double(2.0))


def test_nextafter_mismatch():
    with pytest.raises(TypeError):
        nextafter(ct.c_float(1.0), ct.c_double(2.0))


def test_copysign_mismatch():
    with pytest.raises(TypeError):
        copysign(ct.c_float(1.0), ct.c_double(2.0))
