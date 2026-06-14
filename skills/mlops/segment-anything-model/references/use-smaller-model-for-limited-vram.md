# Use smaller model for limited VRAM
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")