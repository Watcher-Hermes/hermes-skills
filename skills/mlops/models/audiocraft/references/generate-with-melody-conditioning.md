# Generate with melody conditioning
descriptions = ["acoustic guitar folk song"]
wav = model.generate_with_chroma(descriptions, melody, sr)

torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32000)
```

### Stereo generation

```python
from audiocraft.models import MusicGen