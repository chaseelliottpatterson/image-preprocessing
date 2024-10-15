# Interactive Image Tool with Streamlit

This project is an interactive image processing tool built using Python and [Streamlit](https://streamlit.io/). The tool enables users to detect pixel coordinates and apply various image distortions, including barrel distortion, pincushion distortion, cylinder-to-plane transformations, perspective skew, and more. It also supports combining multiple distortions for complex effects.

> **Note**: LaTeX equation embeds are optimized for light mode.

## Features

- **Pixel Coordinate Detection**: Click on the image to retrieve pixel coordinates. The app automatically resizes images that exceed a width of 740 pixels.
- **Image Distortion Effects**:
  - **Barrel Distortion**: Applies radial distortion, causing lines to bulge outward.
  - **Pincushion Distortion**: The inverse of barrel distortion, causing lines to curve inward.
  - **Cylinder to Plane**: Corrects common field-of-view distortions by projecting an image from a cylindrical surface onto a flat plane or the reverse.
  - **Perspective Skew**: Distorts the image using a perspective matrix to simulate viewpoint changes.
  - **Compound Distortion**: Allows for stacking multiple distortions like barrel, pincushion, cylinder-to-plane, and skew for complex effects.
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

### **Barrel Distortion**

Radial distortion causes straight lines to bulge outward, commonly seen in wide-angle lenses.

![Barrel Distortion Formula](https://latex.codecogs.com/png.image?\dpi{110}r'=r\cdot\left(1+k_1\cdot{r}^2+k_2\cdot{r}^4+k_3\cdot{r}^6\right))

#### **Simplified**

![Simplified Barrel Distortion Formula](https://latex.codecogs.com/png.image?\dpi{110}r'=r\cdot\left(1+k_1\cdot{r}^2\right))

Where `k₁` is positive for barrel distortion.

### **Pincushion Distortion**

The inverse of barrel distortion, pincushion distortion curves straight lines inward, commonly seen in telephoto lenses.

![Pincushion Distortion Formula](https://latex.codecogs.com/png.image?\dpi{110}r'=r\cdot\left(1+k_1\cdot{r}^2+k_2\cdot{r}^4+k_3\cdot{r}^6\right))

#### **Simplified**

![Simplified Pincushion Distortion Formula](https://latex.codecogs.com/png.image?\dpi{110}r'=r\cdot\left(1+k_1\cdot{r}^2\right))

Where `k₁` is negitive for pincushion distortion.

### **Cylinder to Plane Distortion**

Projects an image from a cylindrical surface onto a flat plane to correct field-of-view distortions.

![Cylinder to Plane Formula](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7DFOV%3D%5Cfrac%7B%5Ctext%7BLens_Focal_Length%7D%7D%7B%5Ctext%7BFilm_Size%7D%7D%5Ctimes%5Cleft%28%5Cfrac%7B180%7D%7B%5Cpi%7D%5Cright%29)

#### **Inverted (Plane to Cylinder)**

Projects a flat image onto a cylindrical surface, distorting the image as if wrapped around a cylinder.

### **Perspective Skew**

Uses a 3x3 transformation matrix to simulate viewpoint changes.

![Perspective Skew Matrix Formula](https://latex.codecogs.com/png.latex?%5Cdpi%7B110%7D%5Cbegin%7Bpmatrix%7Dx%27%5C%5Cy%27%5C%5Cw%27%5Cend%7Bpmatrix%7D%3D%5Cbegin%7Bpmatrix%7Da%26b%26c%5C%5Cd%26e%26f%5C%5Cg%26h%261%5Cend%7Bpmatrix%7D%5Cbegin%7Bpmatrix%7Dx%5C%5Cy%5C%5C1%5Cend%7Bpmatrix%7D)

The matrix allows for transformations such as skewing and warping the image.

#### **Formula for Perspective Skew**

![Perspective Skew Formula](https://latex.codecogs.com/png.latex?\dpi{110}x'%3D\frac{a\cdot{x}+b\cdot{y}+c}{g\cdot{x}+h\cdot{y}+1},\quad{y}'=\frac{d\cdot{x}+e\cdot{y}+f}{g\cdot{x}+h\cdot{y}+1})

### **Compound Distortion**

Stack multiple distortions (barrel, pincushion, cylinder to plane, and skew) to create complex transformations.

## Contributing

Feel free to open issues or submit pull requests for bug fixes, enhancements, or additional features.

## License

This project is licensed under the MIT License.

