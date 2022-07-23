#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
import xlrd 
import numpy as np
from pylab import *                                 #支持中文
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
xlpath = '/path/to/excel'
fpath = '/path/to/jpg_dir'
font_path = '/path/to/SimHei.ttf'
font = FontProperties(fname=font_path, size=12)
plt.rcParams['figure.figsize'] = (8.0, 4) # 设置figure_size尺寸
plt.rcParams['savefig.dpi'] = 200 #图片像素
plt.rcParams['figure.dpi'] = 200

def drawRodar(fname, suffix, sid, sname, grade_tag, grade_list):
  print('drawRodar for {}_{}'.format(sid, sname))
  print(grade_list)
  fig = plt.figure(0)
  labels = np.array(grade_tag)
  dataLenth = len(labels)
  data_radar = 400- np.array(grade_list)
  angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False) # 分割圆周长
  plt.polar(angles, data_radar, 'b-', linewidth=1) # 做极坐标系
  plt.thetagrids(angles * 180/np.pi, labels, fontproperties=font) # 做标签
  plt.fill(angles, data_radar, facecolor='r', alpha=0.25)# 填充
  plt.ylim(0, 400)
  plt.yticks([])
  plt.title('初三下2模_{}_{}_{}'.format(sid, sname, suffix), fontproperties=font) #标题
  plt.savefig(fname)
  plt.close()

def getTag(sheet, colN):
  taglist = ['语文', '数学', '英语', '物理', '道法', '历史', '化学']
  return taglist

def drawFigure(sid, sname, cme_tag, cme_list, tot_tag, tot_list, sub_tag, sub_list):
    suffix = '各科目雷达'
    fname = fpath + sid+'_'+sname+'_'+suffix+'.png'
    drawRodar(fname, suffix, sid, sname, sub_tag, sub_list)
    '''
    suffix = '语数外趋势'
    fname = fpath + sid+'_'+sname+'_'+suffix+'.png'
    drawLineChar(fname, suffix,sid, sname, cme_tag, cme_list)
    suffix = '总分趋势'
    fname = fpath + sid+'_'+sname+'_'+suffix+'.png'
    drawLineChar(fname, suffix,sid, sname, tot_tag, tot_list)
    '''


def main(argv=None):
  workbook = xlrd.open_workbook(xlpath)
  sub_sheet = workbook.sheets()[0]
  rowNum = sub_sheet.nrows
  sub_tag = ['语文', '数学', '英语', '物理', '道法', '历史', '化学']
  for i in range(3, rowNum):
    sid = sub_sheet.cell_value(i, 0)
    sname = sub_sheet.cell_value(i, 1)
    sub_list = []
    for j in range(0, len(sub_tag)):
        sub_list.append(sub_sheet.cell_value(i, 4 + 3*j))
    suffix = '各科目雷达'
    fname = fpath + sid+'_'+sname+'_'+suffix+'.png'
    #print(fname, sub_list)
    drawRodar(fname, suffix, sid, sname, sub_tag, sub_list)

if __name__ == "__main__":
    sys.exit(main())
