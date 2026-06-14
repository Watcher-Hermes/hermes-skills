# Full GPU offload (small models only)
lms load <model-key> --gpu max -y
```

### Key identifier parameter

Always set `--identifier <name>` on load — this becomes the API model name:
```bash
lms load qwen3-32b-obliterated-i1 --gpu 0.5 -y --identifier qwen3-32b
```
API then uses: `"model": "qwen3-32b"` in requests.

### Context length

Default context upon load is 8192. Max depends on model architecture:
```bash
lms load <model> --context-length 16384 -y
```
Maximum for Qwen3-32B: 40960 tokens.

---