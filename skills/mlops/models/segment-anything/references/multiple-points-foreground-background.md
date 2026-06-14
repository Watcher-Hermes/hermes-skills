# Multiple points (foreground + background)
input_points = np.array([[500, 375], [600, 400], [450, 300]])
input_labels = np.array([1, 1, 0])  # 2 foreground, 1 background

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False  # Single mask when prompts are clear
)
```

### Box prompts

```python