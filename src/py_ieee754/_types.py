"""IEEE 754 floating-point types.

Provides the abstract base class `IEEE754` and concrete implementations `F32`
and `F64` with bit-level access, classification, and construction from float,
int (bit-cast), and string representations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import ctypes as ct
from typing import ClassVar, Self

# ---- Type aliases ----

type ct_float_type = type[ct.c_float] | type[ct.c_double]
type ct_uint_type = type[ct.c_uint32] | type[ct.c_uint64]


class IEEE754(ABC):
    """Abstract base for IEEE 754 binary floating-point types.

    Provides bit-level field access, classification predicates, special-value
    factories, and arithmetic operators for ``binary32`` (:class:`F32`) and
    ``binary64`` (:class:`F64`) representations.

    Subclasses must define the per-format class variables::

        _val_t      — ctypes type (``ct.c_float`` or ``ct.c_double``)
        _uint_t     — same-width unsigned ctypes type
        _bias       — exponent bias (127 for f32, 1023 for f64)
        _exp_bits   — slice for the exponent field (e.g. ``slice(1, 9)``)
        _sig_bits   — slice for the significand field (e.g. ``slice(9, 32)``)

    Additionally, subclasses must implement the abstract property
    :meth:`ctypes_value` with the appropriate narrowed return type.

    Construction is dispatched by :meth:`__new__`

    Objects are **immutable** — methods that logically mutate the value return a
    new instance.
    """

    __slots__ = ("_value", "_as_int")

    # ---- Per-subclass configuration ----

    _val_t: ClassVar[type[ct.c_float] | type[ct.c_double]]
    _uint_t: ClassVar[type[ct.c_uint32] | type[ct.c_uint64]]
    _bias: ClassVar[int]
    _exp_bits: ClassVar[slice]
    _sig_bits: ClassVar[slice]

    # ---- Derived class attributes ----

    @classmethod
    def _total_bits(cls) -> int:
        return cls._sig_bits.stop

    @classmethod
    def _exp_width(cls) -> int:
        return cls._exp_bits.stop - cls._exp_bits.start

    @classmethod
    def _sig_width(cls) -> int:
        return cls._sig_bits.stop - cls._sig_bits.start

    @classmethod
    def _exp_mask(cls) -> int:
        exp_width = cls._exp_width()
        shift = cls._total_bits() - cls._exp_bits.stop
        return ((1 << exp_width) - 1) << shift

    @classmethod
    def _sig_mask(cls) -> int:
        sig_width = cls._sig_width()
        return (1 << sig_width) - 1

    @classmethod
    def _exp_shift(cls) -> int:
        return cls._total_bits() - cls._exp_bits.stop

    @classmethod
    def _max_exp(cls) -> int:
        return (1 << cls._exp_width()) - 1

    # ---- Instance attributes ----

    _value: ct.c_float | ct.c_double
    _as_int: int

    # ---- Construction ----

    def __new__(cls, value: float | int | str | ct.c_float | ct.c_double) -> IEEE754:
        """Construct an IEEE754 instance from *value*.

        Dispatches based on the Python type of *value*

        ==============  =================================
        Argument type   Behaviour
        ==============  =================================
        :class:`float`  Round-trip through ctypes
        :class:`int`    Bit-cast (interpret as raw bit pattern)
        :class:`str`    Parse binary (``0b...``), hex (``0x...``), hex-float (``0x1.8p+0``), or decimal
        ``ct.c_float``  Preserve exact bit pattern (``→ F32``)
        ``ct.c_double`` Preserve exact bit pattern (``→ F64``)
        ==============  =================================
        """
        match value:
            case float():
                return cls._from_float(value)
            case int():
                return cls._from_bits(value)
            case str():
                return cls._from_str(value)
            case ct.c_float() | ct.c_double():
                return cls._from_ctypes(value)
            case _:
                raise TypeError(f"cannot construct {cls.__name__} from {type(value).__name__}")

    @classmethod
    def _from_float(cls, value: float) -> Self:
        c_val = cls._val_t(value)
        c_uint = cls._uint_t.from_buffer_copy(c_val)
        bits = c_uint.value
        return cls._make(c_val, bits)

    @classmethod
    def _from_bits(cls, bits: int) -> Self:
        c_uint = cls._uint_t(bits)
        c_val = cls._val_t.from_buffer_copy(c_uint)
        return cls._make(c_val, bits)

    @classmethod
    def _from_str(cls, s: str) -> Self:
        s = s.strip()
        if s.startswith("0b"):
            return cls._from_bits(int(s.removeprefix("0b"), 2))
        if s.startswith("0x") and "p" not in s:
            return cls._from_bits(int(s, 16))
        if s.startswith("0x") or s.startswith("-0x"):
            return cls._from_float(float.fromhex(s))
        return cls._from_float(float(s))

    @classmethod
    def _from_ctypes(cls, value: ct.c_float | ct.c_double) -> Self:
        if not isinstance(value, cls._val_t):
            raise TypeError(f"cannot construct {cls.__name__} from {type(value).__name__}")
        c_uint = cls._uint_t.from_buffer_copy(value)
        return cls._make(value, c_uint.value)

    @classmethod
    def _make(cls, c_val: ct.c_float | ct.c_double, bits: int) -> Self:
        obj = object.__new__(cls)
        obj._value = c_val
        obj._as_int = bits
        return obj

    @classmethod
    def from_bits(cls, bits: int) -> Self:
        """Create from a raw integer bit pattern (bit-cast).

        The *bits* are interpreted as the complete IEEE 754 encoding (sign,
        exponent, and significand fields).  No value conversion is performed.

        >>> F32.from_bits(0x3FC00000)
        F32(0b0_01111111_10000000000000000000000)
        """
        return cls._from_bits(bits)

    @staticmethod
    def from_ctypes(value: ct.c_float | ct.c_double) -> IEEE754:
        """Create an :class:`F32` or :class:`F64` from a ctypes float or double.

        The exact bit pattern is preserved (no value conversion).
        Dispatch is based on the ctypes type:

        * ``ct.c_float()`` → :class:`F32`
        * ``ct.c_double()`` → :class:`F64`

        >>> IEEE754.from_ctypes(ct.c_float(1.5))
        F32(0b0_01111111_10000000000000000000000)
        """
        match value:
            case ct.c_float():
                return F32._from_ctypes(value)
            case ct.c_double():
                return F64._from_ctypes(value)
            case _:
                raise TypeError(f"cannot construct IEEE754 from {type(value).__name__}")

    # ---- Conversion ----

    @property
    @abstractmethod
    def ctypes_value(self) -> ct.c_float | ct.c_double:
        """Return the underlying ctypes value (``ct.c_float`` or ``ct.c_double``)."""

    @property
    def value(self) -> float:
        """Return the value as a Python float."""
        return self._value.value

    def __float__(self) -> float:
        """Return the value as a Python :class:`float`."""
        return self.value

    def __int__(self) -> int:
        """Truncate toward zero, returning the integer part."""
        return int(self.value)

    @property
    def bits(self) -> int:
        """Raw bit pattern as an :class:`int`."""
        return self._as_int

    @property
    def bin(self) -> str:
        """Bit pattern as a binary string (e.g. ``"0b00111111..."``)."""
        return f"0b{self._as_int:0{self._total_bits()}b}"

    @property
    def hex(self) -> str:
        """Bit pattern as a hex string (e.g. ``"0x3fc00000"``)."""
        total = self._total_bits()
        return f"0x{self._as_int:0{total // 4}x}"

    @property
    def hex_literal(self) -> str:
        """C/C++ hex literal for the bit pattern with type suffix.

        F32 → ``"0x3FC00000U"``,  F64 → ``"0x3FF8000000000000ULL"``.
        """
        total = self._total_bits()
        suffix = "ULL" if total == 64 else "U"
        return f"{self.hex}{suffix}"

    @property
    def float_hex(self) -> str:
        """IEEE 754 hex-float representation (e.g. ``"0x1.8000000000000p+0"`` for 1.5).

        Returns ``"nan"``, ``"inf"``, or ``"0x0.0p+0"`` for special values.
        """
        return self.value.hex()

    @property
    def cxx_bitcast(self) -> str:
        """C++20 ``std::bit_cast`` expression for this value.

        >>> F64(1.5).cxx_bitcast
        'std::bit_cast<double>(0x3FF8000000000000ULL)'
        """
        c_name = "double" if self._total_bits() == 64 else "float"
        return f"std::bit_cast<{c_name}>({self.hex_literal})"

    def __repr__(self) -> str:
        """Detailed representation: ``F32(0b0_01111111_1000...)``."""
        s, e, m = self.decompose_bin()
        return f"{type(self).__name__}(0b{s}_{e}_{m})"

    def __str__(self) -> str:
        """Human-readable decimal string of the value."""
        return str(self.value)

    # ---- Width ----

    @property
    def size_bits(self) -> int:
        """Total number of bits in the representation."""
        return self._total_bits()

    # ---- Decomposition / construction ----

    def decompose(self) -> tuple[int, int, int]:
        """Return ``(sign, biased_exponent, significand)`` as raw :class:`int` values.

        See :meth:`decompose_bin` for a zero-padded binary string version.
        """
        return self.sign, self.exponent, self.significand

    def decompose_bin(self) -> tuple[str, str, str]:
        """Return ``(sign, biased_exponent, significand)`` as zero-padded binary strings.

        See :meth:`decompose` for the raw integer version.
        """
        exp_w = self._exp_width()
        sig_w = self._sig_width()
        return (
            str(self.sign),
            format(self.exponent, f"0{exp_w}b"),
            format(self.significand, f"0{sig_w}b"),
        )

    @classmethod
    def from_components(cls, sign: int | str, exponent: int | str, significand: int | str) -> Self:
        """Create from raw IEEE 754 fields.

        *sign* is the sign bit (0 or 1), *exponent* is the **biased** (stored)
        exponent, and *significand* is the trailing significand without the
        implicit leading bit.

        Each argument may be an :class:`int` or a binary string (e.g. ``"0"``,
        ``"01111111"``).

        >>> F32.from_components(0, 127, 0x400000)
        F32(0b0_01111111_10000000000000000000000)
        """
        s = int(sign, 2) if isinstance(sign, str) else sign
        e = int(exponent, 2) if isinstance(exponent, str) else exponent
        m = int(significand, 2) if isinstance(significand, str) else significand
        total = cls._total_bits()
        bits = (s << (total - 1)) | (e << cls._exp_shift()) | m
        return cls._from_bits(bits)

    @classmethod
    def from_bin_str(cls, s: str) -> Self:
        """Create from a binary string of exactly ``total_bits`` bits.

        Raises :class:`ValueError` if the string length does not match the
        format width (32 for F32, 64 for F64).
        """
        total = cls._total_bits()
        if len(s) != total:
            raise ValueError(f"expected {total} bits, got {len(s)}")
        return cls._from_bits(int(s, 2))

    def with_sign(self, sign: int | str) -> Self:
        """Return a new object with *sign* replaced; exponent and significand unchanged.

        *sign* may be 0, 1, or a binary string ``"0"`` / ``"1"``.
        """
        _, e, m = self.decompose()
        return type(self).from_components(sign, e, m)

    def with_exponent(self, exponent: int | str) -> Self:
        """Return a new object with the **biased** exponent replaced.

        *exponent* may be an :class:`int` or a binary string of the correct
        width (e.g. ``"01111111"`` for F32).

        See :meth:`with_sign` and :meth:`with_significand`.
        """
        s, _, m = self.decompose()
        return type(self).from_components(s, exponent, m)

    def with_significand(self, significand: int | str) -> Self:
        """Return a new object with the trailing significand replaced.

        *significand* may be an :class:`int` or a binary string of the correct
        width (e.g. ``"10000000000000000000000"`` for F32).

        See :meth:`with_sign` and :meth:`with_exponent`.
        """
        s, e, _ = self.decompose()
        return type(self).from_components(s, e, significand)

    # ---- Field access ----

    @property
    def sign(self) -> int:
        """Sign bit: 0 for positive, 1 for negative."""
        return (self._as_int >> (self._total_bits() - 1)) & 1

    @property
    def exponent(self) -> int:
        """Biased (stored) exponent field as an integer.

        This is the raw exponent value as stored in the bit pattern,
        **not** bias-adjusted.  For F32, ``1.5`` has a biased exponent of
        127 (``0x7F``).
        """
        return (self._as_int & self._exp_mask()) >> self._exp_shift()

    @property
    def significand(self) -> int:
        """Trailing significand (mantissa) bits.

        Does **not** include the implicit leading bit for normal numbers.
        """
        return self._as_int & self._sig_mask()

    @property
    def exponent_biased(self) -> int:
        """Mathematical exponent after bias adjustment.

        For normal numbers this is ``exponent - bias``.  For subnormals it
        returns ``1 - bias``, per IEEE 754 convention.
        """
        if self.is_subnormal:
            return 1 - self._bias
        return self.exponent - self._bias

    # ---- Classification ----

    @property
    def is_nan(self) -> bool:
        """Whether the value is a NaN (quiet or signalling).

        An IEEE 754 NaN has the maximum biased exponent and a non-zero
        significand.
        """
        return self.exponent == self._max_exp() and self.significand != 0

    @property
    def is_snan(self) -> bool:
        """Whether the value is a **signalling** NaN.

        Signalling NaNs have the significand MSB **clear** (0), which
        distinguishes them from quiet NaNs.

        https://en.wikipedia.org/wiki/NaN#Encoding
            In practice, the most significant bit of the trailing significand
            field determined whether a NaN is signaling or quiet. most
            processors set the signaling/quiet bit to non-zero if the NaN is
            quiet, and to zero if the NaN is signaling.

        See :meth:`is_qnan` and :meth:`nan`.
        """
        if not self.is_nan:
            return False
        return (self.significand & (1 << (self._sig_width() - 1))) == 0

    @property
    def is_qnan(self) -> bool:
        """Whether the value is a **quiet** NaN.

        Quiet NaNs have the significand MSB **set** (1).  They do not raise
        floating-point exceptions when used in arithmetic.

        https://en.wikipedia.org/wiki/NaN#Encoding
            In practice, the most significant bit of the trailing significand
            field determined whether a NaN is signaling or quiet. most
            processors set the signaling/quiet bit to non-zero if the NaN is
            quiet, and to zero if the NaN is signaling.

        See :meth:`is_snan` and :meth:`nan`.
        """
        if not self.is_nan:
            return False
        return (self.significand & (1 << (self._sig_width() - 1))) != 0

    @property
    def is_inf(self) -> bool:
        """Whether the value is positive or negative infinity."""
        return self.exponent == self._max_exp() and self.significand == 0

    @property
    def is_zero(self) -> bool:
        """Whether the value is positive or negative zero."""
        return self.exponent == 0 and self.significand == 0

    @property
    def is_subnormal(self) -> bool:
        """Whether the value is a subnormal number.

        Subnormals have a biased exponent of 0 and a non-zero significand.
        They fill the underflow gap around zero.
        """
        return self.exponent == 0 and self.significand != 0

    @property
    def is_normal(self) -> bool:
        """Whether the value is a normal (non-zero, non-subnormal) finite number."""
        return 0 < self.exponent < self._max_exp()

    @property
    def is_finite(self) -> bool:
        """Whether the value is finite — neither NaN nor infinity."""
        return not (self.is_nan or self.is_inf)

    # ---- Special values ----

    @classmethod
    def nan(cls) -> Self:
        """Return a **quiet NaN** with a canonical payload (significand MSB set).

        Quiet NaNs propagate through arithmetic without raising the invalid
        exception.

        https://en.wikipedia.org/wiki/NaN#Encoding
            In practice, the most significant bit of the trailing significand
            field determined whether a NaN is signaling or quiet. most
            processors set the signaling/quiet bit to non-zero if the NaN is
            quiet, and to zero if the NaN is signaling.

        See :meth:`snan` for signalling NaN.
        """
        return cls.from_components(0, cls._max_exp(), 1 << (cls._sig_width() - 1))

    @classmethod
    def snan(cls) -> Self:
        """Return a **signalling NaN** with a minimal payload (LSB = 1).

        Signalling NaNs raise the invalid exception when used in arithmetic.

        https://en.wikipedia.org/wiki/NaN#Encoding
            In practice, the most significant bit of the trailing significand
            field determined whether a NaN is signaling or quiet. most
            processors set the signaling/quiet bit to non-zero if the NaN is
            quiet, and to zero if the NaN is signaling.

        See :meth:`nan` for quiet NaN.
        """
        return cls.from_components(0, cls._max_exp(), 1)

    @classmethod
    def inf(cls, negative: bool = False) -> Self:
        """Return positive infinity, or negative infinity if *negative* is ``True``."""
        return cls.from_components(int(negative), cls._max_exp(), 0)

    @classmethod
    def zero(cls, negative: bool = False) -> Self:
        """Return positive zero, or negative zero if *negative* is ``True``."""
        return cls.from_components(int(negative), 0, 0)

    # ---- Comparison ----

    def __eq__(self, other: object) -> bool:
        """Return ``self == other``.

        Comparison is done on the underlying :class:`float` value.  Returns
        ``NotImplemented`` for unsupported types.
        """
        a = self._value.value
        if isinstance(other, IEEE754):
            return a == other._value.value
        if isinstance(other, float):
            return a == other
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return ``self < other``."""
        a = self._value.value
        if isinstance(other, IEEE754):
            return a < other._value.value
        if isinstance(other, float):
            return a < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """Return ``self <= other``."""
        a = self._value.value
        if isinstance(other, IEEE754):
            return a <= other._value.value
        if isinstance(other, float):
            return a <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        """Return ``self > other``."""
        a = self._value.value
        if isinstance(other, IEEE754):
            return a > other._value.value
        if isinstance(other, float):
            return a > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        """Return ``self >= other``."""
        a = self._value.value
        if isinstance(other, IEEE754):
            return a >= other._value.value
        if isinstance(other, float):
            return a >= other
        return NotImplemented

    def __hash__(self) -> int:
        """Hash of the underlying float value."""
        return hash(self._value.value)

    # ---- Arithmetic operators (delegate to _arithmetic.py) ----

    def __neg__(self) -> Self:
        """Return ``-self`` (flip the sign bit)."""
        return self.with_sign(int(not self.sign))

    def __abs__(self) -> Self:
        """Return ``abs(self)`` (clear the sign bit)."""
        return self.with_sign(0)

    def __add__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``self + other``.  Delegates to :func:`~py_ieee754.add`."""
        from py_ieee754._arithmetic import add

        return add(self, other)

    def __radd__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``other + self``.  Delegates to :func:`~py_ieee754.add`."""
        from py_ieee754._arithmetic import add

        return add(other, self)

    def __sub__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``self - other``.  Delegates to :func:`~py_ieee754.sub`."""
        from py_ieee754._arithmetic import sub

        return sub(self, other)

    def __rsub__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``other - self``.  Delegates to :func:`~py_ieee754.sub`."""
        from py_ieee754._arithmetic import sub

        return sub(other, self)

    def __mul__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``self * other``.  Delegates to :func:`~py_ieee754.mul`."""
        from py_ieee754._arithmetic import mul

        return mul(self, other)

    def __rmul__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``other * self``.  Delegates to :func:`~py_ieee754.mul`."""
        from py_ieee754._arithmetic import mul

        return mul(other, self)

    def __truediv__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``self / other``.  Delegates to :func:`~py_ieee754.div`."""
        from py_ieee754._arithmetic import div

        return div(self, other)

    def __rtruediv__(self, other: IEEE754 | float) -> IEEE754:
        """Return ``other / self``.  Delegates to :func:`~py_ieee754.div`."""
        from py_ieee754._arithmetic import div

        return div(other, self)


class F64(IEEE754):
    """IEEE 754 binary64 (double precision) floating-point number.

    64 bits: 1 sign + 11 exponent + 52 significand.  Bias = 1023.
    """

    _val_t: ClassVar = ct.c_double
    _uint_t: ClassVar = ct.c_uint64
    _bias: ClassVar = 1023
    _exp_bits: ClassVar = slice(1, 12)
    _sig_bits: ClassVar = slice(12, 64)

    @property
    def ctypes_value(self) -> ct.c_double:
        """Return the underlying :class:`ctypes.c_double`."""
        v = self._value
        assert isinstance(v, ct.c_double)
        return v


class F32(IEEE754):
    """IEEE 754 binary32 (single precision) floating-point number.

    32 bits: 1 sign + 8 exponent + 23 significand.  Bias = 127.
    """

    _val_t: ClassVar = ct.c_float
    _uint_t: ClassVar = ct.c_uint32
    _bias: ClassVar = 127
    _exp_bits: ClassVar = slice(1, 9)
    _sig_bits: ClassVar = slice(9, 32)

    @property
    def ctypes_value(self) -> ct.c_float:
        """Return the underlying :class:`ctypes.c_float`."""
        v = self._value
        assert isinstance(v, ct.c_float)
        return v
