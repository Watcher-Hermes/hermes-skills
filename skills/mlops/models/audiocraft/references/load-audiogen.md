# Load AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')

model.set_generation_params(duration=5)