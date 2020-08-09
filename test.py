#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""==============================================================================
# Project: playground
# Script : test.py
# Author : Peng Jia
# Date   : 2020.08.05
# Email  : pengjia@stu.xjtu.edu.cn
# Description: TODO
=============================================================================="""
# import numpy as np
# import seaborn as sns
# # import
# np.random.seed(555)
# d = np.random.laplace(loc=15, scale=3, size=500)
# print(d[:5])
# sns.distplot(d)
A=[1,2,3]
B=[4,5,6]
C=[7,9]
my=[1,2,3,6,7]
my_dict={}
for i in my:
    if i in A:
        my_dict[i]="A"
    elif i in B:
        my_dict[i] = "B"
    elif i in C:
        my_dict[i] = "C"
print(my_dict)

for i in my_dict:
    print(i,my_dict[i])