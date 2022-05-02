#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import cv2
import numpy as np
#import matplotlib.pyplot as plt
import maxflow 

# Important parameter
# Higher values means making the image smoother
smoothing = 1000

 
# function to get the images path 
def get_imlist(path):
    """ Return a list of filenames for 
    all jpg images in directory """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

# use the function 'get_imlist'  to call the images' path
imlist = get_imlist('../images/')
#counter
i = 0

#process the denoising for all the images in 'imlist'
for im in imlist:
    # Load the image
    img = cv2.imread(im, cv2.IMREAD_UNCHANGED)
    
    # percent of original size
    scale_percent = 90qqqqqq
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    #convert it to grayscale image
    resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    #plt.contour(img, origin='image'), plt.axis('equal'), plt.axis('off')
    #binarize the image and save as uint8
    img_bin = 255 * (resized > 128).astype(np.uint8)

    # Create the graph.
    g = maxflow.Graph[int]()
    # Add the nodes. nodeids has the identifiers of the nodes in the grid.
    nodeids = g.add_grid_nodes(img_bin.shape)
    # Add non-terminal edges with the same capacity.
    g.add_grid_edges(nodeids, smoothing)
    # Add the terminal edges. The image pixels are the capacities
    # of the edges from the source node. The inverted image pixels
    # are the capacities of the edges to the sink node.
    g.add_grid_tedges(nodeids, img_bin, 255-img_bin)

    # Find the maximum flow.
    g.maxflow()
    # Get the segments of the nodes in the grid.
    sgm = g.get_grid_segments(nodeids)

    # The labels should be 1 where sgm is False and 0 otherwise.
    img_denoised = np.logical_not(sgm).astype(np.uint8) * 255
    

    # Show the result.
#    plt.subplot(141), plt.imshow(resized, cmap='gray'), plt.title('resized image')
#    plt.subplot(142), plt.imshow(img_bin, cmap='gray'), plt.title('Binary image')
#    plt.subplot(143), plt.imshow(img_denoised, cmap='gray'), plt.title('Denoised binary image')
#    plt.show()
    while True:
        
        cv2.imshow('resized image', resized)
        cv2.imshow('Binary image', img_bin)
        cv2.imshow('Denoised binary image', img_denoised)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
#    
    i += 1
    # Save denoised image
    cv2.imwrite('../results/img_denoised'+ str(i) +'.png', img_denoised)
#   print('Original Dimensions : ',img.shape)
#    print('Resized Dimensions : ',resized.shape)
