import streamlit as st
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
import skimage.io
from wand.image import Image as WImage


if 'image' not in st.session_state:
    st.session_state['image'] = None
def set_explanations():
    explanations = {}
    explanations['barrel1'] = 'Barrel distortion attempts to correct spherical distortion caused by camera lenses. It operates with four constant coefficient values A, B, C, & D mapped to the images EXIF meta-data. Usually camera, lens, and zoom attributes. The equation for barrel distortion is:'
    explanations['barrel2'] = ''' Where r is the destination radius. The arguments for the distortion are:
                                    \n A B C D X Y 
                                     \n For this example X,Y are auto-calculated, and A is being modified below since it is the highest contributer to the equasion '''
    return explanations
def main():
    explanations = set_explanations()
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
            barrel= st.checkbox("Barrel")
            skew= st.checkbox("Skew")

        st.image(st.session_state['image'],caption="original",)
        img_array = np.array(st.session_state['image'])
        # if barrel_pincushion:
        #     st.divider()
        #     distortion = st.slider("Pincushion to Barreled", -1.0, 1.0, 0.0)
        #     st.write(distortion)
        # if skew:
        #     st.divider()
        #     h_skew = st.slider("Horizontal Skew", -1.0, 1.0, 0.0)
        #     v_skew = st.slider("Vertical Skew", -1.0, 1.0, 0.0)
        
        with st.spinner():
            wi = WImage.from_array(st.session_state['image'])
            with wi as image:
                image.format = 'jpeg'
                image.alpha_channel = False
                if barrel:
                    st.divider()
                    with st.expander("Barrel Distortion Explanation"):
                        st.write(explanations['barrel1'])
                        st.image(Image.open('ExampleImages/barrel.png'))
                        st.write(explanations['barrel2'])
                    a,b,c,d = (st.slider("Distortion Amount", 0.0, 1.0, 0.0),0,0,1)
                    image.distort('barrel', (a,b,c,d))
                    
                    img_buffer = np.asarray(bytearray(image.make_blob()), dtype='uint8')
                    wimage = skimage.io.imread(BytesIO(img_buffer))
                    st.image(wimage)
                

if __name__ == '__main__':
    main()