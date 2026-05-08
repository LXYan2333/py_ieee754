"""Tests for arithmetic operations: add, sub, mul, div with rounding and exceptions."""

import ctypes as ct

import pytest

from py_ieee754 import (
    F32,
    F64,
    FloatDivByZeroError,
    FloatInexactError,
    FloatInvalidError,
    FloatOverflowError,
    FloatUnderflowError,
    RoundingMode,
    add,
    div,
    math,
    mul,
    sub,
)


class TestBasicArithmetic:
    def test_add(self):
        a = F32(1.5)
        b = F32(2.0)
        assert float(add(a, b)) == pytest.approx(3.5)

    def test_sub(self):
        assert float(sub(F32(3.0), F32(1.0))) == pytest.approx(2.0)

    def test_mul(self):
        assert float(mul(F32(2.0), F32(3.0))) == pytest.approx(6.0)

    def test_div(self):
        assert float(div(F32(7.0), F32(3.0))) == pytest.approx(7.0 / 3.0, rel=1e-6)

    def test_operator_overload(self):
        a = F32(1.5)
        b = a + F32(2.0)
        assert float(b) == pytest.approx(3.5)
        assert type(b) is F32

    def test_neg(self):
        a = -F32(1.5)
        assert float(a) == pytest.approx(-1.5)

    def test_abs(self):
        a = abs(F32(-1.5))
        assert float(a) == pytest.approx(1.5)


class TestTypePromotion:
    def test_f32_plus_f32_yields_f32(self):
        assert type(add(F32(1.0), F32(2.0))) is F32

    def test_f32_plus_f64_yields_f64(self):
        assert type(add(F32(1.0), F64(2.0))) is F64

    def test_f64_plus_f32_yields_f64(self):
        assert type(add(F64(1.0), F32(2.0))) is F64

    def test_f32_plus_float_yields_f32(self):
        assert type(add(F32(1.0), 2.0)) is F32

    def test_float_plus_float_yields_f64(self):
        assert type(add(1.0, 2.0)) is F64


