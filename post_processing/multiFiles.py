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
        if len(path) < 1:
            path = 'E:/work/LidDrivenCavity/with_shashank/c_Re/first_batch'
        self.path = path + '/'
        self.sub_path = np.array([])
        self.legend_name = []
        self.line_style = [
                     ('solid',                (0, (1, 0))),
                     ('dotted',                (0, (1, 1))),
                
                     ('dashed',                (0, (5, 5))),
                     ('densely dashed',        (0, (5, 1))),
                
                     ('dashdotted',            (0, (3, 5, 1, 5))),
                     ('densely dashdotted',    (0, (3, 1, 1, 1))),
                
                     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5)))]

    def readData(self, starts_chars):
        # starts_chars is the starting characters of the sub folder's name, ex. case_m15
        for entry in os.scandir(self.path):
            if entry.path.startswith(self.path+starts_chars):
                self.sub_path = np.append(self.sub_path, entry.path)
        self.sub_path = sorted(self.sub_path, key = lambda x:float(''.join(re.findall(r"Re\d*\.\d*",x)[0].strip('Re'))))
        
        for i in range(len(self.sub_path)):
            value = float(''.join(re.findall(r"Re\d*\.\d*",self.sub_path[i])[0].strip('Re')))
            self.legend_name = np.append(self.legend_name,value)
        print("Selected folders are:\n", self.sub_path)
        decision = input("Do you want to override old cloud.h5 file? (y/n), say y only when changes are made to the source code, or just hit enter not to override.\n")
        yes_list = ['y', 'yes', 'Y', 'YES']
        if decision in yes_list:
            print("Overriding and assembling data...")
            for i in range(len(self.sub_path)):
                pdf=pd.read_csv(self.sub_path[i]+'/cloud.out', delimiter = ' ', names = ["t", "x", "y", "z",
                   "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
                   "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
                pdf['v_mag'] = (pdf['vx']**2 + pdf['vy']**2)**0.5
                pdf.sort_values('t', inplace=True)
                pdf.to_hdf(self.sub_path[i] + '/cloud.h5',key='cloud')
            print("Data is ready.")
        else:
            print("Overriding not selected and assembling data...")
            for i in range(len(self.sub_path)):
                if os.path.isfile(self.sub_path[i]+'/cloud.h5'):
                    continue
                else:
                    pdf=pd.read_csv(self.sub_path[i]+'/cloud.out', delimiter = ' ', names = ["t", "x", "y", "z",
                       "vx", "vy", "vz", "fx", "fy", "fz", "EulerAx", "EulerAy",
                       "EulerAz", "wx", "wy", "wz", "Tx", "Ty", "Tz"])
                    pdf['v_mag'] = (pdf['vx']**2 + pdf['vy']**2)**0.5
                    pdf.sort_values('t', inplace=True)
                    pdf.to_hdf(self.sub_path[i] + '/cloud.h5',key='cloud')
            print("Data is ready.")
    def plot_w_time_series(self, label_name = 'Re'):
        # Plot the angular velocity of the ellipse over time    
        fig, ax = plt.subplots(figsize=(6, 5))
        for i in range(len(self.sub_path)):
            print(self.sub_path[i])
            df = pd.read_hdf(self.sub_path[i]+'/cloud.h5',key='cloud')
            x = df['t']
            y = abs(df['wz'])
            #ax.plot(x, y, label = "%s = %.1f"% (labelName,legendN[i]),color = colors[i])
            ax.plot(x, y, label = "%s = %.1f"% (label_name,self.legend_name[i]), linestyle = self.line_style[i][1])
        plt.rcParams["font.family"] = "Times New Roman"  
        #adds a title and axes labels
        ax.set_xlabel('t')
        ax.set_ylabel(r'$\hat{\omega}$')
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
        ax.legend(loc = 'lower right', fontsize = 12)
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
    path = input("Please identify the path of desired folder; the folder should contain cloud.out file:\n")
    ### convert windows path to linux path
    path = list(path)
    for i, c in enumerate(path):
        if c == '\\':
            path[i] = '/'
    path = ''.join(path)
    ###
    case = multiFiles(path)
    case.readData('case_m15')
    case.test()
    case.plot_w_time_series()
    #case.last_eulerAngle()
