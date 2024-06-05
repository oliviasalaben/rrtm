#!/usr/bin/env python
# coding:utf8
# -*- coding: utf-8 -*-
"""
Main Program: Run RRTM by using c3m data 

Created on 2019

@author: Jianyu Zheng
"""

import os 
import numpy as np
import pandas as pd

from read_c3m_data import *
from read_c3m_data import *
from INPUT_RRTM_sw import *
from INPUT_RRTM_lw import *
from INPUT_CLD_RRTM_sw import *
from INPUT_CLD_RRTM_lw import *
from INPUT_AER_RRTM_sw import *
from read_output_rrtm  import *

p_min=8   #starting point(the number of starting profile(included)) ( based on this code , p_min need to be consistent with head)
Nprof=4 #ending point(the number of ending profile(excluded)) 

Num_profs = 608

# txt file directory
file_dir  = '/home/jzheng3/zzbatmos_user/Python_codes/rrtm_py/c3m_data/'
model_dir = '/umbc/xfs1/zzbatmos/common/Codes/'
RT_model_lw = model_dir+'rrtm_lw/rrtm_lw_taki_intel'
RT_model_sw = model_dir+'rrtm_sw/rrtm_sw_taki_intel'

file0 = file_dir + 'lon_lat'
file1 = file_dir + 'sza_c3m'
file2 = file_dir + 'surf_emis_c3m'
file3 = file_dir + 'surf_albo_c3m'
file4 = file_dir + 'ref_lat_c3m'
file5 = file_dir + 'surf_temp_c3m'
file6 = file_dir + 'heig_boun_c3m'

file7 = file_dir + 'heig_prof_c3m'
file8 = file_dir + 'pres_prof_c3m'
file9 = file_dir + 'temp_prof_c3m'
file10 = file_dir + 'vmol_wv_c3m'
file11 = file_dir + 'vmol_o3_c3m'

# files store output
fout_sw_cl=open('sw_flux_clear_rrtm.txt','w')
fout_sw_ae=open('sw_flux_aerosol_rrtm.txt','w')
fout_lw_cl=open('lw_flux_clear_rrtm.txt','w')
fout_lw_ae=open('lw_flux_aerosol_rrtm.txt','w')

#Parameters the model needs
SOLVAR  = 0.0  #(16,29)the solar source function scale factor for each band.
SZA     = np.loadtxt(fname=file1) 
SEMISS  = np.loadtxt(fname=file2)
SUF_ALB = np.loadtxt(fname=file3)
REF_LAT = np.loadtxt(fname=file4)  
TBOUND  = np.loadtxt(fname=file5)    
#HBOUND = np.loadtxt(fname=file6)       #altitude of the surface (km)
HTOA   = 68.0       #altitude of the top of the atmosphere (km)

#Atmospheric profiles the model needs
#ZM    = np.loadtxt(fname=file7)   #boundary altitude (km).
#PM    = np.loadtxt(fname=file8)   #pressure (units and input options set by JCHARP)
#TM    = np.loadtxt(fname=file9)   #temperature (units and input options set by JCHART)
#IMMAX = len(ZM[0])
#IBMAX = IMMAX   #number of atmospheric profile boundaries
#Max_Nprof = len(ZM[:,0])
#VMOL_wv = np.loadtxt(fname=file10)
#VMOL_o3 = np.loadtxt(fname=file11)


#--------------------------------------------------;
ISCAT_lw   = 2  
ISCAT_sw   = 0  
NUMANGS = 0 # 4 streams for lw
ISTRM = 0   # 4 streams for sw
NSTR  = 4   # of streams
#--------------------------------------------------;

#------------------for loop -------------------;

f7,f8,f9 = open(file7,'r'), open(file8,'r'), open(file9,'r')
f10,f11  = open(file10,'r'), open(file11,'r')

