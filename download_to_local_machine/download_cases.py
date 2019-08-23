# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:52:44 2019

@author: zding5
"""

import os

os.system('mkdir download')
os.chdir('download')
# only change the list below
rhos_list = [1.003]
k_list = [0.2]
AR_list = [0.5]
Re_list = [7,7.2,7.3,7.4,7.6,7.8,8,8.5]
###
for rhos in rhos_list:
    for k in k_list:
        for AR in AR_list:
            for Re in Re_list:
                casename = "case_rhos%.1f_k%.1f_AR%.1f_Re%.1f"%(rhos,k,AR,Re)
                print("generate case: ", casename)
                os.system('mkdir %s' % casename)
                os.system('cp ../%s/cloud.out %s/.'%(casename, casename))
                os.system('cp -r ../%s/0 %s/.'%(casename, casename))
                os.system('cp -r ../%s/300 %s/.'%(casename, casename))
                os.system('cp -r ../%s/constant %s/.'%(casename, casename))
                os.system('cp -r ../%s/system %s/.'%(casename, casename))
                os.system('cp ../%s/solidDict %s/.'%(casename, casename))
                os.system('cp ../%s/view.foam %s/.'%(casename, casename))
print("Program runs successfully!")
