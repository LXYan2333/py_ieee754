"""Tests for IEEE 754 types: construction, field access, classification, conversion."""

import ctypes as ct
import math

import numpy as np
import pytest

from py_ieee754 import F32, F64, IEEE754


class TestConstruction:
    def test_from_float(self):
        a = F32(1.5)
        assert float(a) == pytest.approx(1.5)
        b = F64(-3.14)
        assert float(b) == pytest.approx(-3.14)

    def test_from_int_bitcast(self):
        a = F32(0x3FC00000)  # 1.5
        assert float(a) == pytest.approx(1.5)

    def test_from_bits(self):
        a = F32.from_bits(0x40490FDB)
        assert float(a) == pytest.approx(3.1415927410125732)

    def test_from_hex_str(self):
        a = F32("0x3FC00000")
        assert float(a) == pytest.approx(1.5)

    def test_from_bin_str(self):
        a = F32("0b00111111110000000000000000000000")
        assert float(a) == pytest.approx(1.5)

    def test_from_float_hex_str(self):
        a = F64("0x1.8p+0")
        assert float(a) == 1.5

    def test_from_decimal_str(self):
        a = F32("3.14")
        assert float(a) == pytest.approx(3.14, rel=1e-6)

    def test_from_none(self):
        assert F32(None).is_zero
        assert F32(None).bits == 0
        assert F64(None).is_zero
        assert F64(None).bits == 0
        assert F32().is_zero
        assert F32().bits == 0
        assert F64().is_zero
        assert F64().bits == 0

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            F32([])


class TestFieldAccess:
    def test_sign(self):
        assert F32(1.5).sign == 0
        assert F32(-1.5).sign == 1

    def test_biased_exponent(self):
        # 1.5 = 0x3FC00000 = 0b0 01111111 10000000000000000000000, biased exponent = 0x7F = 127
        assert F32(1.5).biased_exponent == 127
        assert F32(0.5).biased_exponent == 126  # 0.5 = 2**-1, bias 127-1=126

    def test_significand(self):
        # 1.5 significand: 0x400000 (23 bits)
        assert F32(1.5).significand == 0x400000

    def test_exponent(self):
        assert F32(1.5).exponent == 0  # 127 - 127
        assert F64(1.5).exponent == 0  # 1023 - 1023
        # subnormal
        s = F32.from_bits(1)
        assert s.exponent == 1 - 127  # 1 - bias


class TestClassification:
    def test_is_nan(self):
        assert F32.nan().is_nan
        assert math.isnan(F64.nan().value)
        assert not F32(1.0).is_nan

    def test_is_snan_qnan(self):
        nan = F32.nan()
        assert nan.is_qnan
        assert not nan.is_snan
        snan = F32.snan()
        assert snan.is_snan
        assert not snan.is_qnan
        # non-NaN values
        assert not F32(1.0).is_snan
        assert not F32(1.0).is_qnan

    def test_is_inf(self):
        assert F32.inf().is_inf
        assert F32.inf(negative=True).is_inf

    def test_is_zero(self):
        assert F32.zero().is_zero
        assert F32.zero(negative=True).is_zero
        assert not F32(1.0).is_zero

    def test_is_subnormal(self):
        # Smallest positive subnormal f32
        s = F32.from_bits(1)
        assert s.is_subnormal
        assert not F32(1.0).is_subnormal

    def test_is_normal(self):
        assert F32(1.0).is_normal
        assert not F32.nan().is_normal
        assert not F32.inf().is_normal

    def test_is_finite(self):
        assert F32(1.0).is_finite
        assert not F32.nan().is_finite
        assert not F32.inf().is_finite


