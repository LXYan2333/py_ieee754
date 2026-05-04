# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project State

This is a working IEEE 754 float number module with full test coverage. It uses Python 3.13+ with a virtual environment at `.venv/`.

## Project Goal

This is an IEEE 754 float number module with bit-operation and round arithmetic support. User can create F32/F64 IEEE754 object from float number, bin/hex str, int (bit-cast), or ctypes values, and convert float number to them. This project also provides [airithmetic](https://docs.python.org/3/tutorial/floatingpoint.html) between ieee754 float objects, with
- free function style interface, with ctypes float/double interface and an optional parameter to set desired round mode (default to unchange) and unsuppressed exception (default to DivByZeroException and OverflowException).
- operator overload style interface
- round support
which is forwarded to C by ctypes. 

When float point exception happens in C, correspoing exception bits should be return to Python, but allow user to choose the exception desired to propagate (and by default only allow DivByZeroException and OverflowException to propagate).

## Project API and Implementation Details

This project provides this interface:

```python
import ctypes as ct
from typing import Self

# type aliases
type ct_float_type = type[ct.c_float] | type[ct.c_double]
type ct_uint_type = type[ct.c_uint32] | type[ct.c_uint64]

class IEEE754(ABC):
    """Abstract base — not directly instantiated."""

    __slots__ = ("_value", "_as_int")

    # Per-subclass configuration
    _val_t: ClassVar[type[ct.c_float] | type[ct.c_double]]
    _uint_t: ClassVar[type[ct.c_uint32] | type[ct.c_uint64]]
    _bias: ClassVar[int]            # 127 for F32, 1023 for F64
    _exp_bits: ClassVar[slice]      # e.g. slice(1, 9) for F32
    _sig_bits: ClassVar[slice]      # e.g. slice(9, 32) for F32

    # Instance attributes
    _value: ct.c_float | ct.c_double
    _as_int: int  # cached bit pattern

    # Construction: accepts float (value), int (bit-cast), str (hex/bin/decimal),
    # or ctypes (ct.c_float / ct.c_double)
    F32(1.5)                        # from float
    F32(0x3FC00000)                 # from int bit-cast
    F32("0x3FC00000")               # from hex string
    F32("0b00111111...")            # from binary string
    F32(ct.c_float(1.5))            # from ctypes
    F32.from_bits(0x3FC00000)       # explicit bit-cast classmethod
    IEEE754.from_ctypes(ct.c_float(1.5))  # auto-dispatch: ct.c_float → F32, ct.c_double → F64

class F32(IEEE754):
    _val_t = ct.c_float
    _uint_t = ct.c_uint32
    _bias = 127
    _exp_bits = slice(1, 9)
    _sig_bits = slice(9, 32)

class F64(IEEE754):
    _val_t = ct.c_double
    _uint_t = ct.c_uint64
    _bias = 1023
    _exp_bits = slice(1, 12)
    _sig_bits = slice(12, 64)
```

IEEE754 objects are immutable — mutation methods return new `Self` objects.

Type-punning is done via ctypes' `from_buffer_copy`. The `_value` (ctypes) and `_as_int` (bit pattern) are stored together on construction to avoid repeated re-interpretation.

**Key properties / methods on IEEE754:**

- `.sign: int` (0 or 1), `.exponent: int` (unbiased raw exp bits), `.significand: int` (mantissa bits)
- `.exponent_biased: int` (biased exponent; subnormals return 1 - bias)
- `.bits: int` (raw bit pattern), `.bin: str`, `.hex: str`, `.hex_literal: str`, `.float_hex: str`, `.cxx_bitcast: str`
- `.ctypes_value: ct.c_float | ct.c_double` (abstract property, narrowed in F32/F64)
- Classification: `.is_nan`, `.is_snan`, `.is_qnan`, `.is_inf`, `.is_zero`, `.is_subnormal`, `.is_normal`, `.is_finite`
- Factory classmethods: `.nan()`, `.snan()`, `.inf()`, `.zero(negative=False)`, `.from_bits(bits)`, `.from_ctypes(value)`, `.from_components(s, e, m)`, `.from_bin_str(s)`
- Mutation: `.with_sign(s)`, `.with_exponent(e)`, `.with_significand(m)` — all return new Self
- Decomposition: `.decompose() -> (int, int, int)`, `.decompose_bin() -> (str, str, str)`
- Comparison: `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__` against IEEE754 and float
- Arithmetic operators (`__add__`, `__sub__`, `__mul__`, `__truediv__` + reflected) delegate to `_arithmetic.py`

**Exception handling:** FP exception flags are managed entirely in C wrappers (save round → clear except → compute → test except → restore round). Exception flags are returned as `int` and raised via `check_exceptions(excepts, unsuppressed)`. Default unsuppressed: `{FloatDivByZeroError, FloatOverflowError}`.

## math.h Bindings

All `<math.h>` functions are exposed via C wrappers that handle rounding mode and exception flags atomically (save round → clear except → compute → test except → restore round). No Python-side fenv calls — exception flags are returned from C as integers and raised by `check_exceptions`.

### C side

One `.c` file per math category (e.g. `_math_power.c`, `_math_basic.c`), each included in the `wrappers` shared library via `CMakeLists.txt`. Shared macros live in `c/_math_common.h`:

```c
#include "_math_common.h"
#include <math.h>

WRAP_1D(sqrt)  WRAP_1F(sqrt)   // 1-arg double/float
WRAP_2D(pow)   WRAP_2F(pow)    // 2-arg
WRAP_3D(fma)   WRAP_3F(fma)    // 3-arg
```

Each wrapper has the signature `void py_ieee754_NAME(..., TYPE *output, int rnd, int *except)` where `rnd == -1` means "don't change rounding".  For special functions (remquo, frexp, modf, nan) with extra pointer or string args, write explicit functions instead of using macros.

### Python side

Submodule `src/py_ieee754/_math/` with one `.py` file per category.

**`_common.py`** provides typed binders that call C wrappers and return `(result, exception_flags)`:

```python
def bind_1d(name: str) -> Callable[[ct.c_double, int], tuple[ct.c_double, int]]: ...
def bind_2d(name: str) -> Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int]]: ...
def bind_s_d(name: str) -> Callable[[ct.c_char_p, int], tuple[ct.c_double, int]]: ...  # for nan
def bind_2di_d(name: str) -> Callable[[ct.c_double, ct.c_double, int], tuple[ct.c_double, int, int]]: ...  # remquo
```

**Category files** follow this pattern for each function:

```python
# Binding — created once at module level
_sqrt = bind_1d("sqrt")
_sqrtf = bind_1f("sqrt")

# Public function — uses constrained generic T: (ct.c_float, ct.c_double)
# With @overload for multi-arg functions to help pyright narrow types
@overload
def pow_(x: ct.c_float, y: ct.c_float, *, ...) -> ct.c_float: ...
@overload
def pow_(x: ct.c_double, y: ct.c_double, *, ...) -> ct.c_double: ...
def pow_[T: (ct.c_float, ct.c_double)](
    x: T, y: T,
    *,
    round_mode: RoundingMode | None = None,
    unsuppressed: set[type[FloatingPointError]] = DEFAULT_UNSUPPRESSED,
) -> T:
    rnd = _rnd(round_mode)
    if isinstance(x, ct.c_float) and isinstance(y, ct.c_float):
        result, excepts = _powf(x, y, rnd)
    elif isinstance(x, ct.c_double) and isinstance(y, ct.c_double):
        result, excepts = _pow(x, y, rnd)
    else:
        raise TypeError()
    check_exceptions(excepts, unsuppressed)
    return result
```

Rules:
- Use `elif isinstance(x, ct.c_double) and ...: ... else: raise TypeError()` pattern for multi-arg functions (helps pyright narrow constrained TypeVars).
- For 1-arg functions, `if isinstance(x, ct.c_float): ... elif isinstance(x, ct.c_double): ...` is sufficient.
- Tuple-returning functions use `tuple[ct.c_double | ct.c_float, ct.c_int]` style, not `tuple[ct.c_double, ct.c_int] | tuple[ct.c_float, ct.c_int]`.
- Use `@overload` for multi-arg functions only; 1-arg functions don't need them.
- `_rnd(mode)` converts `RoundingMode | None` to C `int` (-1 for None).
- Do NOT use `@fp_wrap` decorators — the binder handles FP state. Do NOT use bash `>>` append to modify files — use the Edit tool.

## Python Environment

- Python 3.13.5
- Virtual environment: `.venv/` (activate with `source .venv/bin/activate`)
- Install packages with `pip install <package>`

## Conventions

Once the project has code, follow these conventions by default unless a specific tool/pattern is established:

- **Type hints**: Use Python 3.13 style type hints everywhere new code is added. The code must be fully type-hinted, `any` should be avoied when possible. Do not use str when Literal is suitable and possible. Do not duplicate Literals everywhere when it is suitable and possible to write it as one global variable.
- **Python doc** write python doc in `PEP257` format
- **Python code** If possible, do not directly write long hex/bin literals, instead generate them with bit operations and write comment to explain it.
- **Testing**: Use `pytest` for tests
- **Formatting/linting**: Use `ruff` for both formatting and linting, and use `pyright` strict mode to check types. However, pytest is not fully typed, only do basic Pyright check on tests. Do not automatically run formatter. Add formatter, linter and pyright check to git pre-commit hook.
- **Import sorting**: Use `ruff check --select I --fix` for import sorting
- **Project structure**: Use src convension
- **CMake code**: Use CMake to manage C code. Keep CMakeLists.txt minimal — just `add_library`, link `m` on non-Windows, add compiler FP flags (`/fp:strict` for MSVC, `-frounding-math -fsignaling-nans` for Clang/GCC), and `install`. Remember to dll export function in MSVC. Note: on windows, the dll needs to be installed as RUNTIME, not LIBRARY. Note on windows there will not be a prefix "lib" in the dll file.
- **C code**: Use C11 standard. Please read manuals about `<math.h>` and `<fenv.h>` for the C API used. If possible, do not directly write long hex/bin literals, instead generate them with bit operations and write comment to explain it. 
- **C cinding**: Use `ctypes` to do C binding. Note the content of a lot of c macros is implemetation defined, do not assume their value and get their value in Python at runtime from C.
- **CI**: A dockerfile to build this project using `scikit-build-core` without Python ABI compatibility (i.e. `wheel.py-api = "py3"`) in manylinux2014, manylinux_2_28, manylinux_2_34, use `auditwheel` to produced universal package. Do not automatically run docker, due to limited disk space. Use Github CI file to build this project and run test on Win, Mac and Linux, on arm and x86 arch. Make the compiled `.whl` file an artifact in Github CI.
- **IEEE754**: The unbiased means the raw exp num, and the biased means the number you get after ieee764 bias number is applied to raw exp (for denormal, 1 - bias).

## Tools

On `X1-Nano` host, use pyright with `npx --prefix ~/.local/opt/npm/ pyright` and use clang-format with `/usr/bin/clang-format-22` 