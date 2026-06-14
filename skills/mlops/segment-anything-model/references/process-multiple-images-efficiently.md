# Process multiple images efficiently
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]

all_masks = []
for image in images:
    predictor.set_image(image)
    masks, _, _ = predictor.predict(
        point_coords=np.array([[500, 375]]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks)
```

### Multiple prompts per image

```python