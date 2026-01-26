from PIL import Image, ImageDraw, ImageFont

# Sample Python code
code = """
print("🧮 Simple Calculator 🧮")

num1 = float(input("Enter first number: "))
op = input("Choose operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))

if op == '+':
    result = num1 + num2
elif op == '-':
    result = num1 - num2
elif op == '*':
    result = num1 * num2
elif op == '/':
    result = num1 / num2
else:
    result = "Invalid operator!"

print("✅ Result:", result)


"""

# Image settings
font_size = 24
font = ImageFont.load_default()
width = 600
height = 150
bg_color = (255, 255, 255)
text_color = (0, 0, 0)

# Create image
img = Image.new("RGB", (width, height), color=bg_color)
draw = ImageDraw.Draw(img)
draw.text((10, 10), code, fill=text_color, font=font)

# Save image
img.save("test_code.png")
print("Image saved as test_code.png")