
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import numpy as np

# Function to perform OCR and get text data
def get_text_data(image):
    text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    return text_data

# Function to replace text in the image
def replace_text_in_image(img, text_data, index, new_word):
    img_copy = img.copy()
    draw = ImageDraw.Draw(img_copy)

    if 0 <= index < len(text_data['text']):
        x, y, w, h = text_data['left'][index], text_data['top'][index], text_data['width'][index], text_data['height'][index]

        draw.rectangle([x, y, x+w, y+h], fill="white")

        try:
            font = ImageFont.truetype("arial.ttf", h)
        except IOError:
            font = ImageFont.load_default()
            try:
                 font = ImageFont.load_default().font_variant(size=h)
            except Exception as e:
                 st.warning(f"Could not set font size for default font: {e}. Using default size.")

        text_x = x
        text_y = y
        if font == ImageFont.load_default():
             text_y += 2

        draw.text((text_x, text_y), new_word, fill="black", font=font)
        return img_copy
    else:
        st.error("Invalid index provided for text replacement.")
        return img_copy

st.title("Image Text Editor")

uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    text_data = get_text_data(image)

    st.subheader("Detected Text:")
    valid_texts = [(i, word) for i, word in enumerate(text_data['text']) if word.strip() != ""]
    if valid_texts:
        st.write("Select an index from the list below to replace the corresponding word.")
        for i, word in valid_texts:
            st.write(f"{i}: {word}")

        st.subheader("Replace Text:")
        index_to_replace = st.number_input("Enter the index of the word to replace:", min_value=0, max_value=len(text_data['text'])-1, value=0, step=1)
        new_word_to_insert = st.text_input("Enter the new text:")

        if st.button("Replace Text"):
            modified_image = replace_text_in_image(image, text_data, index_to_replace, new_word_to_insert)
            st.subheader("Modified Image:")
            st.image(modified_image, caption="Modified Image", use_column_width=True)
    else:
        st.write("No text detected in the image.")
else:
    st.write("Please upload an image to get started.")
