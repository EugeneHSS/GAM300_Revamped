
# Optional executable (sandbox/demo) 
if(NOT EXPORT_ENGINE) 
  add_executable(engine_lib) 
  set_target_properties(engine_lib PROPERTIES OUTPUT_NAME "EngineApp") 
else() 
  add_library(engine_lib) 
  add_library(engine ALIAS engine_lib) 
  set_target_properties(engine_lib PROPERTIES OUTPUT_NAME "Engine") 
endif() 

target_include_directories(engine_lib PUBLIC ${PROJECT_SOURCE_DIR}/include) 
target_include_directories(engine_lib PUBLIC ${PROJECT_SOURCE_DIR}/src) 
set(CONFIG_GEN_DIR ${PROJECT_BINARY_DIR}/config_generated) 
configure_file("${PROJECT_SOURCE_DIR}/src/config.h.in" "${CONFIG_GEN_DIR}/config.h") 
target_include_directories(engine_lib PUBLIC ${CONFIG_GEN_DIR}) 

#add_subdirectory(app)
#add_subdirectory(core) 
#add_subdirectory(utilities)
#add_subdirectory(window) 
#add_subdirectory(rendering)
target_sources(engine_lib PRIVATE
    main.cpp
)
# Reflection generated files 
if(CODE_GENERATED) 
    file(GLOB_RECURSE GENERATED_SOURCES CONFIGURE_DEPENDS "${PROJECT_BINARY_DIR}/generated/*.generated.cpp" ) 
    target_sources(engine_lib PRIVATE ${GENERATED_SOURCES} ) 
    target_include_directories(engine_lib PUBLIC ${PROJECT_BINARY_DIR}/generated ) 
endif()

target_include_directories(engine_lib PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_include_directories(engine_lib PUBLIC ${PROJECT_SOURCE_DIR}/src)
set(CONFIG_GEN_DIR ${PROJECT_BINARY_DIR}/config_generated)
configure_file("${PROJECT_SOURCE_DIR}/src/config.h.in"
               "${CONFIG_GEN_DIR}/config.h")
target_include_directories(engine_lib PUBLIC ${CONFIG_GEN_DIR})

# --- Dependencies ---
if(USE_RTTR)
  find_package(rttr REQUIRED)
  target_link_libraries(engine_lib PRIVATE RTTR::Core)   # also adds the RTTR_DLL define

  # RTTR is a DLL: copy it next to the exe after each build (rttr_core_d.dll in Debug, rttr_core.dll in Release)
  if(NOT EXPORT_ENGINE)
    add_custom_command(TARGET engine_lib POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy_if_different
              $<TARGET_RUNTIME_DLLS:engine_lib> $<TARGET_FILE_DIR:engine_lib>
      COMMAND_EXPAND_LISTS)
  endif()
endif()

if(ENABLE_RENDERING AND USE_VULKAN)
  find_package(Vulkan REQUIRED)
  target_link_libraries(engine_lib PRIVATE Vulkan::Vulkan)

  find_package(VulkanMemoryAllocator REQUIRED)
  target_link_libraries(engine_lib PRIVATE GPUOpen::VulkanMemoryAllocator)

  if (USE_SHADER_C)
    find_package(shaderc REQUIRED)
    target_link_libraries(engine_lib PRIVATE shaderc::shaderc)
  endif()

  if (USE_SPIRV_REFLECT)
    find_package(spirv-reflect-static REQUIRED)
    target_link_libraries(engine_lib PRIVATE spirv-reflect-static)
  endif()

  if (USE_ENTT_ECS)
    find_package(EnTT REQUIRED)
    target_link_libraries(engine_lib PRIVATE EnTT::EnTT)
  endif()

  if (USE_GAIA_ECS)
    find_package(gaia REQUIRED)
    target_link_libraries(engine_lib PRIVATE gaia::gaia)
  endif()

  if (USE_VULKAN_BOOTSTRAP)
    find_package(vk-bootstrap CONFIG REQUIRED)
    target_link_libraries(engine_lib
            PRIVATE vk-bootstrap::vk-bootstrap
        )

    target_compile_definitions(engine_lib
            PRIVATE TDS_USE_VULKAN_BOOTSTRAP
        )
  endif()

endif()

if (ENABLE_RENDERING AND NOT USE_VULKAN)
  find_package(OpenGL REQUIRED)
  find_package(glad REQUIRED)
  target_link_libraries(engine_lib
      PRIVATE
          OpenGL::GL
          glad::glad)
endif()

if (USE_SHADER_COMPILER)
  find_package(glslang REQUIRED)
  target_link_libraries(engine_lib PRIVATE glslang::_glslang-do-not-use)
endif()


if (USE_EDITOR OR USE_ASSIMP)
  find_package(fastgltf CONFIG REQUIRED)
  target_link_libraries(engine_lib
      PRIVATE
          fastgltf::fastgltf
  )
  find_package(Stb REQUIRED)
  target_link_libraries(engine_lib
      PRIVATE
          stb::stb
  )
endif()

if(ENABLE_TRACY)
  find_package(Tracy REQUIRED)
  target_link_libraries(engine_lib PRIVATE Tracy::TracyClient)
endif()

if(USE_ASSIMP)
  find_package(assimp REQUIRED)
  target_link_libraries(engine_lib PRIVATE assimp::assimp)
endif()

if(WITH_STACKTRACE AND NOT USE_BOOST_STACKTRACE)
  find_package(Backward REQUIRED)
  target_link_libraries(engine_lib PRIVATE Backward::Backward)
endif()

if(USE_SIMD_JSON)
  find_package(simdjson REQUIRED)
  target_link_libraries(engine_lib PRIVATE simdjson::simdjson)
endif()

# Core libraries (Conan/system)
find_package(Boost REQUIRED)
target_link_libraries(engine_lib PRIVATE Boost::boost)

find_package(Jolt REQUIRED)
target_link_libraries(engine_lib PRIVATE Jolt::Jolt)

find_package(nlohmann_json REQUIRED)
target_link_libraries(engine_lib PRIVATE nlohmann_json::nlohmann_json)

find_package(RapidJSON REQUIRED)
target_link_libraries(engine_lib PRIVATE rapidjson)

find_package(robin_hood REQUIRED)
target_link_libraries(engine_lib PRIVATE robin_hood::robin_hood)

find_package(PCRE2 REQUIRED)
target_link_libraries(engine_lib PRIVATE pcre2::pcre2)

find_package(fmt REQUIRED)
target_link_libraries(engine_lib PRIVATE fmt::fmt)

find_package(spdlog REQUIRED)
target_link_libraries(engine_lib PRIVATE spdlog::spdlog)

find_package(glfw3 CONFIG REQUIRED)
target_link_libraries(engine_lib PRIVATE glfw)

find_package(glm REQUIRED)
target_link_libraries(engine_lib PRIVATE glm::glm)

find_package(Microsoft.GSL REQUIRED)
target_link_libraries(engine_lib PRIVATE Microsoft.GSL::GSL)

find_package(ZLIB REQUIRED)
target_link_libraries(engine_lib PRIVATE ZLIB::ZLIB)

find_package(phmap REQUIRED)
target_link_libraries(engine_lib PRIVATE phmap)

find_package(concurrentqueue REQUIRED)
target_link_libraries(engine_lib PRIVATE concurrentqueue::concurrentqueue)

find_package(readerwriterqueue REQUIRED)
target_link_libraries(engine_lib PRIVATE readerwriterqueue::readerwriterqueue)
