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

def drawLineChar(fname, suffix,sid, sname, grade_tag, grade_list):
  fig = plt.figure(0)
  data_radar = 400- np.array(grade_list)
  plt.plot(grade_tag, data_radar, marker='o', mec='r', mfc='w')
  plt.xticks(range(len(grade_tag)), grade_tag, rotation=15, fontproperties=font)
  yticks = [0, 50, 100, 150, 200, 250, 300, 350, 400]
  ylabels = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
  plt.ylim(0,400)
  plt.yticks(yticks, ylabels)
  plt.margins(0)
  plt.subplots_adjust(bottom=0.2)
  #plt.xlabel(u"学期", fontproperties=font) #X轴标签
  plt.title('{}_{}_{}'.format(sid, sname, suffix), fontproperties=font) #标题
  plt.grid()
  plt.savefig(fname)
  plt.close()

def getTag(sheet, colN):
  taglist = ['9月', '10月']
  return taglist

def draw_liner_for(sid, sname, suffix, tag, slist):
    fname = fpath + sid+'_'+sname+'_'+suffix+'.png'
    #print(fname, suffix, sid, sname, tag, slist)
    drawLineChar(fname, suffix, sid, sname, tag, slist)
def main(argv=None):
  workbook = xlrd.open_workbook(xlpath)
  tot_sheet = workbook.sheets()[0]
  rowNum = 37
  cul_tag = ['初三上期中','初三上期末','初三下摸底']
  cul_idx = [9, 12, 2]
  tot_tag = ['初三上摸底','初三上10月','初三上期中','初三上期末','初三下摸底', '初三下4月', '初三下1模', '初三下2模']
  tot_idx = [5, 7, 11, 14, 4, 15, 17, 19]
  five_idx = [6, 8, 10, 13, 3, 16, 18, 20]
  for i in range(2, rowNum):
    sid = tot_sheet.cell_value(i, 0)
    sname = tot_sheet.cell_value(i, 1)
    cul_list = []
    five_list = []
    tot_list = []
    for c in cul_idx:
        cul_list.append(tot_sheet.cell_value(i, c))
    for c in five_idx:
        five_list.append(tot_sheet.cell_value(i, c))
    for c in tot_idx:
        tot_list.append(tot_sheet.cell_value(i, c))
    print('drawing figure for {}...'.format(sname))
    #draw_liner_for(sid, sname, '文化课', cul_tag, cul_list)
    draw_liner_for(sid, sname, '语数外物道', tot_tag, five_list)
    draw_liner_for(sid, sname, '总成绩', tot_tag, tot_list)

if __name__ == "__main__":
    sys.exit(main())
