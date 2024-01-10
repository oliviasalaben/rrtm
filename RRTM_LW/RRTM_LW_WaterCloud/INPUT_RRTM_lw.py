#!/usr/bin/env python
# coding:utf8
# -*- coding: utf-8 -*-
"""
Module: write RRTM longwave inputfile (INPUT_RRTM_lw)

Created on 2019

@author: Jianyu Zheng
"""

import os 
import numpy as np
import fortranformat as ff

def read_input_rrtm_lw(fname, ICLD, ISCAT, NUMANGS, TBOUND, HBOUND, SEMISS, IBMAX, ZM, PM, TM, VMOL):
		
	#RECORD 1.1
	CXID  = '$ user defined profile' #80 characters of user identification
	
	#RECORD 1.2
	IATM  = 1  #  flag for RRTATM    1 = yes
	IXSECT = 0 # no cross-sections included in calculation
	#ISCAT = 2  #  switch for DISORT# =0 DISORT =1 two-stream
	#NUMANGS = 0  # 0: 4 stream 1: 8 streams
	IOUT  =  99 #  # 0  only output is for 820-50000 cm-1.
	#ICLD  = 0  #  flag for cloud =0 no cloud =1 has cloud layer(s)
	
	#RECORD 1.4 #TBOUND,  IEMIS, IREFLECT, (SEMISS(IB),IB=1,16)
	#TBOUND = -1.0
	IEMIS  =  2 # 1 means each band has the same surface emissivity (equal to SEMISS(1))
	IREFLECT = 0 # Lambertian reflection at surface
	#SEMISS   = np.ones(16)*0.95 # the surface emissivity for each band
	
	#RECORD 3.1
	MODEL  = 0  # = 0  user supplied atmospheric profile
	NOPRNT = 0   # = 0  full printout
	NMOL   = 7   # number of molecular species (default = 7)
	IPUNCH = 0   # = 0  layer data not written
	MUNITS = 0   # = 0  write molecular column amounts to TAPE7 (if IPUNCH = 1, default)
	RE     = 0.0 #  radius of earth (km) defaults for RE=0: i.e., no adjusting
	CO2MX  = 380.0 # mixing ratio for CO2 (ppm).
	#REF_LAT = 15.0 #  latitude of location of calculation (degrees)
	
	# RECORD 3.2
	#PM = np.ones(65)
	#ZM = np.ones(65)
	#TM = np.ones(65)
	#PM[0]  = 1013.0
	#PM[-1] = 0.01
	
	#RECORD 3.3B
	#IBMAX = 65
	#PBND  = ZM #PM
	#PBND  = reverse( [ 0.1, 10.0, 100.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 700.0, 800.0, 900.0, 1000.0] )
	#PBND1 = np.arange(0.12,32.52,0.12)
	#PBND2 = np.arange(33,48,3)
	#PBND3 = np.arange(45,70,5)
	#PBND  = np.concatenate((PBND1,PBND2,PBND3),axis=0)
	if ZM[0]<0.1:
		ZBND = ZM+0.001
	else:
		ZBND = ZM+0.01
	#force the first pressure level to be 1013.0
	#HBOUND  = 0.120 #min(ZM) #max(PM) # surface pressure (mb)
	HTOA    = 77.  #max(ZM) #min(PM) # TOA pressure (mb)
	
	#  RECORD 3.4
	IMMAX = IBMAX
	HMOD  = ''#'atmospheric profiles'
	
	#
	# ZM = make_array(IMMAX,/float)# boundary altitude (km)
	# PM = make_array(IMMAX,/float)# boundary pressure (mb)
	# TM = make_array(IMMAX,/float)# boundary temperature (K)
	JCHARP = 'A' # indicate that the PM is in the unit of mb
	JCHART = 'A' # indicate that the TM is in the unit of Kelvin
	JCHAR_H20  = 'C'
	JCHAR_CO2  = 'A'
	#JCHAR_O3   = '1'
	JCHAR_O3   = 'C'
	JCHAR_others  ='1111' #1st char for H2O unit: mass mixing ratio (gm/kg)
	                   #2nd char for CO2 unit: volume mixing ratio (ppmv)
	                   #3rd char for O3  unit: mass mixing ratio (gm/kg)
	                   #1111 indicate that N2O, CO CH4 and O2 uses default values (1: tropical 2 MLS# 3:MLW 4:Subaractic summer# 5: Subaractic winter# 6: US standard)
	
	#(M):  AVAILABLE       ( 1)  H2O  ( 2)  CO2  ( 3)    O3 ( 4)   N2O ( 5)    CO ( 6)   CH4 ( 7)    O2
	# MOLECULAR SPECIES     ( 8)   NO  ( 9)  SO2  (10)   NO2 (11)   NH3 (12)  HNO3 (13)    OH (14)    HF
	#                       (15)  HCL  (16)  HBR  (17)    HI (18)   CLO (19)   OCS (20)  H2CO (21)  HOCL
	#                       (22)   N2  (23)  HCN  (24) CH3CL (25)  H2O2 (26)  C2H2 (27)  C2H6 (28)   PH3
	#                       (29) COF2  (30)  SF6  (31)   H2S (32) HCOOH (33) EMPTY (34) EMPTY (35) EMPTY
	# JCHAR = 1-6           - default to value for specified model atmosphere
	#              = " ",A         - volume mixing ratio (ppmv)
	#              = B             - number density (cm-3)
	#              = C             - mass mixing ratio (gm/kg)
	#              = D             - mass density (gm m-3)
	#              = E             - partial pressure (mb)
	#              = F             - dew point temp (K) *H2O only*
	#              = G             - dew point temp (C) *H2O only*
	#              = H             - relative humidity (percent) *H2O only*
	#              = I             - available for user definition
	
	#VMOL = np.zeros([IMMAX,3])
	
	# write the INPUT_RRTM file
	file = open(fname,'w+')
	form = ff.FortranRecordWriter('(A80)')
	file.writelines(form.write([CXID]))

	form = ff.FortranRecordWriter('(A1)')
	file.writelines('\n'+form.write('$'))
	
	
	form = ff.FortranRecordWriter('(I50, I20, I13, I2, I5, I5)')
	file.writelines('\n'+form.write([IATM, IXSECT, ISCAT, NUMANGS, IOUT, ICLD]))
	
	form = ff.FortranRecordWriter('(E10.3, I2, I3, 16F5.3)')
	if np.size(SEMISS) == 1:
		file.writelines('\n'+form.write([TBOUND, IEMIS, IREFLECT, SEMISS]))
	else:
		file.writelines('\n'+form.write([TBOUND, IEMIS, IREFLECT, *SEMISS]))
	
	#these records applicable if RRTATM selected (IATM=1)
	form = ff.FortranRecordWriter('(I5, I10, I10, I5, I5, I5, F10.3)')
	file.writelines('\n'+form.write([MODEL, IBMAX, NOPRNT, NMOL, IPUNCH, MUNITS, RE]))
	
	form = ff.FortranRecordWriter('(F10.3,  F10.3)')
	file.writelines('\n'+form.write([HBOUND, HTOA]))
	
	form = ff.FortranRecordWriter('(8F10.3)')
	file.writelines('\n'+form.write([*ZBND]))
	
	form = ff.FortranRecordWriter('(I5, 3A8)')
	file.writelines('\n'+form.write([IMMAX, HMOD]))
	
	for ily in range(IMMAX):
		form = ff.FortranRecordWriter('(E10.3, E10.3, E10.3, A6, A1, A4, 2A1, A4)')
		file.writelines('\n'+form.write\
					   ([ZM[ily], PM[ily], TM[ily], JCHARP, JCHART, \
					   	JCHAR_H20, JCHAR_CO2, JCHAR_O3, JCHAR_others]))
	
		form = ff.FortranRecordWriter('(8E10.3)')
		file.writelines('\n'+form.write([*VMOL[:,ily]]))
	
	file.write('\n%') # end of RRTM namelist
	file.close()
	
	
