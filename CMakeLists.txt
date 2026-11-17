cmake_minimum_required(VERSION 3.25)
#include(${CMAKE_BINARY_DIR}/generators/conan_toolchain.cmake)

project(EnginePlugin)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

option(CODE_GENERATION "Enable Code Generation" OFF)
option(EXPOSE_DLL "Expose all window dll" ON)
option(EXPORT_ENGINE "Build engine as a shared library (used by editor)" OFF)

if (EXPOSE_DLL)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()


add_subdirectory(src)

if(ENABLE_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()
