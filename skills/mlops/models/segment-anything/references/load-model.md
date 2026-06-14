# Load model
predictor = SamPredictor(sam)
predictor.set_image(image)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: