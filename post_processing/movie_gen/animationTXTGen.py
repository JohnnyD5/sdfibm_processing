# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:19:49 2019

@author: zding5
"""
import numpy as np
fh = open('frameGen.py','w')
fh.write('from paraview.simple import *\n')
fh.write('paraview.simple._DisableFirstRenderCameraReset()\n')

# get active view
fh.write("renderView1 = GetActiveViewOrCreate('RenderView')\n")
fh.write("animationScene1 = GetAnimationScene()\n")
# go to 77 frame in paraview for the code to work in paraview(the frame before frame 78)
t = np.arange(77,181,1)
for i in range(len(t)):
    fh.write("animationScene1.GoToNext()\n")
    fh.write("SaveScreenshot('C:/Users/Zhizhong.Ding/Desktop/figures/%1.f.png', renderView1, ImageResolution=[1563, 576])\n"%t[i])
#for i in range()
fh.close()