class TestRoundingModes:
    def test_div_downward(self):
        result = div(F32(1.0), F32(3.0), round_mode=RoundingMode.DOWNWARD)
        with_round = div(F32(1.0), F32(3.0), round_mode=RoundingMode.UPWARD)
        assert float(result) < float(with_round)

    def test_div_upward(self):
        result = div(F32(1.0), F32(3.0), round_mode=RoundingMode.UPWARD)
        assert float(result) > 0.333

    def test_add_downward(self):
        a = add(F32(1.0), F32(2.0), round_mode=RoundingMode.DOWNWARD)
        assert float(a) == pytest.approx(3.0)

    def test_subnormal_mul_round_up(self):
        s = F32.from_bits(1)  # smallest positive subnormal
        result = mul(F32(1.5), s, round_mode=RoundingMode.UPWARD)
        assert result.bits == 2

    def test_subnormal_mul_round_down(self):
        s = F32.from_bits(1)
        result = mul(F32(1.5), s, round_mode=RoundingMode.DOWNWARD)
        assert result.bits == 1

    def test_subnormal_mul_round_towardzero(self):
        s = F32.from_bits(1)
        result = mul(F32(1.5), s, round_mode=RoundingMode.TOWARDZERO)
        assert result.bits == 1

    def test_subnormal_mul_round_tonearest(self):
        s = F32.from_bits(1)
        # 1.5 is exactly halfway between 1 and 2; tie → even (2)
        result = mul(F32(1.5), s, round_mode=RoundingMode.TONEAREST)
        assert result.bits == 2

    # ---- fma(1.5, subnormal, 0): same exact result as 1.5 × subnormal ----

    def test_subnormal_fma_round_up(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(1.5), s, ct.c_float(0.0), round_mode=RoundingMode.UPWARD)
        assert F32(result).bits == 2

    def test_subnormal_fma_round_down(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(1.5), s, ct.c_float(0.0), round_mode=RoundingMode.DOWNWARD)
        assert F32(result).bits == 1

    def test_subnormal_fma_round_towardzero(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(1.5), s, ct.c_float(0.0), round_mode=RoundingMode.TOWARDZERO)
        assert F32(result).bits == 1

    def test_subnormal_fma_round_tonearest(self):
        s = F32.from_bits(1).ctypes_value
        # 1.5 × subnormal is exactly halfway between 1 and 2; tie → even (2)
        result = math.fma(ct.c_float(1.5), s, ct.c_float(0.0), round_mode=RoundingMode.TONEAREST)
        assert F32(result).bits == 2

    # ---- fma(0.5, subnormal, 0): exact = 2^-150, halfway between 0 and 1 ----

    def test_half_subnormal_fma_round_up(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(0.5), s, ct.c_float(0.0), round_mode=RoundingMode.UPWARD)
        assert F32(result).bits == 1

    def test_half_subnormal_fma_round_down(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(0.5), s, ct.c_float(0.0), round_mode=RoundingMode.DOWNWARD)
        assert F32(result).bits == 0

    def test_half_subnormal_fma_round_towardzero(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(0.5), s, ct.c_float(0.0), round_mode=RoundingMode.TOWARDZERO)
        assert F32(result).bits == 0

    def test_half_subnormal_fma_round_tonearest(self):
        s = F32.from_bits(1).ctypes_value
        # halfway between 0 and 1; tie → even (0)
        result = math.fma(ct.c_float(0.5), s, ct.c_float(0.0), round_mode=RoundingMode.TONEAREST)
        assert F32(result).bits == 0

    # ---- fma(-0.5, subnormal, 0): exact = -2^-150, halfway between -0 and -1 ----

    def test_neg_half_subnormal_fma_round_up(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-0.5), s, ct.c_float(0.0), round_mode=RoundingMode.UPWARD)
        assert F32(result).bits == 0x80000000  # -0

    def test_neg_half_subnormal_fma_round_down(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-0.5), s, ct.c_float(0.0), round_mode=RoundingMode.DOWNWARD)
        assert F32(result).bits == 0x80000001  # -1 subnormal

    def test_neg_half_subnormal_fma_round_towardzero(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-0.5), s, ct.c_float(0.0), round_mode=RoundingMode.TOWARDZERO)
        assert F32(result).bits == 0x80000000  # -0

    def test_neg_half_subnormal_fma_round_tonearest(self):
        s = F32.from_bits(1).ctypes_value
        # halfway between -0 and -1; tie → even (0), sign negative → -0
        result = math.fma(ct.c_float(-0.5), s, ct.c_float(0.0), round_mode=RoundingMode.TONEAREST)
        assert F32(result).bits == 0x80000000

    # ---- fma(-1.5, subnormal, 0): exact = -(2^-149 + 2^-150), halfway between bits 1 and 2 ----

    def test_neg_one_half_subnormal_fma_round_up(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-1.5), s, ct.c_float(0.0), round_mode=RoundingMode.UPWARD)
        assert F32(result).bits == 0x80000001  # toward +inf = less negative = bit 1

    def test_neg_one_half_subnormal_fma_round_down(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-1.5), s, ct.c_float(0.0), round_mode=RoundingMode.DOWNWARD)
        assert F32(result).bits == 0x80000002  # toward -inf = more negative = bit 2

    def test_neg_one_half_subnormal_fma_round_towardzero(self):
        s = F32.from_bits(1).ctypes_value
        result = math.fma(ct.c_float(-1.5), s, ct.c_float(0.0), round_mode=RoundingMode.TOWARDZERO)
        assert F32(result).bits == 0x80000001  # toward 0 = less negative = bit 1

    def test_neg_one_half_subnormal_fma_round_tonearest(self):
        s = F32.from_bits(1).ctypes_value
        # halfway between bits 1 and 2; tie → even (2)
        result = math.fma(ct.c_float(-1.5), s, ct.c_float(0.0), round_mode=RoundingMode.TONEAREST)
        assert F32(result).bits == 0x80000002

    # ---- 0.5 × subnormal: exact = 0.5 × 2^-149 = 2^-150, halfway between 0 and 1 ----

    def test_half_subnormal_mul_round_up(self):
        s = F32.from_bits(1)
        result = mul(F32(0.5), s, round_mode=RoundingMode.UPWARD)
        assert result.bits == 1

    def test_half_subnormal_mul_round_down(self):
        s = F32.from_bits(1)
        result = mul(F32(0.5), s, round_mode=RoundingMode.DOWNWARD)
        assert result.bits == 0

    def test_half_subnormal_mul_round_towardzero(self):
        s = F32.from_bits(1)
        result = mul(F32(0.5), s, round_mode=RoundingMode.TOWARDZERO)
        assert result.bits == 0

    def test_half_subnormal_mul_round_tonearest(self):
        s = F32.from_bits(1)
        # 0.5 × subnormal = exactly halfway between 0 and 1; tie → even (0)
        result = mul(F32(0.5), s, round_mode=RoundingMode.TONEAREST)
        assert result.bits == 0

    # ---- -0.5 × subnormal: exact = -2^-150, halfway between -0 and -1 ----

    def test_neg_half_subnormal_mul_round_up(self):
        s = F32.from_bits(1)
        result = mul(F32(-0.5), s, round_mode=RoundingMode.UPWARD)
        assert result.bits == 0x80000000  # -0

    def test_neg_half_subnormal_mul_round_down(self):
        s = F32.from_bits(1)
        result = mul(F32(-0.5), s, round_mode=RoundingMode.DOWNWARD)
        assert result.bits == 0x80000001  # -1 subnormal

    def test_neg_half_subnormal_mul_round_towardzero(self):
        s = F32.from_bits(1)
        result = mul(F32(-0.5), s, round_mode=RoundingMode.TOWARDZERO)
        assert result.bits == 0x80000000  # -0

    def test_neg_half_subnormal_mul_round_tonearest(self):
        s = F32.from_bits(1)
        # -0.5 × subnormal = exactly halfway between -0 and -1; tie → even (0), sign negative → -0
        result = mul(F32(-0.5), s, round_mode=RoundingMode.TONEAREST)
        assert result.bits == 0x80000000  # -0

    # ---- -1.5 × subnormal: exact = -(2^-149 + 2^-150), halfway between bits 1 and 2 ----

    def test_neg_one_half_subnormal_mul_round_up(self):
        s = F32.from_bits(1)
        result = mul(F32(-1.5), s, round_mode=RoundingMode.UPWARD)
        assert result.bits == 0x80000001  # toward +inf = less negative = bit 1

    def test_neg_one_half_subnormal_mul_round_down(self):
        s = F32.from_bits(1)
        result = mul(F32(-1.5), s, round_mode=RoundingMode.DOWNWARD)
        assert result.bits == 0x80000002  # toward -inf = more negative = bit 2

    def test_neg_one_half_subnormal_mul_round_towardzero(self):
        s = F32.from_bits(1)
        result = mul(F32(-1.5), s, round_mode=RoundingMode.TOWARDZERO)
        assert result.bits == 0x80000001  # toward 0 = less negative = bit 1

    def test_neg_one_half_subnormal_mul_round_tonearest(self):
        s = F32.from_bits(1)
        # -1.5 × subnormal = exactly halfway between bits 1 and 2; tie → even (2)
        result = mul(F32(-1.5), s, round_mode=RoundingMode.TONEAREST)
        assert result.bits == 0x80000002


