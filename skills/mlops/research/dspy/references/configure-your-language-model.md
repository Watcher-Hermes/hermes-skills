# Configure your language model
lm = dspy.Claude(model="claude-sonnet-4-5-20250929")
dspy.settings.configure(lm=lm)