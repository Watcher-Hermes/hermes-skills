# Move mode (default)
lms import -y "/path/to/model.gguf"
```

**Note:** Import attempts HuggingFace lookup which may timeout. If it times out, manually copy the file to `~/.lmstudio/models/<name>/` and LM Studio will find it on next `lms ls`.

### Manual copy (fallback)

```bash
mkdir -p "/c/Users/marko/.lmstudio/models/ModelName/"
cp "/c/Users/marko/Downloads/model.gguf" "/c/Users/marko/.lmstudio/models/ModelName/"
```

### View loaded models (JSON)

```bash
lms ps --json
```

Returns: model key, display name, size, architecture, quantization, identifier, context length, status.

---