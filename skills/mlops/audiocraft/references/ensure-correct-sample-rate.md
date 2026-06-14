# Ensure correct sample rate
if sr != 32000:
    resampler = torchaudio.transforms.Resample(sr, 32000)
    wav = resampler(wav)