# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:02:50 2019

@author: zding5
"""
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('precision', 6)
pd.set_option('expand_frame_repr', True)

class oneFile():
    def __init__(self, path = None):
        if path is None:
            self.path = 'D:/work/LidDrivenCavity/with_shashank/k_Re/case_k0.20_Re5' + '/cloud.out'
        else:
            self.path = path + '/cloud.out'
        pdf=pd.read_csv(self.path, delimiter = ' ', names = ["t", "x", "y", "z",
                       "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
                       "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
        pdf.to_hdf('cloud.h5',key='cloud')
        self.data = pd.read_hdf('cloud.h5', key='cloud')
        self.data['v_mag'] = (self.data['vx']**2 + self.data['vy']**2)**0.5

    def plot_angularV_over_t(self, t = None, y = None):
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
        self.path = self.path + 'slice_data0'
        print(self.path)
        return 0

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
    case.plot_angularV_over_t()
