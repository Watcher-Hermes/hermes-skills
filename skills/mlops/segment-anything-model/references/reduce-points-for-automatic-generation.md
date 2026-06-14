# Reduce points for automatic generation
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=16,  # Default is 32
)