target_sources(engine_lib PRIVATE
    render_context.cpp
    vulkan_backend.cpp
    assets/texture_infos.cpp
    render_converters/render_converters.cpp
    VkImpl/vma_impl.cpp
    VkImpl/vulkan_device.cpp
    VkImpl/vulkan_dyn_functions.cpp
    VkImpl/vulkan_instance.cpp
    VkImpl/commands/command_queue.cpp
    VkImpl/commands/vulkan_command_buffer.cpp
    VkImpl/gpu/vulkan_image.cpp
    VkImpl/synchronizations/vulkan_fence.cpp
    VkImpl/synchronizations/vulkan_semaphore.cpp
)