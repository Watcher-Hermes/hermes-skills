# Generate with text + style
descriptions = ["upbeat dance track"]
wav = model.generate_with_style(descriptions, style_audio, sr)
```

### Style-only generation (no text)

```python