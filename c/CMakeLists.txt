add_library(wrappers SHARED wrappers.c _math_power.c _math_basic.c _math_exponential.c _math_trigonometric.c _math_hyperbolic.c _math_error_gamma.c _math_nearest_int.c _math_manipulation.c)

set_target_properties(wrappers PROPERTIES
    OUTPUT_NAME _py_ieee754_wrappers
    PREFIX ""
)

if(NOT WIN32)
    target_link_libraries(wrappers PRIVATE m)
endif()

if(MSVC)
    target_compile_options(wrappers PRIVATE /fp:strict)
else()
    target_compile_options(wrappers PRIVATE -frounding-math -fsignaling-nans)
endif()

install(TARGETS wrappers
    LIBRARY DESTINATION py_ieee754
    RUNTIME DESTINATION py_ieee754
)
