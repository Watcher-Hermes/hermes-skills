# Log confusion matrix
wandb.log({"conf_mat": wandb.plot.confusion_matrix(
    probs=None,
    y_true=ground_truth,
    preds=predictions,
    class_names=class_names
)})
```

### Reports

Create shareable reports in W&B UI:
- Combine runs, charts, and text
- Markdown support
- Embeddable visualizations
- Team collaboration