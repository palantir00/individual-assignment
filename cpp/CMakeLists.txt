cmake_minimum_required(VERSION 3.16)
project(matmul_bench CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(matmul STATIC src/matmul.cpp)
target_include_directories(matmul PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(matmul_bench src/bench.cpp)
target_link_libraries(matmul_bench PRIVATE matmul)
