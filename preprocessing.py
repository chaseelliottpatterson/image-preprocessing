import logging
import numpy as np
import pandas
from PIL import Image 
import matplotlib.pyplot as plt

def start_logger():
    # Logger order: debug,info,warning,error,critical
    logging.basicConfig(filename="preprocessing.log", format='%(asctime)s %(message)s', filemode='w')
    logging.getLogger().setLevel(logging.INFO) # Setting the threshold of logger to DEBUG
    logging.getLogger().info("Logger Started")

def main():
    start_logger()    
    print()
    a = [[0,1,0],[1,0,1]]
    plt.imshow(a,cmap='gray')
    plt.show()

if __name__ == '__main__':
    main()