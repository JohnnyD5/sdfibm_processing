# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from matplotlib.ticker import AutoMinorLocator
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class oneFile():
    def __init__(self, path = None):
        if len(path) < 1:
            path = 'D:/work/LidDrivenCavity/ellipse_in_shear/c_Re/c_Re300/case_rhos1.0_k0.20_AR0.50_Re7.0'
        self.path = path 
        self.GT_data = pd.read_csv('GT_data.csv', delimiter = ',', skiprows = 1, names=["k","AR","Re", "GT"])
        self.val_data = pd.read_csv('val.csv', delimiter = ',', skiprows = 1, names=["k","AR","Re", "GT"])
        self.map_data = pd.read_csv('mapping.csv', delimiter = ',', skiprows = 1, names=["k","AR","Re_c"])
    def filter(self):
        self.k0d2 = self.GT_data['k']==0.2
        self.k0d33 = self.GT_data['k']==0.33
        self.k0d4 = self.GT_data['k']==0.4
        self.AR0d25 = self.GT_data['AR']==0.25
        self.AR0d33 = self.GT_data['AR']==0.33
        self.AR0d5 = self.GT_data['AR']==0.5
        self.AR0d65 = self.GT_data['AR']==0.65
        self.AR0d75 = self.GT_data['AR']==0.75
        
        self.valk0d2 = self.val_data['k']==0.2
        self.valk0d31 = self.val_data['k']==0.33
        self.valk0d33 = self.val_data['k']==0.33
        self.valk0d41 = self.val_data['k']==0.41
        self.valk0d42 = self.val_data['k']==0.42
        self.valAR0d33 = self.val_data['AR']==0.33
        self.valAR0d5 = self.val_data['AR']==0.5
        self.valAR0d52 = self.val_data['AR']==0.52
        self.valAR0d75 = self.val_data['AR']==0.75
        
        self.mapk0d2 = self.map_data['k']==0.2
        self.mapk0d33 = self.map_data['k']==0.33
        self.mapk0d4 = self.map_data['k']==0.4
    
    
    def readData(self):
        pdf=pd.read_csv(self.path+ '/cloud.out', delimiter = ' ', names = ["t", "x", "y", "z",
                       "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
                       "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
        pdf.sort_values('t', inplace=True)
        pdf.to_hdf(self.path + '/cloud.h5',key='cloud')
        self.data = pd.read_hdf(self.path + '/cloud.h5', key='cloud')
        self.data['v_mag'] = (self.data['vx']**2 + self.data['vy']**2)**0.5

    def plot_w_time_series(self, t = None, y = None):
        # Plot the angular velocity of the ellipse over time
        if t is None:
            GT = self.data['t'] * 2
        if y is None:
            y = abs(self.data['wz']) / 2
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(GT, y)
        ax.set_xlabel('GT')
        ax.set_ylabel(r'$\frac{\omega}{G}$')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        #removing top and right borders
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 300)
        plt.show()
        return
    def force_plot(self):
        GT = self.data['t'] * 2
        fig, axs = plt.subplots(1,2,figsize=(7, 4)) #figsize=(4, 4)
        plt.subplots_adjust(wspace = 0.3)
#        y = self.data['fx'].values    # this will turn a column of dataframe to numpy
#        print(type(y))
        print(self.data['fx'])
        axs[0].plot(GT, self.data['fx']/(1/2*0.1))
        axs[1].plot(GT, self.data['fy']/(1/2*0.1))
        #ax.plot(x, ft, 'b>-.')
        axs[0].set_ylabel(r'$C_D$')
        axs[1].set_ylabel(r'$C_L$')
        #axs[0].set_ylim(bottom=1)
        #axs[1].set_ylim(bottom=0.001)
        for ax in axs:
            #adds a title and axes labels
            ax.set_xlabel('GT')
            #ax.set_yscale('log')
            # set x limit and y limit
            #ax.set_ylim(top = 1e-4, bottom = 1e-6)
            ax.ticklabel_format(style='sci',scilimits=(-3,4),axis='y')
            #adds legend
            #ax.legend(['Drag Coefficient', 'Lift Coefficient'], fontsize = 12)
            # set font 
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(12)
        plt.rcParams["font.family"] = "Times New Roman" 
        plt.show()
    def plot_EulerA_stationary(self):
        # Plot the angular velocity of the ellipse over time
        theta = [20.28, 24.68, 27.28, 29.65, 30.29, 30.92, 31.32, 31.68, 31.98, 32.24]
        Re = [10,15,20,30, 35, 40, 45, 50, 55, 60]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(Re, theta, marker='o')
        ax.set_xlabel('Re')
        ax.set_ylabel(r'$\theta$')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        #removing top and right borders
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        # set x limit and y limit
        #ax.set_xlim(left = 0, right = 300)
        plt.show()
        return
    def val(self):
        self.filter()
        fig, ax = plt.subplots(figsize=(7, 5))
        
        ax.scatter(self.GT_data[self.k0d33 & self.AR0d5]['Re']
        , self.GT_data[self.k0d33 & self.AR0d5]['GT'],label = "k=0.33, AR=0.5")
        ax.scatter(self.val_data[self.valk0d33 & self.valAR0d5]['Re']
        , self.val_data[self.valk0d33 & self.valAR0d5]['GT'],label = "Zettner, k=0.33, AR=0.5", facecolors='none', edgecolors='C0')
        
        ax.scatter(self.GT_data[self.k0d4 & self.AR0d5]['Re']
        , self.GT_data[self.k0d4 & self.AR0d5]['GT'],label = "k=0.4, AR=0.5", marker='s')
        ax.scatter(self.val_data[self.valk0d42 & self.valAR0d52]['Re']
        , self.val_data[self.valk0d42 & self.valAR0d52]['GT'],label = "Zettner, k=0.42, AR=0.52", marker='s', facecolors='none', edgecolors='C1')
        
        ax.scatter(self.GT_data[self.k0d2 & self.AR0d5]['Re']
        , self.GT_data[self.k0d2 & self.AR0d5]['GT'],label = "k=0.2, AR=0.5", marker='^')
        ax.scatter(self.val_data[self.valk0d2 & self.valAR0d5]['Re']
        , self.val_data[self.valk0d2 & self.valAR0d5]['GT'],label = "Ding, k=0.2, AR=0.5", marker='^', facecolors='none', edgecolors='C2')
        
        ax.legend()
        ax.set_xlabel('Re')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(direction = 'in', which = 'both')
        plt.rcParams.update({'font.size': 12})
        plt.rcParams["font.family"] = "Times New Roman"
        plt.show()
        return
    def mapping(self):
        fig = plt.figure(figsize=(6, 4))
        self.filter()
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(self.map_data[self.mapk0d2]['AR']
        , self.map_data[self.mapk0d2]['Re_c'],label = "k = 0.2")
        ax.scatter(self.map_data[self.mapk0d33]['AR']
        , self.map_data[self.mapk0d33]['Re_c'],label = "k = 0.33", marker='^')
        ax.scatter(self.map_data[self.mapk0d4]['AR']
        , self.map_data[self.mapk0d4]['Re_c'],label = "k = 0.4", marker='<')


        ax.legend()
        ax.set_xlabel('AR')
        ax.set_ylabel('Re_c')
        ax.set_xlim(left = 0.2, right = 0.8)
        plt.rcParams.update({'font.size': 12})
        ax.tick_params(direction = 'in', which = 'both')
        plt.rcParams["font.family"] = "Times New Roman"
        plt.show()
        return
    
    def GT_effect_of_k(self):
        self.filter()
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6, 5), sharey=True, gridspec_kw={'wspace': 0})
        axes[0].scatter(self.GT_data[self.k0d2 & self.AR0d5]['Re']
        , self.GT_data[self.k0d2 & self.AR0d5]['GT'],label = "k=0.2, AR=0.5")
        axes[0].scatter(self.GT_data[self.k0d33 & self.AR0d5]['Re']
        , self.GT_data[self.k0d33 & self.AR0d5]['GT'], label = "k=0.33, AR=0.5", marker='s')
        axes[0].scatter(self.GT_data[self.k0d4 & self.AR0d5]['Re']
        , self.GT_data[self.k0d4 & self.AR0d5]['GT'], label = "k=0.4, AR=0.5", marker='^')
        axes[1].scatter(self.GT_data[self.k0d2 & self.AR0d65]['Re']
        , self.GT_data[self.k0d2 & self.AR0d65]['GT'],label = "k=0.2, AR=0.65", facecolors='none', edgecolors='C0')
        axes[1].scatter(self.GT_data[self.k0d33 & self.AR0d65]['Re']
        , self.GT_data[self.k0d33 & self.AR0d65]['GT'], label = "k=0.33, AR=0.65", marker='s', facecolors='none', edgecolors='C1')
        axes[1].scatter(self.GT_data[self.k0d4 & self.AR0d65]['Re']
        , self.GT_data[self.k0d4 & self.AR0d65]['GT'], label = "k=0.4, AR=0.65", marker='^', facecolors='none', edgecolors='C2')
        axes[0].set_ylabel('GT')
        for ax in axes:
            ax.legend()
            ax.set_xlabel('Re')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            ax.tick_params(direction = 'in', which = 'both')
        plt.rcParams.update({'font.size': 12})
        plt.rcParams["font.family"] = "Times New Roman"
        plt.show()
        return
    def GT_effect_of_AR(self):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 6), sharex=True, gridspec_kw={'hspace': 0})
        axes[0].scatter(self.GT_data[self.k0d2 & self.AR0d33]['Re']
        , self.GT_data[self.k0d2 & self.AR0d33]['GT'], label = "k=0.2, AR=0.33")
        axes[0].scatter(self.GT_data[self.k0d2 & self.AR0d5]['Re']
        , self.GT_data[self.k0d2 & self.AR0d5]['GT'], label = "k=0.2, AR=0.5", marker='s')
        axes[0].scatter(self.GT_data[self.k0d2 & self.AR0d65]['Re']
        , self.GT_data[self.k0d2 & self.AR0d65]['GT'],label = "k=0.2, AR=0.65", marker = '^')
        axes[0].scatter(self.GT_data[self.k0d2 & self.AR0d75]['Re']
        , self.GT_data[self.k0d2 & self.AR0d75]['GT'], label = "k=0.2, AR=0.75", marker='D')
        
        axes[1].scatter(self.GT_data[self.k0d4 & self.AR0d33]['Re']
        , self.GT_data[self.k0d4 & self.AR0d33]['GT'], label = "k=0.4, AR=0.33", facecolors='none', edgecolors='C0')
        axes[1].scatter(self.GT_data[self.k0d4 & self.AR0d5]['Re']
        , self.GT_data[self.k0d4 & self.AR0d5]['GT'], label = "k=0.4, AR=0.5", marker='s', facecolors='none', edgecolors='C1')
        axes[1].scatter(self.GT_data[self.k0d4 & self.AR0d65]['Re']
        , self.GT_data[self.k0d4 & self.AR0d65]['GT'],label = "k=0.4, AR=0.65", marker = '^', facecolors='none', edgecolors='C2')
        axes[1].scatter(self.GT_data[self.k0d4 & self.AR0d75]['Re']
        , self.GT_data[self.k0d4 & self.AR0d75]['GT'], label = "k=0.4, AR=0.75", marker='D', facecolors='none', edgecolors='C3')

        for ax in axes:
            ax.legend()
            ax.set_ylabel('GT')
            ax.set_xlabel('Re')
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            ax.tick_params(direction = 'in', which = 'both')
        plt.show()
        return
    def test(self):
        print(self.GT_data)
        return 0
    def last_eulerAngle(self):
        print(self.data['EulerAz'])
        eulerAz = self.data.loc[self.data.index[-1],'EulerAz'] * 180 / np.pi +180
        print("the angle is: %.2f"%(eulerAz))
        
    def dimensionless_period(self):
        peaks, _ = scipy.signal.find_peaks(abs(self.data['wz']),height=1.0)
        GT = self.data.iloc[peaks[-1]]['t']-self.data.iloc[peaks[-2]]['t']
        GT *= 2
        print("GT is: %.2f"%(GT))



if __name__ == '__main__':
    #path = [] # Remember to turn this line off when drawing w-t figure
    path = input("Please identify the path of desired folder; the folder should contain cloud.out file:\n")
    ### convert windows path to linux path
    path = list(path)
    for i, c in enumerate(path):
        if c == '\\':
            path[i] = '/'
    
    path = ''.join(path)
    ###
    case = oneFile(path)
    #case.val()
    #case.mapping()
    case.readData()
    case.plot_w_time_series()
    #case.force_plot()
    #case.dimensionless_period()
    #case.GT_effect_of_k()
    #case.GT_effect_of_AR()
    #case.test()
    #case.last_eulerAngle()
    #case.plot_EulerA_stationary()
