# Process multiple prompts at once (more efficient)
descriptions = ["prompt1", "prompt2", "prompt3", "prompt4"]
wav = model.generate(descriptions)  # Single batch