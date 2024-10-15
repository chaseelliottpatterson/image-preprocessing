import streamlit as st
from PIL import Image
import numpy as np
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
        if st.session_state['image'] is not None:
            image = st.session_state['image']
            if image.size[1]>740:
                reducer = 740/image.size[0]
                st.session_state['reducer'] = reducer
                new_image = image.resize((math.floor(image.size[0]*reducer),(math.floor(image.size[1]*reducer))))
            else:
                new_image = image
            st.session_state['image'] = new_image
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
            user_options_dict['compound_distortions'] = st.checkbox("Compound (Select options above to compound)")
    return user_options_dict
def convert_wand_to_numpy(image):
    img_buffer = np.asarray(bytearray(image.make_blob()), dtype='uint8')
    wimage = skimage.io.imread(BytesIO(img_buffer))
    return(wimage)

def run_pixel_mesurements(image):
    reducer = st.session_state['reducer']
    if reducer is not None:
        info = f'Image Info: Format-{image.format}, Size-({round(image.size[0]/reducer)}, {round(image.size[1]/reducer)}), Mode-{image.mode}'
    else:
        info = f'Image Info: Format-{image.format}, Size-{image.size}, Mode-{image.mode}'
    st.write(info)

    value = streamlit_image_coordinates(image,key="numpy")
    if value is not None:
        x,y = value["x"],value["y"]
        if reducer is not None:
            x = round(x/reducer)
            y = round(y/reducer)
        st.latex(r"(X,Y): \left( {" + str(x) + r"}, {" + str(y) + r"} \right) ")        
    st.divider()
def run_barrel():
        st.divider()
        wi = WImage.from_array(st.session_state['image'])
        with wi as image:
            image.format = 'jpeg'
            image.alpha_channel = False
            with st.expander("Barrel Distortion Explanation:"):
                f = open('explanations/barrel_markdown.txt', 'r')
                unsplit_markdown = f.read()
                split_markdown=unsplit_markdown.split('|FORMULAHERE|')
                st.markdown(split_markdown[0])
                st.latex(r'''r' = r \cdot \left( 1 + k_1 \cdot r^2 + k_2 \cdot r^4 + k_3 \cdot r^6 \right)''')
                st.markdown(split_markdown[1])
                st.latex(r'''r' = r \cdot \left( 1 + k_1 \cdot r^2 \right)''')
                st.markdown(split_markdown[2])
            a,b,c,d = (0,st.slider("Select Barrel Distortion Amount (k1):", 0.0, 5.0, 2.5),0,1)
            image.distort('barrel', (a,b,c,d))
            wimage = convert_wand_to_numpy(image)
            st.image(wimage, caption="distorted")
def run_pincushion():
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        with st.expander("Pincushion Distortion Explanation:"):
            f = open('explanations/pincushion_markdown.txt', 'r')
            unsplit_markdown = f.read()
            split_markdown=unsplit_markdown.split('|FORMULAHERE|')
            st.markdown(split_markdown[0])
            st.latex(r'''r' = r \cdot \left( 1 + k_1 \cdot r^2 + k_2 \cdot r^4 + k_3 \cdot r^6 \right)''')
            st.markdown(split_markdown[1])
            st.latex(r'''r' = r \cdot \left( 1 + k_1 \cdot r^2 \right)''')
            st.markdown(split_markdown[2])
        a,b,c,d = (0,st.slider("Select Pincushion Distortion Amount (k1):", -.16, 0.0,-0.08),0,1)
        image.distort('barrel', (a,b,c,d))
        wimage = convert_wand_to_numpy(image)
        st.image(wimage, caption="distorted")
