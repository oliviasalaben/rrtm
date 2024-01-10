Readme file for look-up tables of shape-constrained optical properties of ellipsoidal dust
(Written on Feb 6, 2023)

1. 13 files are sent:
	- shapeint_TAMU_*wavelength*.txt

2. In each of the 13 files, each line was produced by: 
fprintf(fid_save,'%.4f %.4f %.4f %.4f %.6e %.6e %.6e %.6e %.6e\n', wl, d, n, k, Qext, ssa, g, delta, S);

where:
wl is wavelength in micrometers
d is diameter in micrometers
n is real part of refractive index
k is imaginary part 
Qext is extinction efficiency. Note that Qext here is defined as as the extinction per unit projected area of a volume-equivalent sphere (after Kok et al., 2017). We direct interested readers to the paragraph under Eq. (19) in the manuscript (Huang et al., 2023, ACP) for further details.
ssa is single-scattering albedo
g is asymmetry factor
delta is linear depolarization ratio
S is lidar ratio

3. Ranges of wl, d, n, and k:
	- 13 wavelengths are wl = [0.35, 0.55, 0.75, 0.95, 2, 4, 6, 8, 10, 12, 14, 16, 35], (unit in micrometers)
	- 300 diameters are d = [logspace(log10(0.1),log10(20),230),logspace(log10(20.5),log10(70),70)], (unit in micrometers)
	- At shortwave spectrum (wl<=0.95):
		- six real parts are n = [1.45, 1.50, 1.52, 1.53, 1.56, 1.59];
		- eight imaginary parts are k = [5e-4, 1e-3, 2e-3, 3e-3, 4e-3, 5e-3, 6e-3, 1e-2];
	- At longwave spectrum (wl > 0.95):
		- six real parts are n = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6];
		- ten imaginary parts are k = [5e-4, 1e-3, 5e-3, 1e-2, 2e-2, 5e-2, 8e-2, 1e-1, 2e-1, 0.49];

4. Note that there are lines with NaN at large size paramenters. This is because the simulation is out of range of the ellipsoidal dust optics database (i.e., Meng et al., 2010).

5. Contact information for questions:
Yue Huang (hyue3@yahoo.com)
Jasper Kok (jfkok@ucla.edu)

