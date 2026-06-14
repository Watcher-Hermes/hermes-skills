## MusicGen usage

### Text-to-music generation

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-medium')