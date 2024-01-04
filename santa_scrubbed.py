# pip install pillow
# pip install google-cloud-vision
# pip install openai

from google.cloud import vision
import io
import openai
import re
from PIL import Image, ImageDraw, ImageFont

# Set up the client
client = vision.ImageAnnotatorClient()

# Load the image
with io.open('<your letter in jpg format>', 'rb') as image_file:  # replace with your file
    content = image_file.read()

image = vision.Image(content=content)

# Perform text detection
response = client.text_detection(image=image)
texts = response.text_annotations

# Display detected texts
for text in texts:
    print('\n"{}"'.format(text.description))

if response.error.message:
    raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))

extracted_text = texts[0].description if texts else "No text found."

openai.api_key = '<your key>'  # Replace with your OpenAI API key

response_from_santa = openai.Completion.create(
  engine="text-davinci-003",
  prompt=f"Write a festive response from Santa to the following message and as a footnote, state the interpretation of the letter and guess the age range of the personp: '{extracted_text}'",
  max_tokens=150
)

print(response_from_santa.choices[0].text)

def text_to_cursive_image(text, font_path, output_path):
    # Load the font
    font_size = 20  # Adjust the size as needed
    font = ImageFont.truetype(font_path, font_size)

    # Create a large temporary image
    temp_image = Image.new('RGB', (1000, 1000), color=(255, 255, 255))
    draw = ImageDraw.Draw(temp_image)

    # Draw the text on the temporary image
    draw.text((0, 0), text, fill="black", font=font)

    # Calculate text bounds
    text_bounds = draw.textbbox((0, 0), text, font=font)

    # Create the actual image with the text bounds
    image = Image.new('RGB', (text_bounds[2], text_bounds[3]), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, fill="black", font=font)

    # Save the image
    image.save(output_path)


# Example usage
text = response_from_santa.choices[0].text # Replace with the text you want
font_path = "<your path>"  # Replace with the path to your font
output_path = "<your path>"  # Replace with your desired output path

text_to_cursive_image(text, font_path, output_path)
