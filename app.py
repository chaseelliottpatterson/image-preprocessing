import streamlit as st
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
import skimage.io
from wand.image import Image as WImage

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
        st.divider()
        distortion = st.slider("Pincushion to Barreled", -1.0, 1.0, 0.0)
        st.write(distortion)
    if skew:
        st.divider()
        h_skew = st.slider("Horizontal Skew", -1.0, 1.0, 0.0)
        v_skew = st.slider("Vertical Skew", -1.0, 1.0, 0.0)
    
    with st.spinner():
        wi = WImage.from_array(st.session_state['image'])
        with wi as image:
            image.format = 'jpeg'
            image.alpha_channel = False
            # arguments = (0, 0, 20, 60,
            #             90, 0, 70, 63,
            #             0, 90, 5, 83,
            #             90, 90, 85, 88)
            # image.distort('perspective', arguments)
            args = (
                0.2,  # A
                0.0,  # B
                0.0,  # C
                1.0,  # D
            )
            image.distort('barrel', args)
            img_buffer = np.asarray(bytearray(image.make_blob()), dtype='uint8')
        wimage = skimage.io.imread(BytesIO(img_buffer))
        st.image(wimage)

