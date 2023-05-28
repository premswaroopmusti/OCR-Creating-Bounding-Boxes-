import json
from PIL import Image, ImageDraw, ImageFont

# Load the image
image = Image.open('sanskrit_text.jpg')

# Define font and font size
font = ImageFont.truetype('arial.ttf', 16)

# Create a draw object
draw = ImageDraw.Draw(image)

# Read the text file
with open('sanskrit_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Split the text into lines
lines = text.splitlines()

# Define the starting y-coordinate for the first line
y = 50

# Define a dictionary to store the bounding box coordinates for each line
bounding_boxes = {}

# Iterate over each line
for i, line in enumerate(lines):
    # Calculate the width and height of the line
    width, height = draw.textsize(line, font=font)
    
    # Create a bounding box around the line
    bbox = (50, y, 50 + width, y + height)
    
    # Crop the image to the bounding box
    line_image = image.crop(bbox)
    
    # Save the line as a separate JPEG file
    line_image.save(f'{line}.jpg')
    
    # Save the coordinates of the bounding box in the dictionary
    bounding_boxes[f'box{i+1}'] = {
        'top_left': [bbox[0], bbox[1]],
        'top_right': [bbox[2], bbox[1]],
        'bottom_left': [bbox[0], bbox[3]],
        'bottom_right': [bbox[2], bbox[3]]
    }
    
    # Increment the y-coordinate for the next line
    y += height + 20

# Save the dictionary of bounding box coordinates as a JSON file
with open('bounding_boxes.json', 'w') as file:
    json.dump(bounding_boxes, file, indent=4)