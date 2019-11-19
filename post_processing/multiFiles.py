# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:31:51 2019

@author: zding5
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from matplotlib.ticker import AutoMinorLocator
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class multiFiles():
    def __init__(self, path = None):
        self.line_style = [
                     ('solid',                (0, (1, 0))),
                     ('dotted',                (0, (1, 1))),
                
                     ('dashed',                (0, (5, 5))),
                     ('densely dashed',        (0, (5, 1))),
                
                     ('dashdotted',            (0, (3, 5, 1, 5))),
                     ('densely dashdotted',    (0, (3, 1, 1, 1))),
                
                     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5)))]

    def readData(self, path):
        if not os.path.isfile(path+'/cloud.h5'):
            pdf=pd.read_csv(path+'/cloud.out', delimiter = ' ', names = ["t", "x", "y", "z",
               "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
               "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
            pdf['v_mag'] = (pdf['vx']**2 + pdf['vy']**2)**0.5
            pdf.sort_values('t', inplace=True)
            pdf.to_hdf(path + '/cloud.h5',key='cloud')
    def plot_w_t(self, path, index, ax, legend_name):
        df = pd.read_hdf(path+'/cloud.h5',key='cloud')
        x = df['t'] * 2
        y = abs(df['wz']) / 2
        ax.plot(x, y, label = legend_name[index], linestyle = self.line_style[index][1])
        return 
    def plot_w_time_series(self, label_name = 'Re'):
        # Plot the angular velocity of the ellipse over time   
        fig, ax = plt.subplots(figsize=(6, 5))
        for i in range(len(self.sub_path)):
            print(self.sub_path[i])
            df = pd.read_hdf(self.sub_path[i]+'/cloud.h5',key='cloud')
            x = df['t'] * 2
            y = abs(df['wz']) / 2
            # without line styles
            #ax.plot(x, y, label = "%s = %.1f"% (label_name,self.legend_name[i]))   
            # with line styles
            ax.plot(x, y, label = "%s = %.1f"% (label_name,self.legend_name[i]), linestyle = self.line_style[i][1])
        plt.rcParams["font.family"] = "Times New Roman"  
        #adds a title and axes labels
        ax.set_xlabel('GT')
        ax.set_ylabel(r'$\frac{\omega}{G}$')
        #removing top and right borders
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 400)
        # ticks control
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        #adds legend
        #ax.legend(loc = 'lower right', fontsize = 12)
        ax.legend(loc = 'best', fontsize = 12)
        # set font 
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                  ax.get_xticklabels() + ax.get_yticklabels()):
          item.set_fontsize(12)
        # Adds a text 
        #ax.text(7.5, 0.9, r'$\omega_{ss}=1.00$', fontsize=12, bbox={'facecolor': 'white','alpha': 0.5, 'pad': 8})
        plt.show()
        return 
    def k_effect(self):
       # Plot the angular velocity of the ellipse over time   
        legend_name = ['k=0.2, AR=0.5','k=0.33, AR=0.5','k=0.4, AR=0.5']
        fig, ax = plt.subplots(figsize=(6, 5))
        
        path = 'D:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_confinement/case_rhos1.0_AR0.50_Re7.0_k0.20'
        self.readData(path)
        self.plot_w_t(path, 0, ax, legend_name)
        
        path = 'D:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_confinement/case_rhos1.0_AR0.50_Re7.0_k0.33'
        self.readData(path)
        self.plot_w_t(path, 1, ax, legend_name)
        
        path = 'D:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_confinement/case_rhos1.0_AR0.50_Re7.0_k0.40'
        self.readData(path)
        self.plot_w_t(path, 2, ax, legend_name)
        
        plt.rcParams["font.family"] = "Times New Roman"  
        ax.set_xlabel('GT')
        ax.set_ylabel(r'$\frac{\omega}{G}$')
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 200)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        #ax.legend(loc = 'lower right', fontsize = 12)
        ax.legend(loc = 'best', fontsize = 12)
        # set font 
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                  ax.get_xticklabels() + ax.get_yticklabels()):
          item.set_fontsize(12)
        plt.show()

        return 
    def AR_effect(self):
        # Plot the angular velocity of the ellipse over time   
        legend_name = ['k=0.2, AR=0.5','k=0.2, AR=0.65','k=0.2, AR=0.75']
        fig, ax = plt.subplots(figsize=(6, 5))
        
        path = 'I:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_aspectratio/case_rhos1.0_k0.20_AR0.50_Re7.0'
        self.readData(path)
        self.plot_w_t(path, 0, ax, legend_name)
        
        path = 'I:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_aspectratio/case_rhos1.0_k0.20_AR0.65_Re7.0'
        self.readData(path)
        self.plot_w_t(path, 1, ax, legend_name)
        
        path = 'I:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/effect_aspectratio/case_rhos1.0_k0.20_AR0.75_Re7.0'
        self.readData(path)
        self.plot_w_t(path, 2, ax, legend_name)
        
        plt.rcParams["font.family"] = "Times New Roman"  
        #adds a title and axes labels
        ax.set_xlabel('GT')
        ax.set_ylabel(r'$\frac{\omega}{G}$')
        #removing top and right borders
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 200)
        # ticks control
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        #adds legend
        #ax.legend(loc = 'lower right', fontsize = 12)
        ax.legend(loc = 'best', fontsize = 12)
        # set font 
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                  ax.get_xticklabels() + ax.get_yticklabels()):
          item.set_fontsize(12)
        # Adds a text 
        #ax.text(7.5, 0.9, r'$\omega_{ss}=1.00$', fontsize=12, bbox={'facecolor': 'white','alpha': 0.5, 'pad': 8})
        plt.show()
        return 
    def test(self):
        print(self.path)
        return 0
    def last_eulerAngle(self):
        print(self.data['EulerAz'])
        eulerAz = self.data.loc[self.data.index[-1],'EulerAz'] * 180 / np.pi
        print("the angle is: %.2f"%(eulerAz))



if __name__ == '__main__':
    case = multiFiles()
    case.AR_effect()
    #case.plot_w_time_series()
    #case.k_effect()
    #case.last_eulerAngle()
