import sys, os

import numpy as np
from collections import OrderedDict

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

import pyplotbrain as ppb
#import mycolors

import matplotlib.pyplot as plt




def hex_to_rgb(c1, alpha =1.):
    if c1 is None:
        return (.9, .9, .9, .9)
    c1 = str(c1)
    r = int(c1[1:3],16)/255.
    g = int(c1[3:5],16)/255.
    b = int(c1[5:7],16)/255.
    return (r, g, b, alpha)
    
def plot_graphs(channel_names,channel_coords,signif_diff_mat,export_path,pref):
    
    #TODO FIXME: pourquoi Y est a l'envers ?????
    #~ coords[:,1] = -coords[:,1]
    
    
    app = pg.mkQApp()
    view = ppb.addView(with_config = True)#, cortical_alpha = .4)
    
    view.plot_mesh()
    
    
    ################## tous les noeuds ont la meme couleur ##########################

    view.add_node(channel_coords, color =  (1,0,0), size = 2)
    
    ################## adding connectivity matrix
    
    scale_signif_diff_mat = signif_diff_mat
    
    
    print scale_signif_diff_mat
    
    cmap = plt.get_cmap('jet')
    
    cmap_vals = cmap(np.linspace(0.2,0.8,9))
    
    print cmap_vals
    
    cmap_vals[:,3] = .7
    
    
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == 1,dtype = int) * 2,color = cmap_vals[5])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == 2,dtype = int) * 4,color = cmap_vals[6])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == 3,dtype = int) * 8,color = cmap_vals[7])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == 4,dtype = int) * 16,color = cmap_vals[8])
    
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == -1,dtype = int) * 2,color = cmap_vals[3])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == -2,dtype = int) * 4,color = cmap_vals[2])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == -3,dtype = int) * 8,color = cmap_vals[1])
    view.add_edge(channel_coords,np.array(scale_signif_diff_mat == -4,dtype = int) * 16,color = cmap_vals[0])
    
    view.resize(1200,800)
    
    ## from right
    view.glview.setCameraPosition(distance = 250,elevation = 0, azimuth = 0)
    view.to_file(os.path.join(export_path,pref + '_from_right.png'))
    
    ### from front
    view.glview.setCameraPosition(distance = 280,azimuth = 90,elevation = 0)
    view.to_file(os.path.join(export_path,pref + '_from_front.png'))

    ### from top
    view.glview.setCameraPosition(distance = 250,azimuth = 180,elevation = 90)
    view.to_file(os.path.join(export_path,pref + '_from_top.png'))

    ### from left
    view.glview.setCameraPosition(distance = 250,azimuth = 180,elevation = 0)
    view.to_file(os.path.join(export_path,pref + '_from_left.png'))

    #self.glview .setCameraPosition(160,160,15)
    app.exec_()
    