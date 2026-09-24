# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 14:58:11 2025

@author: geode
"""
# sources used for this one: https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html?utm_source and https://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python?utm_source and 
#https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html?utm_source and https://numpy.org/doc/stable/reference/routines.fft.html?utm_source and https://dsp.stackexchange.com/questions/52820/fast-fourier-transform-using-numpy?utm_source
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
## load ECG and heart-rate data from .mat files very difficult to find out how
data_ecg = sio.loadmat(r'C:\Users\geode\Downloads\ECG_Data.mat')
data_hr  = sio.loadmat(r'C:\Users\geode\Downloads\HeartRate.mat')
ecg      = data_ecg['ECG'][0, :]   # take out the  ECG time 
hr       = data_hr['HR'][0, :]     # take out the  heart-rate 

# set sampling rate and builds a time over frequency axes
fs = 1000  # samples the frequency in Hz
n = ecg.size  # find the number of samples
timea = np.arange(n) / fs   # makes the time axeses in seconds 
freqa = np.arange(n) * (fs/n) # and frequency axis in hrtz

# calcualtes the  FFT and magnitude spectrum
fft_comp = np.fft.fft(ecg)         # complex frequency of each components is made into dft 
mag_spec  = np.abs(fft_comp)       # magnitude of each frequency 

# plot magnitude spectrum  if tge frequency x and magnitude y 
plt.figure()
plt.stem(freqa, mag_spec, markerfmt=' ', use_line_collection=True)
plt.xlim(0, fs/2)
plt.xlabel('frequency (hz)')
plt.ylabel('magnitude')
plt.title('ecg frequency components')
plt.grid(True)
idx_sorted = np.argsort(mag_spec)[::-1]
top_idx= idx_sorted[:10]


# finds the  top 10  frequency 
idx_sorted = np.argsort(mag_spec)[::-1]  # sort by greatest to smallest 
top_idx    = idx_sorted[:10]            # take the first 10


# build a filtered spectrum keeping only top10 values and their opposits are kept or used
filtered  = np.zeros_like(fft_comp)  
filtered[top_idx] = fft_comp[top_idx]  
mirrors = (n - top_idx) % n             # symmetric positions
filtered[mirrors] = fft_comp[mirrors]  

# reconstruct time domain signal to make a using real values  FFT
reconstructed = np.fft.ifft(filtered).real

# generate teh  RMSE between original and reconstructed signals
fft_rmse = np.sqrt(np.mean((reconstructed - ecg)**2))
# find dominant frequency and make them in to bpm
dominant_hz  = freqa[top_idx[0]]
dominant_bpm = dominant_hz * 60
measured_bpm = hr[0]

# print results of everything basically 
print("Q1c Outputs:")
print(f"FFT-based RMSE (Top 10 freqs): {fft_rmse:}")
print(f"Dominant Frequency: {dominant_hz:} Hz")
print(f"Dominant BPM from FFT: {dominant_bpm:} bpm")
print(f"Measured BPM from HR file: {measured_bpm:} bpm")

# plot the original vs new reconstructed signals
plt.figure()
plt.plot(timea, ecg, 'k',   label='original ecg')
plt.plot(timea, reconstructed, '--r', label='reconstructed top-10 fft')
plt.xlabel('time (s)')
plt.ylabel('ecg signal (mv)')
plt.title('fft reconstruction vs original')
plt.legend(loc='best')
plt.grid(True)
plt.show()
