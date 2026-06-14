# Create evaluator
evaluator = Evaluate(
    devset=testset,
    metric=exact_match,
    num_threads=4,
    display_progress=True
)