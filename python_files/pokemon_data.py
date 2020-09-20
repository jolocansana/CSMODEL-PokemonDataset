import matplotlib.image as img 
import matplotlib.pyplot as plt 
from scipy.cluster.vq import whiten 
from scipy.cluster.vq import kmeans2 
import pandas as pd
import numpy as np

# used to store the resulting value from getting dominant color
class Color:
      def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.rgb = (r, g, b)

class PokeData:
  # initialize k
  # k will be used to set the threshold in kmeans clustering
  def __init__(self, k):
    self.k = k

  # called when need to get the dominant color in an image
  def get_from_image (self, image):
    r = [] 
    g = [] 
    b = [] 
    
    # append each pixel (formatted to RGB) to r, g, b array respectively
    for row in image: 
      for temp_r, temp_g, temp_b, temp_alpha in row:
        if (temp_alpha != 0):
          # multiply colors by 255, as rgb values in matplot.image saves pixels as rgb values scaled from 0 -> 1
          r.append(temp_r * 255) 
          g.append(temp_g * 255) 
          b.append(temp_b * 255)    

    # get most dominant color from the r, g, b values
    return self.get_dominant_color(r, g, b)

  # called when need to get the dominant color per type
  def get_from_series (self, series):
    r = []
    g = []
    b = []

    # append each row (formatted to class Color) to r, g, b array respectively
    for row in series:
        if(type(row) != str):
            # multiply colors by 255, as rgb values in matplot.image saves pixels as rgb values scaled from 0 -> 1
            r.append(row.r * 255) 
            g.append(row.g * 255) 
            b.append(row.b * 255)

    # get most dominant color from the r, g, b values
    return self.get_dominant_color(r, g, b)

  # uses the kmeans clustering method to find the dominant colors in the image
  def get_dominant_color(self, r, g, b):
    """
      Params:
        matplotlib.image, image data of pokemon
      Returns:
        Tuple: dominant color of pokemon
    """ 

    # make a dataframe from arrays r, g, b
    image_df = pd.DataFrame({'red' : r, 
                              'green' : g, 
                              'blue' : b}) 

    # we whiten first before executing kmeans in order to normalize the data
    image_df['scaled_color_red'] = whiten(image_df['red']) 
    image_df['scaled_color_blue'] = whiten(image_df['blue']) 
    image_df['scaled_color_green'] = whiten(image_df['green']) 

    # execute kmeans with k
    # cluster_centers holds the k number of centroids
    # clusters holds the cluster sets
    cluster_centers, clusters = kmeans2(image_df[['scaled_color_red', 
                                        'scaled_color_green', 
                                        'scaled_color_blue']], self.k) 
      
    dominant_colors = [] 

    # get standard deviation of each color
    red_std, green_std, blue_std = image_df[['red', 
                                              'green', 
                                              'blue']].std() 

    # to generate dominant colors, find cluster cetners, and scale with regards to standard dev
    for cluster_center in cluster_centers: 
        red_scaled, green_scaled, blue_scaled = cluster_center 
        dominant_colors.append(( 
            red_scaled * red_std / 255, 
            green_scaled * green_std / 255, 
            blue_scaled * blue_std / 255
        )) 
      
    # get the count of the pixels within each cluster
    np.bincount(clusters)

    # get the color with the max mode and set it as the dom
    dom = dominant_colors[np.where(np.bincount(clusters) == np.bincount(clusters).max())[0][0]]
    return Color(dom[0], dom[1], dom[2])