from PIL import Image, ImageDraw

# Create a white image
img = Image.new('RGB', (300, 100), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# Draw text
text = "Hello OCR 123!"
d.text((10, 30), text, fill=(0, 0, 0))

# Save image
img.save('test_ocr_image.png')
print("Test image saved as test_ocr_image.png") 