find_package(pybind11 REQUIRED)


pybind11_add_module(tt_adapter tt_adapter.cc)


file(GLOB_RECURSE RELEVANT_LIBS ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/.local/toolchain/lib/*.a)
file(GLOB_RECURSE RELEVANT_DYLIBS ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/.local/toolchain/lib/*.dylib)
include_directories(${CMAKE_SOURCE_DIR}/third_party/tt-mlir/.local/toolchain/include)
target_link_libraries(tt_adapter PRIVATE ${RELEVANT_LIBS} ${RELEVANT_DYLIBS})

add_library(MLIRTTKernel STATIC IMPORTED)
set_property(TARGET MLIRTTKernel PROPERTY IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/lib/libMLIRTTKernelDialect.a)
target_include_directories(MLIRTTKernel INTERFACE ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/include/ttmlir/Dialect/TTKernel)


add_library(MLIRTTIR STATIC IMPORTED)
set_property(TARGET MLIRTTIR PROPERTY IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/lib/libMLIRTTIRDialect.a)
target_include_directories(MLIRTTIR INTERFACE ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/include/ttmlir/Dialect/TTIR)

add_library(MLIRTT STATIC IMPORTED)
set_property(TARGET MLIRTT PROPERTY IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/lib/libMLIRTTDialect.a)
target_include_directories(MLIRTT INTERFACE ${CMAKE_SOURCE_DIR}/third_party/tt-mlir/build/include/ttmlir/Dialect/TT)

target_link_libraries(tt_adapter PRIVATE MLIRTTKernel MLIRTTIR MLIRTT)