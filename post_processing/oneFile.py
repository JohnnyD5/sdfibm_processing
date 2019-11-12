# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class oneFile():
    def __init__(self, path = None):
        if len(path) < 1:
            path = 'E:/work/LidDrivenCavity/ellipse_in_shear/c_Re/first_batch/case_m15_rhos1.0_k0.2_AR0.5_Re7.0'
        self.path = path + '/cloud.out'
        pdf=pd.read_csv(self.path, delimiter = ' ', names = ["t", "x", "y", "z",
                       "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
                       "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
        pdf.sort_values('t', inplace=True)
        pdf.to_hdf(path + '/cloud.h5',key='cloud')
        self.data = pd.read_hdf(path + '/cloud.h5', key='cloud')
        self.data['v_mag'] = (self.data['vx']**2 + self.data['vy']**2)**0.5

    def plot_w_time_series(self, t = None, y = None):
        # Plot the angular velocity of the ellipse over time
        if t is None:
            t = self.data['t']
        if y is None:
            y = abs(self.data['wz'])
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(t, y)
        ax.set_xlabel('t')
        ax.set_ylabel(r'$\hat{\omega}$')
        #removing top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # set x limit and y limit
        ax.set_xlim(left = 0, right = 300)
        plt.show()
        return

    def test(self):
        print(self.data['fy'])
        return 0
    def last_eulerAngle(self):
        print(self.data['EulerAz'])
        eulerAz = self.data.loc[self.data.index[-1],'EulerAz'] * 180 / np.pi
        print("the angle is: %.2f"%(eulerAz))

    def dimensionless_period(self):
        peaks, _ = scipy.signal.find_peaks(abs(self.data['wz']),height=1.0)
        GT = self.data.iloc[peaks[-1]]['t']-self.data.iloc[peaks[-2]]['t']
        GT *= 2
        print("GT is: %.2f"%(GT))



if __name__ == '__main__':
    path = input("Please identify the path of desired folder; the folder should contain cloud.out file:\n")
    ### convert windows path to linux path
    path = list(path)
    for i, c in enumerate(path):
        if c == '\\':
            path[i] = '/'
    path = ''.join(path)
    ###
    case = oneFile(path)
    case.plot_w_time_series()
    case.dimensionless_period()
    #case.test()
    #case.last_eulerAngle()
