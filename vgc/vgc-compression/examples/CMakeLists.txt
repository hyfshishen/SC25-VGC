# # Find CUDA package
# find_package(CUDAToolkit REQUIRED)

# Define the install directory for binaries
set(install_dir ${PROJECT_BINARY_DIR}/examples/bin)
set(cuSZp "cuSZp")
set(cuSZp_test_f32 "cuSZp_test_f32")
set(cuSZp_test_f64 "cuSZp_test_f64")

# Include the main include directory
include_directories(${PROJECT_SOURCE_DIR}/include 
                    ${CUDAToolkit_INCLUDE_DIRS})

# Compile executable binaries
add_executable(${cuSZp} cuSZp.cpp)
add_executable(${cuSZp_test_f32} cuSZp_test_f32.cpp)
add_executable(${cuSZp_test_f64} cuSZp_test_f64.cpp)

# Link the existing cuSZp_static library
target_link_libraries(${cuSZp} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_test_f32} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_test_f64} PRIVATE cuSZp_static)

# Set output paths for the compiled binary
set_target_properties(${cuSZp} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_test_f32} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_test_f64} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})

# Set installation paths for the compiled binary
install(TARGETS ${cuSZp} DESTINATION bin)
install(TARGETS ${cuSZp_test_f32} DESTINATION bin)
install(TARGETS ${cuSZp_test_f64} DESTINATION bin)


# Test binary for cuSZp3 implementation phase
set(cuSZp_2D_float_plain "cuSZp_2D_float_plain")
set(cuSZp_3D_float_plain "cuSZp_3D_float_plain")
set(cuSZp_2D_double_plain "cuSZp_2D_double_plain")
set(cuSZp_3D_double_plain "cuSZp_3D_double_plain")
set(cuSZp_2D_float_outlier "cuSZp_2D_float_outlier")
set(cuSZp_3D_float_outlier "cuSZp_3D_float_outlier")
set(cuSZp_2D_double_outlier "cuSZp_2D_double_outlier")
set(cuSZp_3D_double_outlier "cuSZp_3D_double_outlier")
add_executable(${cuSZp_2D_float_plain} cuSZp_2D_float_plain.cpp)
add_executable(${cuSZp_3D_float_plain} cuSZp_3D_float_plain.cpp)
add_executable(${cuSZp_2D_double_plain} cuSZp_2D_double_plain.cpp)
add_executable(${cuSZp_3D_double_plain} cuSZp_3D_double_plain.cpp)
add_executable(${cuSZp_2D_float_outlier} cuSZp_2D_float_outlier.cpp)
add_executable(${cuSZp_3D_float_outlier} cuSZp_3D_float_outlier.cpp)
add_executable(${cuSZp_2D_double_outlier} cuSZp_2D_double_outlier.cpp)
add_executable(${cuSZp_3D_double_outlier} cuSZp_3D_double_outlier.cpp)
target_link_libraries(${cuSZp_2D_float_plain} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_3D_float_plain} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_2D_double_plain} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_3D_double_plain} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_2D_float_outlier} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_3D_float_outlier} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_2D_double_outlier} PRIVATE cuSZp_static)
target_link_libraries(${cuSZp_3D_double_outlier} PRIVATE cuSZp_static)
set_target_properties(${cuSZp_2D_float_plain} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_3D_float_plain} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_2D_double_plain} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_3D_double_plain} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_2D_float_outlier} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_3D_float_outlier} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_2D_double_outlier} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
set_target_properties(${cuSZp_3D_double_outlier} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${install_dir})
install(TARGETS ${cuSZp_2D_float_plain} DESTINATION bin)
install(TARGETS ${cuSZp_3D_float_plain} DESTINATION bin)
install(TARGETS ${cuSZp_2D_double_plain} DESTINATION bin)
install(TARGETS ${cuSZp_3D_double_plain} DESTINATION bin)
install(TARGETS ${cuSZp_2D_float_outlier} DESTINATION bin)
install(TARGETS ${cuSZp_3D_float_outlier} DESTINATION bin)
install(TARGETS ${cuSZp_2D_double_outlier} DESTINATION bin)
install(TARGETS ${cuSZp_3D_double_outlier} DESTINATION bin)