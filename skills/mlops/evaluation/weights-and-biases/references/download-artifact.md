# Download artifact
artifact = run.use_artifact('training-dataset:latest')
artifact_dir = artifact.download()