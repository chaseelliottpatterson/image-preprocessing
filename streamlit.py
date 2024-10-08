import streamlit as st
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

st.title("Image Tool")
# st.file_uploader("uploaded_image",label_visibility="hidden")
pil_image = None
with st.form("my_form"):
    image_options = st.radio("Image you would like to use", ["Grid", "Dog", "Custom Upload"] )
    
    img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        if image_options == "Grid":
            image = Image.open('ExampleImages/grid.jpeg')
        elif image_options == "Dog":
            image = Image.open('ExampleImages/dog.jpg')
        elif image_options == "Custom Upload":
            image = Image.open(img_file_buffer)

        st.write(f'Image Info: Format-{image.format}, Size-{image.size}, Mode-{image.mode}')
        pil_image = image
st.image(pil_image)
img_array = np.array(pil_image)