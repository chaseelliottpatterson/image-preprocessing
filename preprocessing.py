import logging
import numpy as np
import pandas
import PIL
from PIL import Image 
import matplotlib.pyplot as plt

def generate_grid():
    grid_height, grid_width = 9,9
    logging.getLogger().info(f"Generating Grid with dimentions{grid_height}x{grid_width}")
    generated_grid = np.zeros((grid_height, grid_width,3), dtype=np.uint8)
    counter = 0
    for i in range(grid_height):
        for j in range(grid_width):
            counter = counter + 1
            if counter % 2 == 0:
                generated_grid[i,j]=[255,255,255]
    plt.imshow(generated_grid)
    plt.axis('off')
    plt.show()
    

def numpy_tweak(image):
    # pass
    np_img = np.array(image)
    # print(np_img)
    plt.imshow(np_img)
    plt.axis('off')
    plt.show()

def import_image():
    logging.getLogger().info(f'Pillow Version:{PIL.__version__}')
    image = Image.open('ExampleImages/dog.jpg')
    logging.getLogger().info(f'Image Info: Format-{image.format}, Size-{image.size}, Mode-{image.mode}')
    return image

def start_logger():
    # Logger order: debug,info,warning,error,critical
    logging.basicConfig(filename="preprocessing.log", format='%(asctime)s %(message)s', filemode='w')
    logging.getLogger().setLevel(logging.INFO) # Setting the threshold of logger to DEBUG
    logging.getLogger().info("Logger Started")

def main():
    start_logger()
    image = import_image()    
    numpy_tweak(image)
    # generate_grid()
    
if __name__ == '__main__':
    main()