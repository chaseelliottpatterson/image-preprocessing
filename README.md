# Interactive Image Tool with Streamlit
![Barrel Distortion Formula](https://latex.codecogs.com/png.latex?r%27%20%3D%20r%20%5Ccdot%20%5Cleft%28%201%20%2B%20k_1%20%5Ccdot%20r%5E2%20%2B%20k_2%20%5Ccdot%20r%5E4%20%2B%20k_3%20%5Ccdot%20r%5E6%20%5Cright%29)
This project is an interactive image processing tool built using Python and [Streamlit](https://streamlit.io/). The tool enables users to detect pixel coordinates and apply various image distortions, including barrel distortion, pincushion distortion, cylinder-to-plane transformations, perspective skew, and more. It also supports combining multiple distortions for complex effects.

## Features

- **Pixel Coordinate Detection**: Click on the image to retrieve pixel coordinates. The app automatically resizes images that exceed a width of 740 pixels.
- **Image Distortion Effects**:
  - **Barrel Distortion**: Applies radial distortion, causing lines to bulge outward.
  - **Pincushion Distortion**: The inverse of barrel distortion, causing lines to curve inward.
  - **Cylinder to Plane**: Corrects common field-of-view distortions by projecting an image from a cylindrical surface onto a flat plane or the reverse.
  - **Perspective Skew**: Distorts the image using a perspective matrix to simulate viewpoint changes.
  - **Compound Distortion**: Allows for stacking multiple distortions like barrel, pincushion, and skew for complex effects.
- **Support for Image Uploads**: Choose between preloaded images (grid or dog) or upload a custom image.

## Technologies Used

- **Python**
- **Streamlit**: For creating the web interface.
- **Pillow (PIL)**: For basic image processing.
- **NumPy**: Image array manipulation.
- **Wand**: For handling complex image distortions like barrel and perspective.
- **Scikit-image**: Image I/O and additional processing.
- **streamlit-image-coordinates**: Used for pixel coordinate detection.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your_username/interactive-image-tool.git
    cd interactive-image-tool
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Image Selection**: Choose from preloaded images or upload your own.
2. **Pixel Measurements**: Activate the “Image Pixel Information” tool to interactively detect pixel coordinates.
3. **Apply Distortions**: Enable and tweak various distortion effects, such as barrel or pincushion distortion, and adjust sliders to modify distortion parameters.
4. **View Distorted Images**: The app displays the transformed image with the applied effects.
5. **Compound Distortions**: Enable multiple distortions simultaneously to achieve compounded effects.
6. **Cylinder to Plane/Plane to Cylinder**: Use the Cylinder to Plane tool to correct wide-angle distortions or invert the projection for cylindrical effects.

## Available Image Distortions

### **Barrel Distortion**:
Radial distortion causes straight lines to bulge outward, commonly seen in wide-angle lenses.  
\[
r' = r \cdot \left( 1 + k_1 \cdot r^2 + k_2 \cdot r^4 + k_3 \cdot r^6 \right)
\]

#### **Simplified**:
\[
r' = r \cdot \left( 1 + k_1 \cdot r^2 \right)
\]
Where \( k_1 \) is negative for barrel distortion.

### **Pincushion Distortion**:
The inverse of barrel distortion, pincushion distortion curves straight lines inward, commonly seen in telephoto lenses.  
\[
r' = r \cdot \left( 1 + k_1 \cdot r^2 + k_2 \cdot r^4 + k_3 \cdot r^6 \right)
\]

#### **Simplified**:
\[
r' = r \cdot \left( 1 + k_1 \cdot r^2 \right)
\]
Where \( k_1 \) is positive for pincushion distortion.

### **Cylinder to Plane Distortion**:
Projects an image from a cylindrical surface onto a flat plane to correct field-of-view distortions.  
\[
FOV = \frac{\text{Lens Focal Length}}{\text{Film Size}} \times \left( \frac{180}{\pi} \right)
\]

#### **Inverted (Plane to Cylinder)**:
Projects a flat image onto a cylindrical surface, distorting the image as if wrapped around a cylinder.

### **Perspective Skew**:
Uses a 3x3 transformation matrix to simulate viewpoint changes.  
\[
\begin{pmatrix}
x' \\
y' \\
w'
\end{pmatrix}
=
\begin{pmatrix}
a & b & c \\
d & e & f \\
g & h & 1
\end{pmatrix}
\begin{pmatrix}
x \\
y \\
1
\end{pmatrix}
\]

The matrix allows for transformations such as skewing and warping the image.

### **Compound Distortion**:
Stack multiple distortions (barrel, pincushion, cylinder to plane, and skew) to create complex transformations.

## Contributing

Feel free to open issues or submit pull requests for bug fixes, enhancements, or additional features.

## License

This project is licensed under the MIT License.
