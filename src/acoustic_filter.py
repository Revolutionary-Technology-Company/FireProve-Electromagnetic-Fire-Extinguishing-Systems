#!/usr/bin/env python3
"""
FireProve Turret System - Real-World Acoustic Signal Filter
Implements a 4th-order Butterworth bandpass filter and spectral subtraction
to isolate 30 Hz - 60 Hz flame combustion signatures from high-ambient noise fields.
"""

import numpy as np
from scipy.signal import butter, lfilter

class AcousticSignalFilter:
    def __init__(self, sample_rate=4000, low_cut=30.0, high_cut=60.0):
        """
        Initializes the processor. A low sample rate (e.g., 4000 Hz) is preferred
        to maximize computational efficiency on the RT Hex silicon for sub-bass signals.
        """
        self.sample_rate = sample_rate
        self.low_cut = low_cut
        self.high_cut = high_cut
        
        # Initialize noise profile memory container for spectral subtraction
        self.ambient_noise_profile = None

    def _butter_bandpass(self):
        """Generates filter coefficients for low-frequency isolation."""
        nyquist = 0.5 * self.sample_rate
        low = self.low_cut / nyquist
        high = self.high_cut / nyquist
        b, a = butter(4, [low, high], btype='band')
        return b, a

    def apply_bandpass_filter(self, raw_audio_data):
        """Stage 1: Strips out high-frequency sirens, voice, and low-end rumble outside the target zone."""
        b, a = self._butter_bandpass()
        filtered_signal = lfilter(b, a, raw_audio_data)
        return filtered_signal

    def calibrate_noise_profile(self, silent_ambient_sample):
        """
        Captures a static snapshot of background machinery or wind noise.
        Should be run when the turret boots up or during safe-state idle phases.
        """
        fft_profile = np.fft.rfft(silent_ambient_sample)
        self.ambient_noise_profile = np.abs(fft_profile)
        print("[*] Acoustic Calibration Complete: Background noise footprint registered.")

    def apply_spectral_subtraction(self, filtered_audio_data, noise_threshold_multiplier=2.0):
        """
        Stage 2: Eliminates steady, continuous in-band background noise (like fans or engine humming).
        Subtracts the calibrated noise spectrum from the live signal.
        """
        if self.ambient_noise_profile is None:
            # Fallback if no calibration data is available yet
            return filtered_audio_data
            
        # Transform the live time-domain signal into the frequency domain
        signal_fft = np.fft.rfft(filtered_audio_data)
        signal_magnitude = np.abs(signal_fft)
        signal_phase = np.angle(signal_fft)
        
        # Execute magnitude subtraction
        subtracted_magnitude = signal_magnitude - (self.ambient_noise_profile * noise_threshold_multiplier)
        
        # Clamp negative values to zero (preventing phase reconstruction errors)
        subtracted_magnitude = np.maximum(subtracted_magnitude, 0)
        
        # Reconstruct the time-domain signal using the original phase angles
        reconstructed_fft = subtracted_magnitude * np.exp(1j * signal_phase)
        cleaned_signal = np.fft.irfft(reconstructed_fft)
        
        return cleaned_signal

    def compute_signal_to_noise_ratio(self, processed_signal, raw_signal):
        """Calculates performance efficiency metrics for telemetry tracking logs."""
        rms_processed = np.sqrt(np.mean(processed_signal**2)) + 1e-12
        rms_raw = np.sqrt(np.mean(raw_signal**2)) + 1e-12
        snr = 20 * np.log10(rms_processed / rms_raw)
        return snr
