# Generate continuation
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=512)
```