# Load melody model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)