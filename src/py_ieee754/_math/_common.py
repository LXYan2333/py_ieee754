"""Shared infrastructure for math.h bindings."""

from __future__ import annotations

from collections.abc import Callable
import ctypes as ct

from py_ieee754._lib import clib

# ---- Typed binders: call C wrapper, return (result, exception_flags) ----


def bind_1d(name: str) -> Callable[[ct.c_double, int], tuple[ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_double, int]:
        output = ct.c_double()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_1f(name: str) -> Callable[[ct.c_float, int], tuple[ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.POINTER(ct.c_float), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_float, int]:
        output = ct.c_float()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_2d(name: str) -> Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.c_double, ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, y: ct.c_double, rnd: int) -> tuple[ct.c_double, int]:
        output = ct.c_double()
        excepts = ct.c_int()
        f(x, y, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_2f(name: str) -> Callable[[ct.c_float, ct.c_float, int], tuple[ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.c_float, ct.POINTER(ct.c_float), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, y: ct.c_float, rnd: int) -> tuple[ct.c_float, int]:
        output = ct.c_float()
        excepts = ct.c_int()
        f(x, y, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_3d(
    name: str,
) -> Callable[[ct.c_double, ct.c_double, ct.c_double, int], tuple[ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [
        ct.c_double,
        ct.c_double,
        ct.c_double,
        ct.POINTER(ct.c_double),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_double, y: ct.c_double, z: ct.c_double, rnd: int) -> tuple[ct.c_double, int]:
        output = ct.c_double()
        excepts = ct.c_int()
        f(x, y, z, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_3f(
    name: str,
) -> Callable[[ct.c_float, ct.c_float, ct.c_float, int], tuple[ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [
        ct.c_float,
        ct.c_float,
        ct.c_float,
        ct.POINTER(ct.c_float),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_float, y: ct.c_float, z: ct.c_float, rnd: int) -> tuple[ct.c_float, int]:
        output = ct.c_float()
        excepts = ct.c_int()
        f(x, y, z, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_s_d(name: str) -> Callable[[ct.c_char_p, int], tuple[ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_char_p, ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(tag: ct.c_char_p, rnd: int) -> tuple[ct.c_double, int]:
        output = ct.c_double()
        excepts = ct.c_int()
        f(tag, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_s_f(name: str) -> Callable[[ct.c_char_p, int], tuple[ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_char_p, ct.POINTER(ct.c_float), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(tag: ct.c_char_p, rnd: int) -> tuple[ct.c_float, int]:
        output = ct.c_float()
        excepts = ct.c_int()
        f(tag, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_2di_d(
    name: str,
) -> Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [
        ct.c_double,
        ct.c_double,
        ct.POINTER(ct.c_double),
        ct.POINTER(ct.c_int),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_double, y: ct.c_double, rnd: int) -> tuple[ct.c_double, int, int]:
        output = ct.c_double()
        quo = ct.c_int()
        excepts = ct.c_int()
        f(x, y, ct.byref(output), ct.byref(quo), rnd, ct.byref(excepts))
        return output, quo.value, excepts.value

    return w


def bind_2fi_f(
    name: str,
) -> Callable[[ct.c_float, ct.c_float, int], tuple[ct.c_float, int, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [
        ct.c_float,
        ct.c_float,
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_int),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_float, y: ct.c_float, rnd: int) -> tuple[ct.c_float, int, int]:
        output = ct.c_float()
        quo = ct.c_int()
        excepts = ct.c_int()
        f(x, y, ct.byref(output), ct.byref(quo), rnd, ct.byref(excepts))
        return output, quo.value, excepts.value

    return w


def bind_d_l(name: str) -> Callable[[ct.c_double, int], tuple[ct.c_long, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.POINTER(ct.c_long), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_long, int]:
        output = ct.c_long()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_f_l(name: str) -> Callable[[ct.c_float, int], tuple[ct.c_long, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.POINTER(ct.c_long), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_long, int]:
        output = ct.c_long()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_d_ll(name: str) -> Callable[[ct.c_double, int], tuple[ct.c_longlong, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.POINTER(ct.c_longlong), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_longlong, int]:
        output = ct.c_longlong()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_f_ll(name: str) -> Callable[[ct.c_float, int], tuple[ct.c_longlong, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.POINTER(ct.c_longlong), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_longlong, int]:
        output = ct.c_longlong()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_1di_d(
    name: str,
) -> Callable[[ct.c_double, int], tuple[ct.c_double, int, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [
        ct.c_double,
        ct.POINTER(ct.c_double),
        ct.POINTER(ct.c_int),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_double, int, int]:
        output = ct.c_double()
        exp_out = ct.c_int()
        excepts = ct.c_int()
        f(x, ct.byref(output), ct.byref(exp_out), rnd, ct.byref(excepts))
        return output, exp_out.value, excepts.value

    return w


def bind_1fi_f(
    name: str,
) -> Callable[[ct.c_float, int], tuple[ct.c_float, int, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [
        ct.c_float,
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_int),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_float, int, int]:
        output = ct.c_float()
        exp_out = ct.c_int()
        excepts = ct.c_int()
        f(x, ct.byref(output), ct.byref(exp_out), rnd, ct.byref(excepts))
        return output, exp_out.value, excepts.value

    return w


def bind_1dd_d(
    name: str,
) -> Callable[[ct.c_double, int], tuple[ct.c_double, ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [
        ct.c_double,
        ct.POINTER(ct.c_double),
        ct.POINTER(ct.c_double),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_double, ct.c_double, int]:
        output = ct.c_double()
        intpart = ct.c_double()
        excepts = ct.c_int()
        f(x, ct.byref(output), ct.byref(intpart), rnd, ct.byref(excepts))
        return output, intpart, excepts.value

    return w


def bind_1ff_f(
    name: str,
) -> Callable[[ct.c_float, int], tuple[ct.c_float, ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [
        ct.c_float,
        ct.POINTER(ct.c_float),
        ct.POINTER(ct.c_float),
        ct.c_int,
        ct.POINTER(ct.c_int),
    ]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_float, ct.c_float, int]:
        output = ct.c_float()
        intpart = ct.c_float()
        excepts = ct.c_int()
        f(x, ct.byref(output), ct.byref(intpart), rnd, ct.byref(excepts))
        return output, intpart, excepts.value

    return w


def bind_di_d(name: str) -> Callable[[ct.c_double, ct.c_int, int], tuple[ct.c_double, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.c_int, ct.POINTER(ct.c_double), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, n: ct.c_int, rnd: int) -> tuple[ct.c_double, int]:
        output = ct.c_double()
        excepts = ct.c_int()
        f(x, n, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_fi_f(name: str) -> Callable[[ct.c_float, ct.c_int, int], tuple[ct.c_float, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.c_int, ct.POINTER(ct.c_float), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, n: ct.c_int, rnd: int) -> tuple[ct.c_float, int]:
        output = ct.c_float()
        excepts = ct.c_int()
        f(x, n, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_d_i(name: str) -> Callable[[ct.c_double, int], tuple[ct.c_int, int]]:
    f = getattr(clib, f"py_ieee754_{name}")
    f.argtypes = [ct.c_double, ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_double, rnd: int) -> tuple[ct.c_int, int]:
        output = ct.c_int()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w


def bind_f_i(name: str) -> Callable[[ct.c_float, int], tuple[ct.c_int, int]]:
    f = getattr(clib, f"py_ieee754_{name}f")
    f.argtypes = [ct.c_float, ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int)]
    f.restype = None

    def w(x: ct.c_float, rnd: int) -> tuple[ct.c_int, int]:
        output = ct.c_int()
        excepts = ct.c_int()
        f(x, ct.byref(output), rnd, ct.byref(excepts))
        return output, excepts.value

    return w
