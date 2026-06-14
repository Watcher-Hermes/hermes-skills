# Generate matching style without text prompt
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=None  # Disable double CFG for style-only
)

wav = model.generate_with_style([None], style_audio, sr)
```