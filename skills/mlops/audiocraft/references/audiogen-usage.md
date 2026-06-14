## AudioGen usage

### Sound effect generation

```python
from audiocraft.models import AudioGen
import torchaudio

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=10)