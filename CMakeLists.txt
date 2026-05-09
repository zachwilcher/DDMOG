cmake_minimum_required(VERSION 3.10)
project (ddmog)

find_package(Eigen3 REQUIRED NO_MODULE)

set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.conda-env")
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS_DEBUG "-g")

# Make Conda libraries available at runtime.
set(CMAKE_INSTALL_RPATH "${CMAKE_CURRENT_SOURCE_DIR}/.conda-env/lib")
# Make sure this path is a part of the created executable
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

add_executable(ddmog_counter ddmog_counter/main.cpp)
set_property(TARGET ddmog_counter PROPERTY CXX_STANDARD 23)

target_link_libraries(ddmog_counter Eigen3::Eigen)
