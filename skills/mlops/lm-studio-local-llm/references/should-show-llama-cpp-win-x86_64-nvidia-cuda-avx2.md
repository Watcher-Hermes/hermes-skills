# Should show: "llama.cpp-win-x86_64-nvidia-cuda-avx2"
```

### Setting Default GPU Offload (GUI)

There is NO API endpoint to change per-model GPU offload settings. To set all models to use maximum GPU:

1. Open LM Studio GUI
2. Click the gear icon (Settings) — either in sidebar bottom-left or top-right
3. Navigate to **Model** or **Loading** tab
4. Set **GPU Offload / GPU Layers** slider to **Maximum** (or -1 for all layers)
5. Apply/Save
6. Each subsequent model load will use these GPU layers by default

`lms load` CLI commands with `--gpu max` also achieve this per-session, but the GUI setting makes it permanent.