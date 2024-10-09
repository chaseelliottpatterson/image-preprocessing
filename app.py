import streamlit as st
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

if 'image' not in st.session_state:
    st.session_state['image'] = None

st.title("Image Tool")
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
        st.session_state['image'] = image
if st.session_state['image'] is not None:
    with st.expander("Distortions"):
        barrel_pincushion= st.checkbox("Barrel/Pincushion")
        skew= st.checkbox("Skew")

    st.image(st.session_state['image'])
    img_array = np.array(st.session_state['image'])
    if barrel_pincushion:
        distortion = st.slider("Pincushion to Barreled", -1.0, 1.0, 0.0)
        st.write(distortion)