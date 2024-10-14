import streamlit as st
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import chain
from streamlit_image_coordinates import streamlit_image_coordinates

from io import BytesIO
import skimage.io
from wand.image import Image as WImage

if 'image' not in st.session_state:
    st.session_state['image'] = None

if 'reducer' not in st.session_state:
    st.session_state['reducer'] = None


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
        if 'image' not in st.session_state:
            st.session_state['image'] = None
        else:
            st.session_state['image'] = None
        if 'reducer' not in st.session_state:
            st.session_state['reducer'] = None
        else:
            st.session_state['reducer'] = None
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
    with st.expander("Options"):
            st.divider()
            st.write("Tools:")
            user_options_dict['pixel_measurements'] = st.checkbox("Image Pixel Information")
            st.divider()
            st.write("Distortions:")
            user_options_dict['barrel'] = st.checkbox("Barrel")
            user_options_dict['pincushion'] = st.checkbox("Pincushion")
            user_options_dict['cylinder_to_plane'] = st.checkbox("Cylinder to Plane")
            user_options_dict['skew'] = st.checkbox("Perspective Skew")
            user_options_dict['compound_distortions'] = st.checkbox("Compound (distort in sequence for stacking distortions)")
    return user_options_dict
def convert_wand_to_numpy(image):
    img_buffer = np.asarray(bytearray(image.make_blob()), dtype='uint8')
    wimage = skimage.io.imread(BytesIO(img_buffer))
    return(wimage)

def run_pixel_mesurements(image):
    info = f'Image Info: Format-{image.format}, Size-{image.size}, Mode-{image.mode}'
    reducer = None
    if image.size[1]>740:
        reducer = 740/image.size[0]
        info = info + f" | Image over max size, resizing to {math.floor(image.size[0]*reducer)}x{math.floor(image.size[1]*reducer)}"
        new_image = image.resize((math.floor(image.size[0]*reducer),(math.floor(image.size[1]*reducer))))
    else:
        new_image = image
    st.write(info)

    value = streamlit_image_coordinates(new_image,key="numpy")

    if value is not None:
        x,y = value["x"],value["y"]
        result = ""
        if reducer is not None:
            x = math.floor(x/reducer)
            y = math.floor(y/reducer)
            result = "  *This value has been retroactivly calculated from resizing process"
        resut = f"(X,Y): ({x},{y})" + result
        st.write(resut)
    st.divider()
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
            st.image(wimage, caption="distorted")
def run_pincushion(explanations):
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        with st.expander("Pincushion Distortion Explanation"):
            st.write(explanations['pincushion1'])
            st.image(Image.open('ExampleImages/pincushion.png'))
            st.write(explanations['pincushion2'])
        a,b,c,d = (st.slider("Pincushion Distort Amount", 0.0, .1, 0.0),0,0,1)
        image.distort('barrel_inverse', (a,b,c,d))
        wimage = convert_wand_to_numpy(image)
        st.image(wimage, caption="distorted")
def run_cylinder_to_plane(explanations):
    st.divider()
    invert = st.checkbox("Invert?")
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        expander_text = "Cylinder to Plane"
        if invert:
            expander_text = "Plane to Cylinder"
        with st.expander(expander_text):
            # st.write(explanations['pincushion1'])
            # st.image(Image.open('ExampleImages/pincushion.png'))
            # st.write(explanations['pincushion2'])
            st.write("TODO")
        lens = st.slider("lens", 1, 100, 1)
        film = st.slider("film", 1, 100, 1)
        fov_angle = (lens/film) * (180/math.pi)
        if fov_angle > 160:
            fov_angle = 160
            st.write("FOV angle over 160, setting to 160")
        st.write(f"FOV angle: {fov_angle:.1f}")
        if invert:
            image.distort('cylinder_2_plane', (fov_angle,))
        else:
            image.distort('plane_2_cylinder', (fov_angle,))
        wimage = convert_wand_to_numpy(image)
        st.image(wimage, caption="distorted")
def run_skew(explanations):
        st.divider()
        size = st.session_state['image'].size
        wi = WImage.from_array(st.session_state['image'])
        with wi as image:
            image.format = 'jpeg'
            image.alpha_channel = False
            with st.expander("Perspective"):
                st.write("TODO")
                
                # st.write(explanations['barrel1'])
                # st.image(Image.open('ExampleImages/barrel.png'))
                # st.write(explanations['barrel2'])
            source_points = (
                (0, 0),
                (size[0], 0),
                (0, size[1]),
                (size[0], size[1])
            )
            advanced = st.checkbox("Advanced Point Selection")
            destination_points = None
            if advanced:
                st.write(st.session_state['reducer'])
                if st.session_state['reducer'] is None:
                    txt = st.text_area(f"Please input coordinates in the format listed below: Image size for reference: {size}","(x1,y1)\n(x2,y2)\n(x3,y3)\n(x4,y4)")
                    st.write(txt)
                    destination_points = (
                        (0, 0),
                        (size[0], 0),
                        (0, size[1]),
                        (size[0], size[1])
                    )
                else:
                    destination_points = (
                        (0, 0),
                        (size[0], 0),
                        (0, size[1]),
                        (size[0], size[1])
                    )
            else:
                if st.session_state['reducer'] is None:
                    x = st.slider("x",0,size[0],math.floor(size[0]/2))
                    y = st.slider("y",0,size[1],math.floor(size[1]/2))
                    destination_points = (
                        (0, 0),
                        (x, 0),
                        (0, y),
                        (size[0], size[1])
                    )
                else:
                    reducer = st.session_state['reducer']
                    x = st.slider("x",0,math.floor(size[0]/reducer),math.floor(size[0]/(reducer*2)))
                    y = st.slider("y",0,math.floor(size[1]/reducer),math.floor(size[1]/(reducer*2)))
                    destination_points = (
                        (0, 0),
                        (math.floor(x*reducer), 0),
                        (0, math.floor(y*reducer)),
                        (size[0], size[1])
                    )

            order = chain.from_iterable(zip(source_points, destination_points))
            arguments = list(chain.from_iterable(order))
            image.distort('perspective', arguments)
            wimage = convert_wand_to_numpy(image)
            st.image(wimage, caption="distorted")

def run_compound(barrel, pincushion, cylinder_to_plane, plane_to_cylinder):
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
    st.set_page_config(layout="centered")
    st.title("Imaging Tool")
    with st.form("my_form"):
        form_contents()
    if st.session_state['image'] is not None:
        image = st.session_state['image']
        if image.size[1]>740:
            reducer = 740/image.size[0]
            st.session_state['reducer'] = reducer
            new_image = image.resize((math.floor(image.size[0]*reducer),(math.floor(image.size[1]*reducer))))
        else:
            new_image = image
        st.session_state['image'] = new_image
        user_options_dict = user_options()
        purged_dict = user_options_dict.copy()
        del purged_dict['pixel_measurements']
        if True not in user_options_dict.values():
            st.image(st.session_state['image'],caption="original")
        if user_options_dict['pixel_measurements']:
            run_pixel_mesurements(image)
        if True in purged_dict.values():
            st.image(st.session_state['image'],caption="original")
        if user_options_dict['barrel'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_barrel(explanations)
        if user_options_dict['pincushion'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_pincushion(explanations)
        if user_options_dict['cylinder_to_plane'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_cylinder_to_plane(explanations)
        if user_options_dict['skew'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_skew(explanations)
        if user_options_dict['compound_distortions']:
            run_compound(user_options_dict['barrel'],user_options_dict['pincushion'],user_options_dict['cylinder_to_plane'])
               

if __name__ == '__main__':
    main()