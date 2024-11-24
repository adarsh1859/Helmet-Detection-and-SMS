# import os
# import easyocr
# from PIL import Image

# def extract_text_from_images(number_plates, textNum):
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])

#     # Create output folder if it doesn't exist
#     if not os.path.exists(textNum):
#         os.makedirs(textNum)

#     # Loop through each image file in the input folder
#     for filename in os.listdir(number_plates):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             image_path = os.path.join(number_plates, filename)

#             # Read image using PIL
#             image = Image.open(image_path)

#             # Extract text using EasyOCR
#             result = reader.readtext(image)

#             # Write extracted text to a text file in the output folder
#             output_text_filename = os.path.splitext(filename)[0] + ".txt"
#             output_text_path = os.path.join(textNum, output_text_filename)

#             with open(output_text_path, "w") as text_file:
#                 for detection in result:
#                     text_file.write(detection[1] + "\n")

#             print(f"Text extracted from {filename} and saved to {output_text_filename}")

# # Example usage:
# number_plates = "input_images"
# textNum = "output_texts"
# extract_text_from_images(number_plates, textNum)


import os
import easyocr
from PIL import Image

def extract_text_from_images(input_folder, output_folder):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each image file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)

            # Read image using PIL
            image = Image.open(image_path)

            # Extract text using EasyOCR
            result = reader.readtext(image)

            # Write extracted text to a text file in the output folder
            output_text_filename = os.path.splitext(filename)[0] + ".txt"
            output_text_path = os.path.join(output_folder, output_text_filename)

            with open(output_text_path, "w") as text_file:
                for detection in result:
                    text_file.write(detection[1] + "\n")

            print(f"Text extracted from {filename} and saved to {output_text_filename}")

# Example usage:
input_folder = "number_plates"
output_folder = "output_texts"
extract_text_from_images(input_folder, output_folder)
