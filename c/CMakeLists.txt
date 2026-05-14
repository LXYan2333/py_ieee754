add_library(py_ieee754_wrappers SHARED 
    wrappers.c
    _math_power.c
    _math_basic.c
    _math_exponential.c
    _math_trigonometric.c
    _math_hyperbolic.c
    _math_error_gamma.c
    _math_nearest_int.c
    _math_manipulation.c
    _float_hex_format.c
)

set_target_properties(py_ieee754_wrappers PROPERTIES PREFIX "lib")

if(NOT WIN32)
    target_link_libraries(py_ieee754_wrappers PRIVATE m)
endif()

if(MSVC)
    target_compile_options(py_ieee754_wrappers PRIVATE /fp:strict)
else()
    target_compile_options(py_ieee754_wrappers PRIVATE -frounding-math -fsignaling-nans)
endif()

install(TARGETS py_ieee754_wrappers
    LIBRARY DESTINATION py_ieee754
    RUNTIME DESTINATION py_ieee754
)
