#!/usr/bin/env python
# coding:utf8
# -*- coding: utf-8 -*-
"""
Module: Read RRTM OUTPUT data 

Created on 2019

@author: Jianyu Zheng
"""

#remove IMMAX

import numpy  as np
import pandas as pd
import fortranformat as ff

def read_output_rrtm_funct(IMMAX, Rs, sza):
    #file = open(fname_sw_cl,'w+')	
    data = np.array(pd.read_table('./rrtm_output/scat_OUTPUT_RRTM_sw_Rs{:}_sza{:}.clear'.format(Rs,sza),header=3,\
            names=['a','b','c','d','e','f','g'], nrows=IMMAX, delim_whitespace=True)).astype(float) 

    # Variables we need for the plot
    TOA_sw_cl_upflux_bb = data[0,2]
    TOA_sw_cl_dwflux_bb = data[0,4]
    TOA_sw_cl_netflux_bb = data[0,5]
    #file = open(fname_sw_ae,'w+')	
    data = np.array(pd.read_table('./rrtm_output/scat_OUTPUT_RRTM_sw_Rs{:}_sza{:}.aerosol'.format(Rs,sza),header=3,\
            names=['a','b','c','d','e','f','g'], nrows=IMMAX, delim_whitespace=True)).astype(float)
    
    # Variables we need for the plot
    TOA_sw_ae_upflux_bb = data[0,2]
    TOA_sw_ae_dwflux_bb = data[0,4]
    TOA_sw_ae_netflux_bb = data[0,5]

    return TOA_sw_ae_netflux_bb, TOA_sw_cl_netflux_bb, TOA_sw_ae_netflux_bb-TOA_sw_cl_netflux_bb