for p in range(Nprof):  
	print(' Profile =', p)
	ZM = np.array(list(f7.readline().split())).astype(np.float)
	#print(ZM)
	#if ZM == '':
	#	print('End of file')
	#	break
	#elif (ZM[0] == '#') or (ZM[0] == '\n'):
	#	pass

	PM = np.array(list(f8.readline().split())).astype(np.float)
	#print(PM)
	TM = np.array(list(f9.readline().split())).astype(np.float)
	
	HBOUND = ZM[0]
	#print(HBOUND)
	
	IMMAX = len(PM)
	IBMAX = IMMAX   #number of atmospheric profile boundaries
	
	VMOL_wv = np.array(list(f10.readline().split())).astype(np.float)
	VMOL_o3 = np.array(list(f11.readline().split())).astype(np.float)
	VMOL_co2= np.zeros(IMMAX)* 400e-3 #no CO2 profile in data, add mannually
	#print(VMOL_wv.shape,VMOL_o3.shape,VMOL_co2.shape)
	VMOL_total = np.vstack((VMOL_wv,VMOL_co2,VMOL_o3))#density of the molecule set by JCHAR(K)
	VMOL=1e3*VMOL_total
	
	#---------------- lw flux ------------------------------------
	ICLD = 0
	
	if ICLD == 0:
		print(' Compute clear-sky lw flux w/o cloud')
		read_input_rrtm_lw('INPUT_RRTM', ICLD, ISCAT_lw, NUMANGS, TBOUND[p], HBOUND, \
                           SEMISS[p], IMMAX, ZM, PM, TM, VMOL, REF_LAT[p])
		os.system(RT_model_lw)
		os.system('mv INPUT_RRTM INPUT_RRTM.lw')
		os.system('mv OUTPUT_RRTM OUTPUT_RRTM_lw.clear')
	elif CLD == 1:
		print(' Compute clear-sky lw flux w/ cloud')
		aer_lay   = np.array(list(f12.readline().split())).astype(np.float)
		NLAY      = len(aer_lay)
		pmom_dust = np.array(list(f13.readline().split())).astype(np.float)
		#(16,NLAY)aod for NLAY layers and 16 bands
		aod_lay_band_lw = np.array(list(f14.readline().split())).astype(np.float)
		#(14,NLAY)aod for NLAY layers and 14 bands
		aod_lat_band_sw = np.array(list(f15.readline().split())).astype(np.float)
		#print,'1aer_lay',aer_lay
		read_input_rrtm_lw('INPUT_RRTM', ICLD, ISCAT_lw, NUMANGS, TBOUND[p], HBOUND, \
                           SEMISS[p], IMMAX, ZM, PM, TM, VMOL, REF_LAT[p])
		write_IN_CLD_RRTM_lw('IN_CLD_RRTM', NLAY, aer_lay, aod_lay_band_lw, \
		                      al_dust_lw, NSTR, pmom_dust)
		os.system(RT_model_lw)
		os.system('mv INPUT_RRTM INPUT_RRTM.lw')
		os.system('mv IN_CLD_RRTM IN_CLD_RRTM.lw')
		os.system('mv OUTPUT_RRTM OUTPUT_RRTM_lw.cloudy')
	else: 
		print(' ICLD should be 0 or 1 for RRTM_lw !!')
		sys.exit()
	#---------------sw flux-------------------------------------
	ICLD = 0 
	IAER = 0
	
	if ICLD == 0 and IAER == 0:
		print(' Compute clear-sky sw flux w/o aerososl')
		read_input_rrtm_sw('INPUT_RRTM', IAER, ICLD, ISCAT_sw, ISTRM, SZA[p], 1.0-SUF_ALB[p], \
                           HBOUND, IMMAX, ZM, PM, TM, VMOL, REF_LAT[p])
		os.system(RT_model_sw)
		os.system('mv INPUT_RRTM INPUT_RRTM.sw')
		os.system('mv OUTPUT_RRTM OUTPUT_RRTM_sw.clear')
	elif ICLD == 0 and IAER == 10:
		print(' Compute sw fluxs with aerosol')
		read_input_rrtm_sw('INPUT_RRTM', IAER, ICLD, ISCAT_sw, ISTRM, SZA[p], 1.0-SUF_ALB[p], \
                           HBOUND, IMMAX, ZM, PM, TM, VMOL, REF_LAT[p])
		#print('input aerosol optical depth for 14 bands', aod_lay_band_sw;\
		#       aod;qe_dust_sw[9]*qe_dust_sw)
		#print('input aerosol single-scattering albedo', al_dust_sw)
		#print('input aerosol asymmetry factor', af_dust_sw)                         
		write_IN_AER_RRTM_sw('IN_AER_RRTM',NLAY, aer_lay, aod_lay_band_sw, \
                             al_dust_sw,af_dust_sw)
		os.system(RT_model_sw)
		os.system('mv INPUT_RRTM INPUT_RRTM.sw')
		os.system('mv IN_AER_RRTM IN_AER_RRTM.sw')
		os.system('mv OUTPUT_RRTM OUTPUT_RRTM_sw.aerosol')
		#print('cloud properties',2.0/3.0 * cot_LUT[icot] * cer_LUT[icer], cer_LUT[icer])
		#print('aerosol properties',aer_lay, aod_LUT[0,iaod,itype])
		#write_IN_AER_RRTM('IN_AER_RRTM', aer_lay, 0.01*aod_LUT[*,iaod,itype], asa_LUT[*,itype],aaf_LUT[*,itype])
	else:
		print(' IAER should be 0 or 10 if ICLD is 0 for RRTM_sw !!')
		sys.exit()
	
	#----------------read output of rrtm-------------------------
	print('IMMAX = ',IMMAX)
	TOA_sw_cl_upflux_bb, TOA_sw_cl_dwflux_bb, TOA_sw_ae_upflux_bb, TOA_sw_ae_dwflux_bb, \
	TOA_lw_cl_upflux_bb, TOA_lw_cl_dwflux_bb, TOA_lw_ae_upflux_bb, TOA_lw_ae_dwflux_bb, \
	SUF_lw_cl_upflux_bb, SUF_lw_cl_dwflux_bb, SUF_lw_ae_upflux_bb, SUF_lw_ae_dwflux_bb= \
	read_output_rrtm(fout_sw_cl,fout_sw_ae,fout_lw_cl,fout_lw_ae,IMMAX)

	#----------------plot sw DRE-------------------------
	
	#----------------plot lw DRE-------------------------

	