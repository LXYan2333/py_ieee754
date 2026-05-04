# py_ieee754

[![cov](https://lxyan2333.github.io/py_ieee754/badges/coverage.svg)](https://github.com/LXYan2333/py_ieee754/actions)

IEEE 754 float number python module with bit-operation and round arithmetic support.

## Usage

```python
>>> import py_ieee754 as pi7
>>> import ctypes as ct

# Construction
>>> pi7.F32(1.5)
F32(0b0_01111111_10000000000000000000000)
>>> pi7.F64.from_components("0", "0"*11, "1"*52)# construct from sign, exp and sig bits
F64(0b0_00000000000_1111111111111111111111111111111111111111111111111111)
>>> pi7.F32.from_bits(0x3FC00000)               # from bit pattern
F32(0b0_01111111_10000000000000000000000)
>>> pi7.IEEE754.from_ctypes(ct.c_float(1.5))    # auto-dispatch (→ F32)
F32(0b0_01111111_10000000000000000000000)

# Field access & classification
>>> a = pi7.F32(1.5)
>>> a.sign, a.exponent, a.significand, a.bits
(0, 127, 4194304, 1069547520)
>>> a.is_nan, a.is_inf, a.is_zero, a.is_subnormal, a.is_normal
(False, False, False, False, True)

# Arithmetic with rounding
>>> pi7.add(pi7.F32(1.0), pi7.F32(2.0), round_mode=pi7.RoundingMode.DOWNWARD)
F32(0b0_10000000_10000000000000000000000)

# math.h functions with ctypes interface, round control and fenv exceptions
>>> pi7.math.sqrt(ct.c_double(2.0))
c_double(1.4142135623730951)
>>> pi7.math.fma(
            ct.c_double(1.5), 
            pi7.F64.from_bits(1).ctypes_value, 
            ct.c_double(0), 
            round_mode=pi7.RoundingMode.DOWNWARD)
c_double(5e-324) # = bit 0b1
```