include(CTest)
include(Catch)

file(GLOB TEST_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

add_executable(engine_tests ${TEST_SOURCES})

find_package(Catch2 CONFIG REQUIRED)

# find_package(gaia REQUIRED)
# target_link_libraries(engine_tests PRIVATE gaia::gaia)

target_link_libraries(engine_tests
    PRIVATE
        engine_lib
        Catch2::Catch2WithMain
)

catch_discover_tests(engine_tests
    TEST_PREFIX "Engine."
    REPORTER console
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)