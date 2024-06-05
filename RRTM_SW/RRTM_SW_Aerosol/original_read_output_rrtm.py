#!/usr/bin/env python
# coding:utf8
# -*- coding: utf-8 -*-
"""
Module: Read RRTM OUTPUT data 

Created on 2019

@author: Jianyu Zheng
"""

import numpy  as np
import pandas as pd
import fortranformat as ff

def read_output_rrtm(fname_sw_cl, fname_sw_ae, fname_lw_cl, fname_lw_ae, IMMAX):
	#file = open(fname_sw_cl,'w+')	
	data = np.array(pd.read_table("OUTPUT_RRTM_sw.clear",header=5,\
		   names=['a','b','c','d','e','f','g'],nrows=IMMAX,delim_whitespace=True)).astype(np.float)
	form = ff.FortranRecordWriter('(F10.4,F10.4,F10.4,F10.4,F10.4,F10.4)')
	for i in range(IMMAX):
		fname_sw_cl.writelines(form.write([data[i]]) + '\n')
	# Variables we need for the plot
	TOA_sw_cl_upflux_bb = data[0,2]
	TOA_sw_cl_dwflux_bb = data[0,4]

	#file = open(fname_sw_ae,'w+')	
	data = np.array(pd.read_table("OUTPUT_RRTM_sw.aerosol",header=3,\
		   names=['a','b','c','d','e','f','g'],nrows=IMMAX,delim_whitespace=True)).astype(np.float)
	form = ff.FortranRecordWriter('(F10.4,F10.4,F10.4,F10.4,F10.4,F10.4)')
	for i in range(IMMAX):
		fname_sw_ae.writelines(form.write([data[i]]) + '\n')
	# Variables we need for the plot
	TOA_sw_ae_upflux_bb = data[0,2]
	TOA_sw_ae_dwflux_bb = data[0,4]
	
	#file = open(fname_lw_cl,'w+')	
	data = np.array(pd.read_table("OUTPUT_RRTM_lw.clear",header=3,\
		   names=['a','b','c','d','e','f','g'],nrows=IMMAX,delim_whitespace=True)).astype(np.float)
	form = ff.FortranRecordWriter('(F10.4,F10.4,F10.4,F10.4,F10.4,F10.4)')
	for i in range(IMMAX):
		fname_lw_cl.writelines(form.write([data[i]]) + '\n')
	# Variables we need for the plot
	TOA_lw_cl_upflux_bb = data[0,2]
	TOA_lw_cl_dwflux_bb = data[0,3]
	SUF_lw_cl_upflux_bb = data[IMMAX-1,2]
	SUF_lw_cl_dwflux_bb = data[IMMAX-1,3]

	#file = open(fname_lw_ae,'w+')	
	data = np.array(pd.read_table("OUTPUT_RRTM_sw.clear",header=3,\
		   names=['a','b','c','d','e','f','g'],nrows=IMMAX,delim_whitespace=True)).astype(np.float)
	form = ff.FortranRecordWriter('(F10.4,F10.4,F10.4,F10.4,F10.4,F10.4)')
	for i in range(IMMAX):
		fname_lw_ae.writelines(form.write([data[i]]) + '\n')
	# Variables we need for the plot
	TOA_lw_ae_upflux_bb = data[0,2]
	TOA_lw_ae_dwflux_bb = data[0,3]
	SUF_lw_ae_upflux_bb = data[IMMAX-1,2]
	SUF_lw_ae_dwflux_bb = data[IMMAX-1,3]

	return TOA_sw_cl_upflux_bb, TOA_sw_cl_dwflux_bb, TOA_sw_ae_upflux_bb, TOA_sw_ae_dwflux_bb, \
		   TOA_lw_cl_upflux_bb, TOA_lw_cl_dwflux_bb, TOA_lw_ae_upflux_bb, TOA_lw_ae_dwflux_bb, \
		   SUF_lw_cl_upflux_bb, SUF_lw_cl_dwflux_bb, SUF_lw_ae_upflux_bb, SUF_lw_ae_dwflux_bb