class TestConversion:
    def test_float(self):
        assert float(F32(3.14)) == pytest.approx(3.14, rel=1e-6)

    def test_int_truncates(self):
        assert int(F32(3.14)) == 3

    def test_bits_property(self):
        assert F32(1.5).bits == 0x3FC00000

    def test_bin(self):
        b = F32(1.5).bin
        assert b.startswith("0b")
        assert len(b) == 34  # "0b" + 32 bits

    def test_hex(self):
        assert F32(1.5).hex == "0x3fc00000"
        assert F64(1.5).hex == "0x3ff8000000000000"

    def test_hex_literal(self):
        assert F32(1.5).hex_literal == "0x3fc00000U"
        assert F64(1.5).hex_literal == "0x3ff8000000000000ULL"

    # ---- f64 ----

    def test_f64_float_hex_subnormal(self):
        s = F64.from_bits(1)
        assert float.fromhex(s.float_hex) == s.value

    def test_f64_float_hex_neg_subnormal(self):
        s = F64.from_bits(0x8000000000000001)
        assert float.fromhex(s.float_hex) == s.value

    def test_f64_float_hex_normal(self):
        a = F64(1.5)
        assert float.fromhex(a.float_hex) == a.value

    def test_f64_float_hex_neg_normal(self):
        a = F64(-3.14)
        assert float.fromhex(a.float_hex) == a.value

    def test_f64_float_hex_zero(self):
        assert float.fromhex(F64.zero().float_hex) == 0.0

    def test_f64_float_hex_neg_zero(self):
        v = float.fromhex(F64.zero(negative=True).float_hex)
        assert v == 0.0 and str(v) == "-0.0"

    def test_f64_float_hex_inf(self):
        assert float.fromhex(F64.inf().float_hex) == float("inf")

    def test_f64_float_hex_neg_inf(self):
        assert float.fromhex(F64.inf(negative=True).float_hex) == float("-inf")

    def test_f64_float_hex_nan(self):
        assert math.isnan(float.fromhex(F64.nan().float_hex))

    def test_f64_float_hex_neg_nan(self):
        assert math.isnan(float.fromhex(F64.snan().float_hex))

    # ---- f32 ----

    def test_f32_float_hex_subnormal(self):
        s = F32.from_bits(1)
        assert float.fromhex(s.float_hex) == s.value

    def test_f32_float_hex_neg_subnormal(self):
        s = F32.from_bits(0x80000001)
        assert float.fromhex(s.float_hex) == s.value

    def test_f32_float_hex_normal(self):
        a = F32(1.5)
        assert float.fromhex(a.float_hex) == a.value

    def test_f32_float_hex_neg_normal(self):
        a = F32(-3.14)
        assert float.fromhex(a.float_hex) == a.value

    def test_f32_float_hex_zero(self):
        assert float.fromhex(F32.zero().float_hex) == 0.0

    def test_f32_float_hex_neg_zero(self):
        v = float.fromhex(F32.zero(negative=True).float_hex)
        assert v == 0.0 and str(v) == "-0.0"

    def test_f32_float_hex_inf(self):
        assert float.fromhex(F32.inf().float_hex) == float("inf")

    def test_f32_float_hex_neg_inf(self):
        assert float.fromhex(F32.inf(negative=True).float_hex) == float("-inf")

    def test_f32_float_hex_nan(self):
        assert math.isnan(float.fromhex(F32.nan().float_hex))

    def test_f32_float_hex_neg_nan(self):
        assert math.isnan(float.fromhex(F32.snan().float_hex))

    def test_cxx_bitcast(self):
        c = F32(1.5).cxx_bitcast
        assert "std::bit_cast<float>" in c
        assert "0x3fc00000U" in c

    def test_ctypes_value(self):
        a = F32(1.5).ctypes_value
        assert isinstance(a, ct.c_float)
        assert a.value == pytest.approx(1.5)


class TestComparison:
    def test_eq(self):
        assert F32(1.5) == F64(1.5)
        assert F32(1.5) == 1.5
        assert F32(1.5) != F32(2.0)

    def test_lt(self):
        assert F32(1.0) < F32(2.0)
        assert F32(1.0) < 2.0

    def test_nan_compare(self):
        assert F32.nan() != F32.nan()
        assert not (F32.nan() < 0.0)

    def test_zero_compare(self):
        assert F32.zero() == F32.zero(negative=True)
        assert F32.zero() >= F32.zero(negative=True)

    def test_hash_equal(self):
        assert hash(F32(1.5)) == hash(F64(1.5))


class TestSpecialValues:
    def test_nan(self):
        n = F32.nan()
        assert n.is_nan
        assert float(n) != float(n)  # NaN != NaN

    def test_inf(self):
        assert float(F32.inf()) == float("inf")

    def test_zero(self):
        assert float(F32.zero()) == 0.0
        assert float(F32.zero(negative=True)) == -0.0


class TestDecompose:
    def test_decompose(self):
        s, e, m = F32(1.5).decompose()
        assert s == 0
        assert e == 127
        assert m == 0x400000

    def test_decompose_bin(self):
        sb, eb, mb = F32(1.5).decompose_bin()
        assert sb == "0"
        assert eb == "01111111"
        assert mb == "10000000000000000000000"


class TestFromComponents:
    def test_from_components_int(self):
        a = F32.from_components(0, 127, 0x400000)
        assert float(a) == pytest.approx(1.5)

    def test_from_components_str(self):
        a = F32.from_components("0", "01111111", "10000000000000000000000")
        assert float(a) == pytest.approx(1.5)

    def test_from_bin_str(self):
        a = F32.from_bin_str("00111111110000000000000000000000")
        assert float(a) == pytest.approx(1.5)

    def test_from_bin_str_wrong_length(self):
        with pytest.raises(ValueError):
            F32.from_bin_str("123")


class TestWithFields:
    def test_with_sign(self):
        a = F32(1.5).with_sign(1)
        assert float(a) == pytest.approx(-1.5)

    def test_with_biased_exponent(self):
        a = F32(1.5).with_biased_exponent(128)
        assert float(a) == pytest.approx(3.0)

    def test_with_significand(self):
        a = F32(1.5).with_significand(0x200000)
        assert float(a) == pytest.approx(1.25)


class TestRepr:
    def test_repr(self):
        r = repr(F32(1.5))
        assert "F32(" in r
        assert "0" in r  # sign
        assert "01111111" in r  # exponent
        assert "10000000000000000000000" in r  # significand