class TestExceptionHandling:
    # ---- DivByZero (raises by default) ----

    def test_div_by_zero_raises(self):
        with pytest.raises(FloatDivByZeroError):
            div(F32(1.0), F32.zero())

    def test_div_by_zero_no_raise_with_empty_unsuppressed(self):
        result = div(F32(1.0), F32.zero(), unsuppressed=set())
        assert result.is_inf

    # ---- Inexact (suppressed by default) ----

    def test_inexact_does_not_raise_by_default(self):
        result = div(F32(1.0), F32(3.0))
        assert float(result) == pytest.approx(1.0 / 3.0, rel=1e-6)

    def test_inexact_raises_when_unsuppressed(self):
        with pytest.raises(FloatInexactError):
            div(F32(1.0), F32(3.0), unsuppressed={FloatInexactError})

    # ---- Overflow (raises by default) ----

    def test_overflow_raises(self):
        largest = F32.from_bits(0x7F7FFFFF)  # max finite F32
        with pytest.raises(FloatOverflowError):
            mul(largest, F32(2.0))

    def test_overflow_no_raise_with_empty_unsuppressed(self):
        largest = F32.from_bits(0x7F7FFFFF)
        result = mul(largest, F32(2.0), unsuppressed=set())
        assert result.is_inf

    # ---- Underflow (suppressed by default) ----

    def test_underflow_does_not_raise_by_default(self):
        s = F32.from_bits(1)  # smallest positive subnormal
        result = mul(s, F32(0.5))
        assert result.is_zero

    def test_underflow_raises_when_unsuppressed(self):
        s = F32.from_bits(1)
        with pytest.raises(FloatUnderflowError):
            mul(s, F32(0.5), unsuppressed={FloatUnderflowError})

    # ---- Invalid (suppressed by default) ----

    def test_invalid_does_not_raise_by_default(self):
        result = div(F32.zero(), F32.zero())  # 0/0 → NaN
        assert result.is_nan

    def test_invalid_raises_when_unsuppressed(self):
        with pytest.raises(FloatInvalidError):
            div(F32.zero(), F32.zero(), unsuppressed={FloatInvalidError})

    def test_multiple_exceptions_stored_in_excepts(self):
        largest = F32.from_bits(0x7F7FFFFF)  # max finite F32
        with pytest.raises(FloatOverflowError) as exc_info:
            mul(largest, F32(2.0))
        assert exc_info.value.excepts == {FloatOverflowError, FloatInexactError}


