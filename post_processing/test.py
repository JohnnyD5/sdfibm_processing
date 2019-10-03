# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:03:24 2019

@author: zding5
"""
import re
a = ['a8Re9.0','a7Re10.0','a9Re11.0']
a = 'a8Re9.0'
b= re.findall(r"Re\d*\.\d",a)[0].strip('Re')

print(b)