class TestMatchCaseConstruction:
    def test_match_float(self):
        a = F32(1.5)
        assert float(a) == pytest.approx(1.5)

    def test_match_int(self):
        a = F32(0x3FC00000)
        assert float(a) == pytest.approx(1.5)

    def test_match_str_bin(self):
        a = F32("0b00111111110000000000000000000000")
        assert float(a) == pytest.approx(1.5)

    def test_match_else_raises(self):
        with pytest.raises(TypeError):
            F32([])


class TestAllComparisons:
    def test_comparison_ops(self):
        a = F32(1.5)
        b = F32(2.0)
        assert a <= b
        assert a <= F32(1.5)
        assert b > a
        assert b >= a
        assert a >= F32(1.5)

    def test_comparison_with_float(self):
        a = F32(1.5)
        assert a <= 1.5
        assert a >= 1.5
        assert a > 1.0
        assert a < 2.0

    def test_comparison_with_non_ieee754_returns_notimplemented(self):
        assert (F32(1.5).__eq__("not_a_number")) is NotImplemented  # type: ignore[arg-type]
        assert (F32(1.5).__lt__("x")) is NotImplemented  # type: ignore[arg-type]
        assert (F32(1.5).__le__("x")) is NotImplemented  # type: ignore[arg-type]
        assert (F32(1.5).__gt__("x")) is NotImplemented  # type: ignore[arg-type]
        assert (F32(1.5).__ge__("x")) is NotImplemented  # type: ignore[arg-type]

    def test_le_float(self):
        assert F32(1.5) <= 1.5

    def test_gt_float(self):
        assert F32(2.0) > 1.0

    def test_ge_float(self):
        assert F32(1.5) >= 1.0

    def test_le_ieee(self):
        assert F32(1.0) <= F32(2.0)

    def test_gt_ieee(self):
        assert F32(2.0) > F32(1.0)

    def test_ge_ieee(self):
        assert F32(2.0) >= F32(1.0)


class TestFloatHexSpecialValues:
    def test_nan_float_hex(self):
        assert F32.nan().float_hex == "nan"

    def test_inf_float_hex(self):
        assert F32.inf().float_hex == "inf"
        assert F32.inf(negative=True).float_hex == "-inf"

    def test_zero_float_hex(self):
        assert F32.zero().float_hex == "0x0.0p+0"
        assert F32.zero(negative=True).float_hex == "-0x0.0p+0"


class TestF64Conversions:
    def test_f64_cxx_bitcast(self):
        c = F64(1.5).cxx_bitcast
        assert "std::bit_cast<double>" in c
        assert "0x3ff8000000000000ULL" in c

    def test_str(self):
        assert str(F32(1.5)) == "1.5"

    def test_size_bits(self):
        assert F32(1.5).size_bits == 32
        assert F64(1.5).size_bits == 64

    def test_exp_bits(self):
        assert F32(1.5).exp_len == 8
        assert F64(1.5).exp_len == 11

    def test_sig_bits(self):
        assert F32(1.5).sig_len == 23
        assert F64(1.5).sig_len == 52


class TestCtypesConstruction:
    def test_from_ctypes_f32(self):
        result = IEEE754.from_ctypes(ct.c_float(1.5))
        assert type(result) is F32
        assert float(result) == pytest.approx(1.5)

    def test_from_ctypes_f64(self):
        result = IEEE754.from_ctypes(ct.c_double(1.5))
        assert type(result) is F64
        assert float(result) == pytest.approx(1.5)

    def test_f32_from_ctypes_float(self):
        result = F32(ct.c_float(1.5))
        assert type(result) is F32
        assert float(result) == pytest.approx(1.5)

    def test_f64_from_ctypes_double(self):
        result = F64(ct.c_double(1.5))
        assert type(result) is F64
        assert float(result) == pytest.approx(1.5)

    def test_f32_from_wrong_ctypes_raises(self):
        with pytest.raises(TypeError):
            F32(ct.c_double(1.5))

    def test_f64_from_wrong_ctypes_raises(self):
        with pytest.raises(TypeError):
            F64(ct.c_float(1.5))

    def test_f64_ctypes_value(self):
        v = F64(1.5).ctypes_value
        assert isinstance(v, ct.c_double)
        assert v.value == pytest.approx(1.5)

    def test_from_ctypes_bad_type_raises(self):
        with pytest.raises(TypeError):
            IEEE754.from_ctypes(42)  # type: ignore[arg-type]


class TestNumpyDtype:
    def test_f32_dtype(self):
        assert F32(1.5).__numpy_dtype__ == np.dtype(np.float32)

    def test_f64_dtype(self):
        assert F64(1.5).__numpy_dtype__ == np.dtype(np.float64)

    def test_array_with_f32_dtype(self):
        arr = np.array([1.5, 2.5], dtype=F32)  # F32 as dtype spec
        assert arr.dtype == np.float32
        assert arr[0] == np.float32(1.5)

    def test_array_with_f64_dtype(self):
        arr = np.array([1.5, 2.5], dtype=F64)
        assert arr.dtype == np.float64
