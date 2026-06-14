# Optimize
optimizer = BootstrapFewShot(metric=validate_answer, max_bootstrapped_demos=3)
optimized_qa = optimizer.compile(qa, trainset=trainset)