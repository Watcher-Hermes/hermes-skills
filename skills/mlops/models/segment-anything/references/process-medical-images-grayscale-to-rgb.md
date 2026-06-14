# Process medical images (grayscale to RGB)
medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)
rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)

predictor.set_image(rgb_image)