def run_cylinder_to_plane():
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False
        with st.expander("Cylinder to Plane Distortion Explanation:"):
            f = open('explanations/cylinder_to_plane_markdown.txt', 'r')
            unsplit_markdown = f.read()
            split_markdown=unsplit_markdown.split('|FORMULAHERE|')
            st.markdown(split_markdown[0])
            st.latex(r'''FOV = \frac{\text{Lens Focal Length}}{\text{Film Size}} \times \left(\frac{180}{\pi}\right)''')
            st.markdown(split_markdown[1])
            st.latex(r'''FOV = \frac{\text{Lens Focal Length}}{\text{Film Size}} \times \left(\frac{180}{\pi}\right)''')
            st.markdown(split_markdown[2])
        invert = st.checkbox("Invert?")
        setting_mode = "Cylinder to Plane"
        if invert:
            setting_mode = "Plane to Cylinder"
        st.write(setting_mode)
        lens = st.slider("Lens Focal Length", 1, 100, 65)
        film = st.slider("Film Size", 1, 100, 35)
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
def run_skew():
        st.divider()
        size = st.session_state['image'].size
        wi = WImage.from_array(st.session_state['image'])
        with wi as image:
            image.format = 'jpeg'
            image.alpha_channel = False
            with st.expander("Perspective Distortion (Skew) Explanation:"):
                f = open('explanations/perspective_skew_markdown.txt', 'r')
                unsplit_markdown = f.read()
                split_markdown=unsplit_markdown.split('|FORMULAHERE|')
                st.markdown(split_markdown[0])
                st.latex(r'''\begin{pmatrix}x' \\y' \\w'\end{pmatrix}=\begin{pmatrix}a & b & c \\d & e & f \\g & h & 1\end{pmatrix}\begin{pmatrix}x \\y \\1\end{pmatrix}''')
                st.markdown(split_markdown[1])
                st.latex(r'''x' = \frac{a \cdot x + b \cdot y + c}{g \cdot x + h \cdot y + 1}  \ y' = \frac{d \cdot x + e \cdot y + f}{g \cdot x + h \cdot y + 1}''')
                st.markdown(split_markdown[2])
                st.latex(r'''(src1x, src1y) \rightarrow (dst1x, dst1y)\\(src2x, src2y) \rightarrow (dst2x, dst2y)\\(src3x, src3y) \rightarrow (dst3x, dst3y)\\(src4x, src4y) \rightarrow (dst4x, dst4y)''')
                st.markdown(split_markdown[3])
                st.latex(r'''\begin{pmatrix}0, 0\end{pmatrix}\rightarrow\begin{pmatrix}14, 4\end{pmatrix}\\\begin{pmatrix}140, 0\end{pmatrix}\rightarrow\begin{pmatrix}126, 9\end{pmatrix}\\\begin{pmatrix}0, 92\end{pmatrix}\rightarrow\begin{pmatrix}0, 92\end{pmatrix}\\\begin{pmatrix}140, 92\end{pmatrix}\rightarrow\begin{pmatrix}140, 92\end{pmatrix}''')
                st.markdown(split_markdown[4])
            source_points = (
                (0, 0),
                (size[0], 0),
                (0, size[1]),
                (size[0], size[1])
            )
            advanced = st.checkbox("Advanced Point Selection")
            destination_points = None
            if advanced:
                if st.session_state['reducer'] is None:
                    txt = st.text_area(f"Please input coordinates in the format listed below: Image size for reference: {size}",placeholder="(src1x,src1y)(dst1x,dst1y)\n(src2x,src2y)(dst2x,dst2y)\n(src3x,src3y)(dst3x,dst3y)\n(src4x,src4y)(dst4x,dst4y)")
                    splitter = txt.replace('\n', "|").replace(' ', "|").replace('(', "|").replace(')', "|").replace(',', "|").split('|')
                    points = []
                    for split in splitter:
                        if split.isdigit():
                            points.append(int(split))
                    if len(points) == 16:
                        error = False
                        tmp = (
                            (points[0], points[1]),
                            (points[4], points[5]),
                            (points[8], points[9]),
                            (points[12], points[13])
                        )
                        destination_points = (
                            (points[2], points[3]),
                            (points[6], points[7]),
                            (points[10], points[11]),
                            (points[14], points[15])
                        )
                        for point in tmp:
                            if point[0] > size[0] or point[0] < 0:
                                error=True
                            if point[1] > size[1] or point[1] < 0:
                                error=True     
                        if not error:
                            source_points=tmp
                        else:
                            st.write("Invalid values setting to default parameters")
                            destination_points = (
                            (0, 0),
                            (size[0], 0),
                            (0, size[1]),
                            (size[0], size[1])
                            )
                    else:
                        st.write("Invalid values setting to default parameters")
                        destination_points = (
                        (0, 0),
                        (size[0], 0),
                        (0, size[1]),
                        (size[0], size[1])
                        )
