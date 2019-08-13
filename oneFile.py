# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class oneFile():
    def __init__(self, path = None):
        if path is None:
            self.path = '/'
        self.path = self.path + 'slice_data0'
        pdf=pd.read_csv('slice_data0.csv', delimiter = ',', skiprows = 1,
                        names = ["Q", "vx", "vy", "vz", "vx_avg", "vy_avg", "vz_avg",
                                 "vx_prime", "vy_prime", "vz_prime", "vx_y",
                                 "vy_z", "vz_x", "p", "p_avg", 'p_prime', "x", "y", "z"])
        pdf.to_hdf('slice_data0.h5',key='df')
        self.data = pd.read_hdf('slice_data0.h5', key='df')
        self.data['v_mag'] = (self.data['vx']**2 + self.data['vy']**2)**0.5
        self.data['vx_fluc'] = self.data['vx'] - self.data['vx_avg']
        self.data['vy_fluc'] = self.data['vy'] - self.data['vy_avg']
        self.data['v_fluc'] = (self.data['vx_fluc']**2 + self.data['vy_fluc']**2)**0.5
        
    def contour_plot_vmag(self, z = None, x = None, y = None):
        if x is None:
            x = self.data['x']
        if y is None:
            y = self.data['y']
        if z is None:
            z = self.data['v_mag']
        fig, ax = plt.subplots(figsize=(22, 8))
        #ax.tricontour(x, y, z, levels=14, linewidths=0.5, colors='k')
        contour = ax.tricontourf(x, y, z, levels=200, cmap="rainbow")
        #ax.scatter(x, y, z)
        fig.colorbar(contour)
        #ax2.set_title('tricontour (%d points)' % npts)
        
    def contour_plot_vfluc(self, z = None, x = None, y = None):
        if x is None:
            x = self.data['x']
        if y is None:
            y = self.data['y']
        if z is None:
            z = self.data['v_fluc']
        fig, ax = plt.subplots(figsize=(22, 8))
        #ax.tricontour(x, y, z, levels=14, linewidths=0.5, colors='k')
        contour = ax.tricontourf(x, y, z, levels=200, cmap="rainbow")
        #ax.scatter(x, y, z)
        fig.colorbar(contour)
        #ax2.set_title('tricontour (%d points)' % npts)

#    def contour_plot_epsilon(self):
#        # sort values in x axis
#        self.data.sort_values('x', inplace = True)
#        return 
    
    
    def test(self):
        self.path = self.path + 'slice_data0'
        print(self.path)
        return 0

a = oneFile()
print(a.data)
a.contour_plot_vfluc()