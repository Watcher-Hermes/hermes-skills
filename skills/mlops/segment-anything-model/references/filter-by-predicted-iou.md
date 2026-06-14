# Filter by predicted IoU
high_quality = [m for m in masks if m['predicted_iou'] > 0.9]