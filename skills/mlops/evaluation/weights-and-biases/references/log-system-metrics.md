# Log system metrics
wandb.log({
    "gpu/util": gpu_utilization,
    "gpu/memory": gpu_memory_used,
    "cpu/util": cpu_utilization
})