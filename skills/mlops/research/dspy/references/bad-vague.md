# ❌ Bad: Vague
class Task(dspy.Signature):
    input = dspy.InputField()
    output = dspy.OutputField()