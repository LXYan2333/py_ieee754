"""Shared wrapper library loader.

Supports both regular and editable installs by searching
``py_ieee754`` submodule locations first, then falling back
to the directory alongside this file.
"""

from __future__ import annotations

import ctypes as ct
import importlib.util as _iu
import os
import sys

_suffixes = {"linux": ".so", "darwin": ".dylib", "win32": ".dll"}
_lib_name = f"_py_ieee754_wrappers{_suffixes.get(sys.platform, '.so')}"


def _find_library() -> str:
    """Locate the shared library, supporting both regular and editable installs."""
    _pkg_spec = _iu.find_spec("py_ieee754")
    if _pkg_spec is not None and _pkg_spec.submodule_search_locations:
        for _loc in _pkg_spec.submodule_search_locations:
            _candidate = os.path.join(_loc, _lib_name)
            if os.path.exists(_candidate):
                return _candidate

    # Fallback: alongside this file.
    return os.path.join(os.path.dirname(__file__), _lib_name)  # pragma: no cover


clib = ct.CDLL(_find_library())
"""ctypes handle to the shared C wrapper library ``_py_ieee754_wrappers``.

All :mod:`py_ieee754._math` functions and the arithmetic operators call
into this library to perform computations with correct FP rounding and
exception flag reporting."""

