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
    explanations['barrel2'] = ''' Where r is the destination radius. The arguments for the distortion are:  \n A B C D X Y  \n For this example X,Y are auto-calculated, and A is being modified below since it is the highest contributer to the equasion '''
    explanations['pincushion1'] = '''The barrel inverse distortion has the same arguments as the barrel distortion, but performs a different equation.'''
    explanations['pincushion2'] = '''It does not exactly reverse, or undo, the effects of the barrel distortion.'''
    return explanations
def form_contents():
    image_options = st.radio("Image you would like to use", ["Grid", "Dog", "Custom Upload"] )
    img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
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
def user_options():
    user_options_dict = {}
    with st.expander("Distortions"):
            user_options_dict['barrel'] = st.checkbox("Barrel")
            user_options_dict['pincushion'] = st.checkbox("Pincushion")
            user_options_dict['skew'] = st.checkbox("Skew")
            user_options_dict['compound_distortions'] = st.checkbox("Compound (distort in sequence for stacking distortions)")
    return user_options_dict
def convert_wand_to_numpy(image):
    img_buffer = np.asarray(bytearray(image.make_blob()), dtype='uint8')
    wimage = skimage.io.imread(BytesIO(img_buffer))
    return(wimage)

def run_barrel(explanations):
        st.divider()
        wi = WImage.from_array(st.session_state['image'])
        with wi as image:
            image.format = 'jpeg'
            image.alpha_channel = False
            with st.expander("Barrel Distortion Explanation"):
                st.write(explanations['barrel1'])
                st.image(Image.open('ExampleImages/barrel.png'))
                st.write(explanations['barrel2'])
            a,b,c,d = (st.slider("Barrel Distortion Amount", 0.0, 1.0, 0.0),0,0,1)
            image.distort('barrel', (a,b,c,d))
            wimage = convert_wand_to_numpy(image)
            st.image(wimage)
def run_pincushion(explanations):
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        with st.expander("Pincushion Distortion Explanation"):
            pass
            st.write(explanations['pincushion1'])
            st.image(Image.open('ExampleImages/pincushion.png'))
            st.write(explanations['pincushion2'])
        a,b,c,d = (st.slider("Pincushion Distort Amount", 0.0, .1, 0.0),0,0,1)
        image.distort('barrel_inverse', (a,b,c,d))
        wimage = convert_wand_to_numpy(image)
        st.image(wimage)
def run_compound(barrel, pincushion):
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        barrel_a,barrel_b,barrel_c,barrel_d = (st.slider("Barrel Distort Amount", 0.0, 1.0, 0.0),0,0,1)
        pin_a,pin_b,pin_c,pin_d = (st.slider("Pincushion Distort Amount", 0.0, .1, 0.0),0,0,1)
        image.distort('barrel', (barrel_a,barrel_b,barrel_c,barrel_d))
        image.distort('barrel_inverse', (pin_a,pin_b,pin_c,pin_d))
        wimage = convert_wand_to_numpy(image)
        st.image(wimage, caption="Distorted")
        st.write("Note: Distortion explanations provided while not compounded")

def main():
    explanations = set_explanations()
    st.title("Image Tool")
    with st.form("my_form"):
        form_contents()
    if st.session_state['image'] is not None:
        user_options_dict = user_options()
        st.image(st.session_state['image'],caption="original",)
        if user_options_dict['barrel'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_barrel(explanations)
        if user_options_dict['pincushion'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_pincushion(explanations)
        if user_options_dict['compound_distortions']:
            run_compound(user_options_dict['barrel'],user_options_dict['pincushion'])

                    

                

if __name__ == '__main__':
    main()