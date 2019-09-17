# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17

@author: Zhizhong Ding
"""

import os
try:
    os.mkdir('download')
except:
    print("download already existed")
for folder in os.listdir("."):
    if folder.startswith('case'):
        try:
            os.mkdir('download/%s'%(folder))
            print('copying %s'%(folder))
        except:
            print('%s already existed'%(folder))
        os.system('cp ./%s/cloud.out download/%s/.'%(folder, folder))
        os.system('cp -r ./%s/0 download/%s/.'%(folder, folder))
        os.system('cp -r ./%s/250 download/%s/.'%(folder, folder))
        os.system('cp -r ./%s/constant download/%s/.'%(folder, folder))
        os.system('cp -r ./%s/system download/%s/.'%(folder, folder))
        os.system('cp ./%s/solidDict download/%s/.'%(folder, folder))
        os.system('cp ./%s/view.foam download/%s/.'%(folder, folder))
print("Program runs successfully!")
