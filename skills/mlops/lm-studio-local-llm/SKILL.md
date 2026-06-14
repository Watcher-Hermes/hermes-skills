---

name: lm-studio-local-llm
description: "LM Studio local LLM operations — Windows install, GGUF model import/load, GPU offload configuration, server management, API testing, and model swapping. Sibling to ollama-local-llm."
title: "Lm Studio Local LLM"
version: 1.2.0
platforms: [windows]
tags: [lm-studio, local-llm, gpu-offload, gguf, windows, lms-cli]
category: mlops
audience: user
---

# Lm Studio Local Llm

Bu skill modüler bir yönlendiricidir. İhtiyacınız olan bölümü seçin ve ilgili reference dosyasını yükleyin.

## 📂 Bölümler

| Bölüm | Reference Dosyası |
|-------|------------------|
| LM Studio Local LLM | `references/lm-studio-local-llm.md` |
| When to use | `references/when-to-use.md` |
| Windows Installation | `references/windows-installation.md` |
| Silent install (NSIS-based): | `references/silent-install-nsis-based.md` |
| Model Management (`lms` CLI) | `references/model-management-lms-cli.md` |
| Copy mode (keeps original in downloads) | `references/copy-mode-keeps-original-in-downloads.md` |
| Move mode (default) | `references/move-mode-default.md` |
| LM Studio Internal Config Files | `references/lm-studio-internal-config-files.md` |
| Should show: "llama.cpp-win-x86_64-nvidia-cuda-avx2" | `references/should-show-llama-cpp-win-x86_64-nvidia-cuda-avx2.md` |
| GPU Offload Configuration (CRITICAL) | `references/gpu-offload-configuration-critical.md` |
| Estimate resource requirements first (safest) | `references/estimate-resource-requirements-first-safest.md` |
| Auto-detect (default — no --gpu flag) | `references/auto-detect-default-no-gpu-flag.md` |
| Partial GPU offload (recommended for 14B+ models on 4GB VRAM) | `references/partial-gpu-offload-recommended-for-14b-models-on-4gb-vram.md` |
| Full GPU offload (small models only) | `references/full-gpu-offload-small-models-only.md` |
| API Server | `references/api-server.md` |
| → "Server is now running on port 1234" | `references/server-is-now-running-on-port-1234.md` |
| Model Swapping | `references/model-swapping.md` |
| Hermes Provider Configuration | `references/hermes-provider-configuration.md` |
| Define the provider | `references/define-the-provider.md` |
| Set as active provider (model name = lms --identifier value) | `references/set-as-active-provider-model-name-lms-identifier-value.md` |
| GUI-Based Model Switching (Mouse/Keyboard) | `references/gui-based-model-switching-mouse-keyboard.md` |
| → "[ControlType.Pane] \"Chrome Legacy Window\" ..." | `references/controltype-pane-chrome-legacy-window.md` |
| Tüm metinleri listele (LM Studio bölgesinde) | `references/t-m-metinleri-listele-lm-studio-b-lgesinde.md` |
| Belirli metni bul | `references/belirli-metni-bul.md` |
| Metne tıkla | `references/metne-t-kla.md` |
| 1. "Select a model" butonuna tıkla | `references/1-select-a-model-butonuna-t-kla.md` |
| 2. Arama kutusuna dolphin yaz | `references/2-arama-kutusuna-dolphin-yaz.md` |
| 3. Dolphin modeline tıkla (arama sonucu) | `references/3-dolphin-modeline-t-kla-arama-sonucu.md` |
| 4. "Load Model" butonuna tıkla (varsa) | `references/4-load-model-butonuna-t-kla-varsa.md` |
| See running models | `references/see-running-models.md` |
| Load new model via CLI (may need server restart) | `references/load-new-model-via-cli-may-need-server-restart.md` |
| Restart server | `references/restart-server.md` |
| Troubleshooting | `references/troubleshooting.md` |
| Pitfalls | `references/pitfalls.md` |

## Kullanım

1. İhtiyacın olan bölümü belirle
2. `skill_view(name="...", file_path="references/...")` ile yükle
