# Define metric
def validate_answer(example, pred, trace=None):
    return example.answer == pred.answer