class TestNegAbs:
    def test_neg_bit_op(self):
        a = F32(1.5)
        neg = -a
        assert float(neg) == pytest.approx(-1.5)

    def test_abs_bit_op(self):
        a = abs(F32(-1.5))
        assert float(a) == pytest.approx(1.5)


class TestF64Arithmetic:
    def test_f64_add(self):
        a = F64(1.5)
        b = F64(2.0)
        assert float(add(a, b)) == pytest.approx(3.5)

    def test_f64_div_downward(self):
        result = div(F64(1.0), F64(3.0), round_mode=RoundingMode.DOWNWARD)
        assert float(result) <= 1.0 / 3.0


class TestPromotionEdges:
    def test_only_b_is_ieee(self):
        result = add(1.0, F32(2.0))
        assert type(result) is F32

    def test_both_floats(self):
        result = add(1.0, 2.0)
        assert type(result) is F64

    def test_f32_plus_f32(self):
        assert type(F32(1.0) + F32(2.0)) is F32

    def test_radd_float(self):
        result = 3.0 + F32(2.0)
        assert type(result) is F32

    def test_rsub_float(self):
        result = 3.0 - F32(2.0)
        assert type(result) is F32

    def test_rmul_float(self):
        result = 3.0 * F32(2.0)
        assert type(result) is F32

    def test_rtruediv_float(self):
        result = 3.0 / F32(2.0)
        assert type(result) is F32

    def test_sub_operator(self):
        result = F32(3.0) - F32(1.0)
        assert float(result) == pytest.approx(2.0)

    def test_mul_operator(self):
        result = F32(2.0) * F32(3.0)
        assert float(result) == pytest.approx(6.0)

    def test_truediv_operator(self):
        result = F32(7.0) / F32(2.0)
        assert float(result) == pytest.approx(3.5)

    def test_rsub_operator(self):
        result = 3.0 - F32(1.0)
        assert float(result) == pytest.approx(2.0)

    def test_rmul_operator(self):
        result = 2.0 * F32(3.0)
        assert float(result) == pytest.approx(6.0)

    def test_only_b_is_ieee_sub(self):
        result = sub(1.0, F32(2.0))
        assert type(result) is F32


class TestFloorDivMod:
    def test_floordiv(self):
        assert float(F32(7.0) // F32(3.0)) == 2.0

    def test_floordiv_negative(self):
        assert float(F32(-7.0) // F32(3.0)) == -3.0

    def test_mod(self):
        assert float(F32(7.0) % F32(3.0)) == 1.0

    def test_mod_negative(self):
        assert float(F32(-7.0) % F32(3.0)) == 2.0

    def test_rfloordiv(self):
        assert float(7.0 // F32(3.0)) == 2.0

    def test_rmod(self):
        assert float(7.0 % F32(3.0)) == 1.0

    def test_floordiv_f64(self):
        assert float(F64(10.0) // F64(3.0)) == 3.0

    def test_mod_f64(self):
        assert float(F64(10.0) % F64(3.0)) == 1.0

    def test_floordiv_type_promotion(self):
        assert type(F32(7.0) // F64(3.0)) is F64

    def test_mod_type_promotion(self):
        assert type(F32(7.0) % F64(3.0)) is F64