# valid input for testing
# (0,0)(14,16)      
# (140,0)(126,9)
# (0,92)(0,92)
# (140,92)(140,92)
                else:
                    reducer = st.session_state['reducer']
                    txt = st.text_area(f"Please input coordinates in the format listed below: Image size for reference: ({round(size[0]/reducer)}, {round(size[1]/reducer)})",placeholder="(src1x,src1y)(dst1x,dst1y)\n(src2x,src2y)(dst2x,dst2y)\n(src3x,src3y)(dst3x,dst3y)\n(src4x,src4y)(dst4x,dst4y)")
                    splitter = txt.replace('\n', "|").replace(' ', "|").replace('(', "|").replace(')', "|").replace(',', "|").split('|')
                    points = []
                    for split in splitter:
                        if split.isdigit():
                            points.append(int(split))
                    if len(points) == 16:
                        error = False
                        tmp = (
                            (round(points[0]*reducer), round(points[1]*reducer)),
                            (round(points[4]*reducer), round(points[5]*reducer)),
                            (round(points[8]*reducer), round(points[9]*reducer)),
                            (round(points[12]*reducer), round(points[13]*reducer))
                        )
                        destination_points = (
                            (round(points[2]*reducer), round(points[3]*reducer)),
                            (round(points[6]*reducer), round(points[7]*reducer)),
                            (round(points[10]*reducer), round(points[11]*reducer)),
                            (round(points[14]*reducer), round(points[15]*reducer))
                        )
                        for point in tmp:
                            if point[0] > size[0] or point[0] < 0:
                                error=True
                            if point[1] > size[1] or point[1] < 0:
                                error=True     
                        if not error:
                            source_points=tmp
                        else:
                            st.write("Invalid values setting to default parameters")
                            destination_points = (
                            (0, 0),
                            (size[0], 0),
                            (0, size[1]),
                            (size[0], size[1])
                            )
                    else:
                        st.write("Invalid values setting to default parameters")
                        destination_points = (
                        (0, 0),
                        (size[0], 0),
                        (0, size[1]),
                        (size[0], size[1])
                        )
            else:
                if st.session_state['reducer'] is None:
                    x = st.slider("Basic Destination X Modifier",0,size[0],math.floor(size[0]/2))
                    y = st.slider("Basic Destination Y Modifier",0,size[1],math.floor(size[1]/2))
                    destination_points = (
                        (0, 0),
                        (x, 0),
                        (0, y),
                        (size[0], size[1])
                    )
                else:
                    reducer = st.session_state['reducer']
                    x = st.slider("Basic Destination X Modifier",0,math.floor(size[0]/reducer),math.floor(size[0]/(reducer*2)))
                    y = st.slider("Basic Destination Y Modifier",0,math.floor(size[1]/reducer),math.floor(size[1]/(reducer*2)))
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

def run_compound(barrel, pincushion, cylinder_to_plane, skew):
    st.divider()
    wi = WImage.from_array(st.session_state['image'])
    with wi as image:
        image.format = 'jpeg'
        image.alpha_channel = False

        if barrel:
            barrel_a,barrel_b,barrel_c,barrel_d = (0,st.slider("Select Barrel Distortion Amount (k1):", 0.0, 5.0, 2.5),0,1)
            image.distort('barrel', (barrel_a,barrel_b,barrel_c,barrel_d))

        if pincushion:
            pin_a,pin_b,pin_c,pin_d = (0,st.slider("Select Pincushion Distortion Amount (k1):", -.16, 0.0,-0.08),0,1)
            image.distort('barrel', (pin_a,pin_b,pin_c,pin_d))

        if cylinder_to_plane:
            invert = st.checkbox("Invert?")
            fov = st.slider("FOV angle", 1, 160, 1)
            if invert:
                st.write("Plane to Cylinder")
                image.distort('cylinder_2_plane', (fov,))
            else:
                st.write("Cylinder to Plane")
                image.distort('plane_2_cylinder', (fov,))

        if skew:
            size = st.session_state['image'].size
            source_points = (
                (0, 0),
                (size[0], 0),
                (0, size[1]),
                (size[0], size[1])
            )
            destination_points = None
            if st.session_state['reducer'] is None:
                    x = st.slider("Basic Destination X Modifier",0,size[0],math.floor(size[0]/2))
                    y = st.slider("Basic Destination Y Modifier",0,size[1],math.floor(size[1]/2))
                    destination_points = (
                        (0, 0),
                        (x, 0),
                        (0, y),
                        (size[0], size[1])
                    )
            else:
                reducer = st.session_state['reducer']
                x = st.slider("Basic Destination X Modifier",0,math.floor(size[0]/reducer),math.floor(size[0]/(reducer*2)))
                y = st.slider("Basic Destination Y Modifier",0,math.floor(size[1]/reducer),math.floor(size[1]/(reducer*2)))
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
        st.image(wimage, caption="Distorted")
        st.write("Note: Distortion explanations provided while not compounded")

def main():
    explanations = set_explanations()
    st.set_page_config(layout="centered")
    st.title("Interactive Image Tool")
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
                run_barrel()
        if user_options_dict['pincushion'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_pincushion()
        if user_options_dict['cylinder_to_plane'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_cylinder_to_plane()
        if user_options_dict['skew'] and not user_options_dict['compound_distortions']:
            with st.spinner():
                run_skew()
        if user_options_dict['compound_distortions']:
            run_compound(user_options_dict['barrel'],user_options_dict['pincushion'],user_options_dict['cylinder_to_plane'],user_options_dict['skew'])
                
if __name__ == '__main__':
    main()