from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import replace_in_file
import sys
import platform
import os

os_platform = sys.platform

class TDSEngine(ConanFile):
    name = "TDSEngine"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    options = {
        "shared": [True, False],
        "editor": [True, False],
        "use_rttr": [True, False],
        "use_vulkan": [True, False],
        "use_vulkan_bootstrap" : [True, False],
        "use_gaia_ecs" : [True, False],
        "use_entt_ecs": [True, False],
        "enable_rendering" : [True, False],
        "enable_exception": [True, False],
        "enable_testing": [True, False],
        "export_engine": [True, False],
        "console_logging": [True, False],
        "file_logging": [True, False],
        "enable_boost_exception": [True, False],
        "using_glm": [True, False],
        "with_stacktrace": [True, False],
        "use_boost_stacktrace": [True, False],
        "treat_warnings_as_errors": [True, False],
        "use_tracy": [True, False],
        "use_thread_sanitizer":[True, False],
        "use_assimp":[True,False],
        "use_simd_json":[True,False],
        "use_shader_compiler":[True,False],
        "use_shaderc" : [True,False],
        "use_spirv_reflect" : [True,False],
        "code_generated":[True, False],
        "vulkan_debug":[True, False],
        #Architecture option

    }

    default_options = {
        "shared": False,
        "editor": False,
        "use_rttr": True,
        "use_vulkan": False,
        "use_vulkan_bootstrap" : False,
        "use_gaia_ecs": False,
        "use_entt_ecs": False,
        "enable_rendering" : False,
        "enable_exception": True,
        "enable_testing": False,
        "export_engine": False,
        "console_logging": True,
        "file_logging": False,
        "enable_boost_exception": True,
        "using_glm": True,
        "with_stacktrace": True,
        "use_boost_stacktrace": True,
        "treat_warnings_as_errors": False,
        "use_tracy": True,
        "use_thread_sanitizer" : False,
        "use_assimp": False,
        "use_simd_json" : True,
        "use_shader_compiler": True,
        "use_shaderc": False,
        "use_spirv_reflect" : True,
        "code_generated" : False,
        "vulkan_debug": True,

    }

    def requirements(self):
        #if self.options.editor or self.options.use_rttr:
            #self.requires("rttr/0.9.6")
        if self.options.use_rttr:
            self.requires("rttr/0.9.7@eugene/prebuilt")

        if self.options.editor or self.options.use_assimp:
            self.requires("assimp/5.4.3")
            self.requires("fastgltf/0.9.0")
            self.requires("stb/cci.20230920")

        if self.options.use_tracy:
            self.requires("tracy/0.12.2")

        if not self.options.use_boost_stacktrace and self.options.with_stacktrace:
            self.requires("backward-cpp/1.6")

        if self.options.use_vulkan:
            #self.requires("vulkan-headers/1.4.313.0")
            self.requires("vulkan-memory-allocator/3.3.0")
            if self.options.use_spirv_reflect:
                self.requires("spirv-reflect/1.4.350.0")
            if self.options.use_shaderc:
                self.requires("shaderc/2025.3")

        if self.options.use_vulkan_bootstrap:
            self.requires("vk-bootstrap/1.3.296")
            
        if not (self.options.use_vulkan and self.options.use_vulkan_bootstrap) and self.options.enable_rendering:
            self.requires("opengl/system")
            self.requires("glad/2.0.8")

        if self.options.enable_testing:
            self.requires("catch2/3.7.1")
        
        self.requires("boost/1.88.0")
        self.requires("joltphysics/5.2.0")
        self.requires("nlohmann_json/3.12.0")
        self.requires("rapidjson/cci.20230929")
        self.requires("robin-hood-hashing/3.11.5")
        if self.options.use_gaia_ecs:
            self.requires("gaia-ecs/0.9.2")
        if self.options.use_simd_json:
            self.requires("simdjson/3.13.0")
        self.requires("ctre/3.10.0")
        self.requires("pcre2/10.44")
        self.requires("fmt/11.2.0")
        self.requires("spdlog/1.15.3")
        self.requires("glfw/3.4")

        if self.options.using_glm:
            self.requires("glm/1.0.1")
            
        self.requires("ms-gsl/4.2.0")
        self.requires("zlib/1.3.1")
        self.requires("parallel-hashmap/2.0.0")
        self.requires("concurrentqueue/1.0.4")
        self.requires("readerwriterqueue/1.0.6")

        if self.options.use_shader_compiler:
            self.requires("glslang/1.4.350.0")

    def configure(self):
        shared = self.options.shared

        # if self.options.editor or self.options.use_rttr:
        #     self.options["rttr"].shared = shared

        if (self.options.editor or self.options.use_assimp):
            self.options["assimp"].shared = shared
            self.options["fastgltf"].shared = shared
            self.options["stb"].shared = shared

        if self.options.use_tracy:
            self.options["tracy"].shared = shared

        if not self.options.use_boost_stacktrace and self.options.with_stacktrace:
            self.options["backward-cpp"].shared = shared
            self.options["boost"].without_stacktrace = True

        if self.options.enable_testing:
            self.options["catch2"].shared = shared

    

        for dep in [
            "boost", "joltphysics", "nlohmann_json", "rapidjson",
            "robin-hood-hashing", "simdjson", "ctre", "pcre2", "fmt",
            "spdlog", "glfw", "glm", "ms-gsl", "zlib",
            "parallel-hashmap", "concurrentqueue", "readerwriterqueue"
        ]:
            self.options[dep].shared = shared

    def generate(self):
        tc = CMakeToolchain(self)

        if os_platform == "win32":
            tc.variables["PLATFORM_WIN32"] = True
            if self.settings.compiler == "msvc":
                tc.variables["USING_MSVC"] = True
            else:
                raise Exception("Only MSVC is supported on Windows builds.")
        elif os_platform == "linux":
            tc.variables["PLATFORM_LINUX"] = True
            if self.options.use_thread_sanitizer:
                if self.settings.compiler == "clang":
                    tc.variables["USING_CLANG"] = True
                    tc.cache_variables["CMAKE_CXX_FLAGS_INIT"] = "-fsanitize=thread -g -O1"
                    tc.cache_variables["CMAKE_EXE_LINKER_FLAGS_INIT"] = "-fsanitize=thread"
                else:
                    raise Exception("Linux builds and Clang is unable to use ThreadSanitizer support.")

        else:
            raise Exception(f"Unsupported platform: {os_platform}")


        # Logging
        tc.variables["ENABLE_LOG_CONSOLE"] = self.options.console_logging
        tc.variables["ENABLE_LOG_FILE"] = self.options.file_logging
        tc.variables["ENABLE_TRACY"] = self.options.use_tracy
        # RTTI and editor
        tc.variables["USE_RTTR"] = self.options.use_rttr
        tc.variables["USE_EDITOR"] = self.options.editor
        tc.variables["USE_ASSIMP"] = self.options.use_assimp
        tc.variables["USE_VULKAN"] = self.options.use_vulkan
        tc.variables["USE_VULKAN_BOOTSTRAP"] = self.options.use_vulkan_bootstrap
        tc.variables["ENABLE_RENDERING"] = self.options.enable_rendering
        # Exceptions
        tc.variables["ENABLE_EXCEPTIONS"] = self.options.enable_exception
        tc.variables["BOOST_EXCEPTION"] = self.options.enable_boost_exception

        # Stack trace
        tc.variables["WITH_STACKTRACE"] = self.options.with_stacktrace
        tc.variables["USE_BOOST_STACKTRACE"] = self.options.use_boost_stacktrace
        # Math
        tc.variables["USING_GLM"] = self.options.using_glm
        
        # Misc
        tc.variables["EXPORT_ENGINE"] = self.options.export_engine
        tc.variables["ENABLE_TESTING"] = self.options.enable_testing
        tc.variables["TREAT_WARNINGS_AS_ERRORS"] = self.options.treat_warnings_as_errors
        tc.variables["USE_SIMD_JSON"] = self.options.use_simd_json
        tc.variables["USE_GAIA_ECS"] = self.options.use_gaia_ecs
        tc.variables["USE_ENTT_ECS"] = self.options.use_entt_ecs
        tc.variables["CODE_GENERATED"] = self.options.code_generated
        tc.variables["USE_SHADER_C"] = self.options.use_shaderc
        tc.variables["USE_SHADER_COMPILER"] = self.options.use_shader_compiler
        tc.variables["USE_SPIRV_REFLECT"] = self.options.use_spirv_reflect
        tc.variables["VULKAN_DEBUG"] = self.options.vulkan_debug
        
        arch = str(self.settings.arch) if self.settings.arch else platform.machine().lower()

        x86_arch = arch in ("x86_64", "amd64", "i686", "i386")
        arm_arch = arch.startswith("arm") or arch.startswith("aarch")

        if not (x86_arch or arm_arch):
            from conan.errors import ConanInvalidConfiguration
            raise ConanInvalidConfiguration(f"Unsupported architecture {arch}")

        tc.variables["X86_ARCH"] = "TRUE" if x86_arch else "FALSE"
        tc.variables["ARM_ARCH"] = "TRUE" if arm_arch else "FALSE"
        tc.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self.options.enable_testing:
            cmake.test()

