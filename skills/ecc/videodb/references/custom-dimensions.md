# Custom dimensions
reframed = video.reframe(start=0, end=60, target={"width": 1280, "height": 720})
```

### Generative media

```python
image = coll.generate_image(
    prompt="a sunset over mountains",
    aspect_ratio="16:9",
)
```