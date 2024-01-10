#!/usr/bin/env python
# coding:utf8
# -*- coding: utf-8 -*-
"""
Module: write RRTM longwave cloud inputfile (INPUT_CLD_RRTM_lw)

Created on 2019

@author: Jianyu Zheng (Originally created by Zhibo using IDL, then coverted to Python by Jianyu)
"""

import os 
import numpy as np
import fortranformat as ff

def write_IN_CLD_RRTM_lw(fname, NLAY, LAY, TAUCLD, ALB, NSTR, PMOM):
		
	INFLAG  = 10 #  = 2 calculation of separate ice and liquid cloud optical depths, with
	             #           parameterizations determined by values of ICEFLAG and LIQFLAG.
	ICEFLAG = 3  # = 3 the optical properties are computed by a method based on the parameterization
		    #		of ice clouds due to Q. Fu, J. Clim., 9, 2058 (1996).
	LIQFLAG = 1 #  LIQFLAG = 1 the optical depths (non-gray) due to water clouds are computed by a method
	            #            based on the parameterization of water clouds due to Y.X. Hu and K. Stamnes,
	            #            J. Clim., 6, 728-742 (1993).
	
	##LAY     = np.ones(3)
	##NLAY    = 3
	CLDFRAC = 1.0
	CWP     = 100.0
	FRACICE = 0.7
	EFFSIZEICE = 20.0
	##EFFSIZELIQ =14.0
	TESTCHAR = 'z'
	
	# write the INPUT_CLD_RRTM file
	file = open(fname,'w+')
	
	form = ff.FortranRecordWriter('(I5, I5, I5)')
	file.writelines(form.write([INFLAG, ICEFLAG, LIQFLAG]))

	for j in range(NLAY):
		form = ff.FortranRecordWriter('(A1, I4, F10.5, F10.5, F10.5, 17F10.5)')
		file.writelines('\n'+form.write([TESTCHAR, LAY[j], CLDFRAC, TAUCLD[0,j], ALB[0], *PMOM[0,0:5]]))
		for i in range(1,16):
			form = ff.FortranRecordWriter('(F25.5, F10.5, 16F10.5)')
			file.writelines('\n'+form.write([TAUCLD[i,j], ALB[i], *PMOM[i,0:NSTR+1]]))
	file.write('\n%') # end of RRTM namelist
	file.close()


