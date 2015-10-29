import sys, os

import numpy as np
from collections import OrderedDict

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

import pyplotbrain as ppb
#import mycolors

import matplotlib.pyplot as plt

from webcolors import name_to_rgb


def hex_to_rgb(c1, alpha =1.):
    if c1 is None:
        return (.9, .9, .9, .9)
    c1 = str(c1)
    r = int(c1[1:3],16)/255.
    g = int(c1[3:5],16)/255.
    b = int(c1[5:7],16)/255.
    return (r, g, b, alpha)
    
def plot_signif_graphs(channel_names,channel_coords,signif_diff_mat,export_path,pref,cortical_alpha = 0.5,graph_alpha = 1.0):
    
    #TODO FIXME: pourquoi Y est a l'envers ?????
    #~ coords[:,1] = -coords[:,1]
    
    
    app = pg.mkQApp()
    view = ppb.addView(with_config = True)#, cortical_alpha = .4)
    
    view.plot_mesh()
    
    view.change_alpha_mesh()
    
    view.params['cortical_alpha'] =  cortical_alpha
    
    
    ################## tous les noeuds ont la meme couleur ##########################

    view.add_node(channel_coords, color =  (1,0,0), size = 2)
    
    ################## adding connectivity matrix
    
    scale_signif_diff_mat = signif_diff_mat
    
    
    print scale_signif_diff_mat
    
    
    #dict_cmap_vals = {'1':'orange','-1':'blue' }
    
    
    cmap = plt.get_cmap('jet')
    
    cmap_vals = cmap(np.linspace(0.2,0.8,9))
    
    print cmap_vals
    
    cmap_vals[:,3] = graph_alpha
    
    
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
    
def plot_thr_cor_graphs(channel_names,channel_coords,thr_cor_mat,export_path,pref,cortical_alpha = 0.5,graph_alpha = 1.0,nodes_mag = 20,edges_mag = 50):
    
    #TODO FIXME: pourquoi Y est a l'envers ?????
    #~ coords[:,1] = -coords[:,1]
    
        
    app = pg.mkQApp()
    
    view = ppb.addView(with_config = True)
    
    view.plot_mesh()

    view.params['cortical_alpha'] =  cortical_alpha
    #view.params['cortical_alpha'] =  0.5
    #view.params['cortical_alpha'] =  0.1

    view.change_alpha_mesh()
    
    dict_cmap_vals = {'1.0':'orange','0.0':'black','-1.0':'blue' }
    
    signif_cor_strength = np.sum(thr_cor_mat,axis = 0)
    
    print signif_cor_strength
    
    #view.add_node(np.random.randn(n, 3)*20, color =  (0,1,1,0.8), size = 10)
    
    for sign_strength in np.unique(np.sign(signif_cor_strength)):
    
        print sign_strength
        
        col = tuple([rgb_val/255.0 for rgb_val in name_to_rgb(dict_cmap_vals[str(sign_strength)])] + [graph_alpha])
        
        print col
        
        node_coords = channel_coords[np.sign(signif_cor_strength) == sign_strength]        
        print node_coords
        
        node_sizes = np.abs(signif_cor_strength[np.sign(signif_cor_strength) == sign_strength])  
        print node_sizes
        
        view.add_node(node_coords, color =  col, size = node_sizes*nodes_mag)
    
    ################## tous les noeuds ont la meme couleur ##########################

    ################## adding connectivity matrix
    
    print thr_cor_mat
    
    
    for sign_cor in np.unique(np.sign(thr_cor_mat)):
        
        print sign_cor
        
        col = tuple([rgb_val/255.0 for rgb_val in name_to_rgb(dict_cmap_vals[str(sign_cor)])] + [graph_alpha])
        
        print col
        
        
        #edge_sizes = thr_cor_mat[np.sign(thr_cor_mat) ==  sign_cor]
        
        edge_sizes = np.array(np.sign(thr_cor_mat) ==  sign_cor,dtype = int) * np.abs(thr_cor_mat)
        
        
        print edge_sizes
        print edge_sizes.shape
        
        view.add_edge(channel_coords,edge_sizes*edges_mag,color = col)
        
        
    #scale_signif_diff_mat = thr_cor_mat
    
    
    #print scale_signif_diff_mat
    
    view.resize(1200,800)
    
    ### from top
    view.glview.setCameraPosition(distance = 250,azimuth = 180,elevation = 90)
    view.to_file(os.path.join(export_path,pref + '_from_top.png'))

    #self.glview .setCameraPosition(160,160,15)
    app.exec_()