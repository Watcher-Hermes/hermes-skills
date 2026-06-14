## Layer 3: Deterministic Cuts (FFmpeg)

FFmpeg handles the boring but critical work: splitting, trimming, concatenating, and preprocessing.

### Extract segment by timestamp

```bash
ffmpeg -i raw.mp4 -ss 00:12:30 -to 00:15:45 -c copy segment_01.mp4
```

### Batch cut from edit decision list

```bash
#!/bin/bash