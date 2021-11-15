import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d
import csv
import random

#ランダムに点を発生させる
nloop_max = 10000
nloop = 0

#==================
#input 
xmin = 0.0
ymin = 0.0
xmax = 5.0
ymax = 10.0
elmsize = 0.1

#output
#ELEMENT.txt
#==================

_x = []
_y = []
_id = []

#ランダムに点を発生させる,ループ回数=nloop_max id=1は対象の点, id=0は要素外点, ここらへんは3Dと同じ
while nloop < nloop_max:
    flag_loop = 0
    a = random.random()
    x = (xmax-xmin)*a
    a = random.random()
    y = (ymax-ymin)*a
    if (nloop == 0):
        _x.append(x)
        _y.append(y)
        _id.append(1)
        nloop += 1
    else:
        for i in range(len(_x)):
            dx = x - _x[i]
            dy = y - _y[i]
            dd = np.sqrt(dx**2+dy**2)
            if (dd < elmsize):
                flag_loop = 1
                break
        if (flag_loop == 1):
            nloop += 1
        else:
            _x.append(x)
            _y.append(y)
            _id.append(1)
            nloop += 1        

#解析対象要素点数 ここまでの_xの数
n_pts_body = len(_x)

#反転
for i in range(n_pts_body):
    r_x = _x[i]-2*(_x[i]-xmin)
    r_y = _y[i]
    dd = np.sqrt((xmin-r_x)**2)
    if(dd < 2*elmsize):
        _x.append(r_x)
        _y.append(r_y)
        _id.append(0)
        continue
for i in range(n_pts_body):
    r_x = _x[i]+2*(xmax-_x[i])
    r_y = _y[i]
    dd = np.sqrt((r_x-xmax)**2)
    if(dd < 2*elmsize):
        _x.append(r_x)
        _y.append(r_y)
        _id.append(0)
        continue
for i in range(n_pts_body):
    r_x = _x[i]
    r_y = _y[i]-2*(_y[i]-ymin)
    dd = np.sqrt((ymin-r_y)**2)
    if(dd < 2*elmsize):
        _x.append(r_x)
        _y.append(r_y)
        _id.append(0)
        continue
for i in range(n_pts_body):
    r_x = _x[i]
    r_y = _y[i]+2*(ymax-_y[i])
    dd = np.sqrt((r_y-ymax)**2)
    if(dd < 2*elmsize):
        _x.append(r_x)
        _y.append(r_y)
        _id.append(0)
        continue

#母点の表示
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
ax.set_aspect('equal')
for i in range(len(_x)):
    if (_id[i]==1):
        plt.scatter(_x[i],_y[i],color="r",s=5)
    else:
        plt.scatter(_x[i],_y[i],color="k",s=5)

plt.show()

#array作成 ボロノイ分割に使う
pts = np.zeros([len(_x),2],dtype=np.float64)
for i in range(len(_x)):
    pts[i][0] = float(_x[i])
    pts[i][1] = float(_y[i])

print("トータル母点数",len(_x))
print("対象母点数",n_pts_body)

#ボロノイ分割
vor = Voronoi(pts)
fig = voronoi_plot_2d(vor,point_size=1,show_vertices=False,show_points=False,line_width=0.8)
plt.subplot().set_aspect("equal")
fig.savefig('voronoi.png')

pre_num_node = len(vor.vertices)
print("カット前ノード数",pre_num_node)

#誤差範囲とりあえず0.01
xmin = 0.0 - 1e-2
ymin = 0.0 - 1e-2
xmax = 5.0 + 1e-2
ymax = 10.0 + 1e-2

#対象範囲外にある点をとりあえず-100にする
num_node = 0
change = np.zeros(pre_num_node,dtype=np.int64)
xnode = np.zeros(num_node)
ynode = np.zeros(num_node)
for i in range(pre_num_node):
    x = vor.vertices[i][0]
    y = vor.vertices[i][1]
    if (x < xmin or x > xmax or y < ymin or y > ymax):
        change[i] = -100
        continue
    else:
        change[i] = num_node
        xnode = np.append(xnode,x)
        ynode = np.append(ynode,y)
        num_node += 1
print("カット後ノード数",num_node)

#自動で生成される無限遠点(-1)を含むリストを削除
region_body = []
for r in range(len(vor.regions)):
    if -1 not in vor.regions[r]:
        region_body.append(vor.regions[r])
if (len(region_body[0])==0):
    del region_body[0]

# print("region_body")  デバック用
# print(region_body)

#要素を構成する点のリストの更新(要素範囲外) maxnodeは面を構成する最大節点数 
maxnode = 0
new_list = [[]]
for i in range(len(region_body)):
    temp_ = []
    flag_add = 0
    for j in region_body[i]:
        if(j>=0):
            temp_.append(change[j])
            if(change[j] == -100):
                flag_add = 0
                break
        else:
            break
        flag_add = 1
    if(flag_add == 1):
        new_list.append(temp_)
        num = len(temp_)
        if(num > maxnode):
            maxnode = num
if (len(new_list[0])==0):
    del new_list[0]

# print("new_list") デバック用
# print(new_list)

#ELEMENT.txt作成
f = open("ELEMENT.txt", 'w', newline = "", encoding = "utf-8_sig")
print("要素数",file=f)
print(n_pts_body,maxnode,file=f)
print("要素番号, X座標, Y座標, 頂点数, 節点番号",file=f)
for i in range(n_pts_body):
    print('{}\t{:6f}\t{:6f}\t{}\t'.format(i,pts[i][0],pts[i][1],len(new_list[i])), end="", file=f)
    for j in range(len(new_list[i])):
        print(new_list[i][j], "\t", end="", file=f)
    print("", file=f)
print("節点数",file=f)
print(num_node,file=f)
print("X座標, Y座標",file=f)
for i in range(num_node):
    print('{}\t{:6f}\t{:6f}'.format(i,xnode[i],ynode[i]), file=f)
f.close()
