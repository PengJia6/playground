#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""==============================================================================
# Project: playground
# Script : vnodes.py
# Author : Peng Jia
# Date   : 2020.07.15
# Email  : pengjia@stu.xjtu.edu.cn
# Description: Visualize resource of cluster (pbs task system)
=============================================================================="""
import os

qnodes_str = ""
qstatn = os.popen("qnodes")
for line in qstatn:
    qnodes_str = qnodes_str + line
nodes_info = {}
nodes_list = []
for i in qnodes_str.split("\n\n")[:-1]:
    node = i.split("\n")[0]
    nodes_list.append(node)
    total = i.split("np =")[1].split("\n")[0]
    nodes_info[node] = [0, int(total)]
qstatn = os.popen("qstat -n |grep -v mu01")
for job in qstatn:
    lineinfo = job[:-1].lstrip().split("/")
    if len(lineinfo) > 1:
        if lineinfo[0] in nodes_info:
            for cpu in lineinfo[1].split(","):
                if "-" in cpu:
                    start, end = cpu.split("-")
                    nodes_info[lineinfo[0]][0] += (int(end) - int(start) + 1)
                else:
                    nodes_info[lineinfo[0]][0] += 1
total_use = 0
total = 0
#
# for nodes, info in nodes_info.items():
#     print(nodes + ":", str(info[1] - info[0]) + "/" + str(info[1]))
#     total_use+=info[0]
#     total+=info[1]
for node in nodes_list:
    print(node + ":", str(nodes_info[node][1] - nodes_info[node][0]) + "/" + str(nodes_info[node][1]))
    total_use += nodes_info[node][0]
    total += nodes_info[node][1]

print("-------------------------------------------------")
print("total" + ":", str(total - total_use) + "/" + str(total))
