#!/usr/bin/env python3
"""
FireProve Turret System - Real-Time Inverse Wave Audio Synthesis Engine
Identifies the dominant combustion frequency (30 Hz - 60 Hz) and generates 
an exact 180-degree phase-inverted anti-wave to drive the titanium compression driver.
"""

import numpy as np

class WaveInversionEngine:
    def __init__(self, sample_rate=4000, buffer_size=512):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Continuous time track vector for smooth wave generation across blocks
        self.time_index = 0.0
        self.dt = 1.0 / self.sample_rate

    def detect_combustion_frequency(self, cleaned_audio_buffer):
        """
        Analyzes the filtered audio buffer using an FFT to isolate 
        the exact peak frequency causing the combustion feedback loop.
        """
        # Apply a Hanning window to prevent spectral leakage at buffer boundaries
        windowed_signal = cleaned_audio_buffer * np.hanning(len(cleaned_audio_buffer))
        
        # Compute real FFT
        fft_data = np.fft.rfft(windowed_signal)
        frequencies = np.fft.rfftfreq(len(cleaned_audio_buffer), d=self.dt)
        magnitudes = np.abs(fft_data)
        
        # Target only the valid 30 Hz to 60 Hz fire suppression band
        valid_indices = np.where((frequencies >= 30.0) & (frequencies <= 60.0))[0]
        
        if len(valid_indices) == 0:
            return 0.0, 0.0  # No valid fire signature detected
            
        # Locate the peak energy bin within the target suppression spectrum
        peak_sub_index = np.argmax(magnitudes[valid_indices])
        peak_index = valid_indices[peak_sub_index]
        
        dominant_freq = frequencies[peak_index]
        peak_magnitude = magnitudes[peak_index]
        
        return dominant_freq, peak_magnitude

    def synthesize_anti_wave(self, frequency, amplitude, target_attenuation_factor=1.2):
        """
        Generates a continuous, phase-flipped anti-wave buffer.
        Applies a 180-degree (pi radian) phase offset directly to the sine generation.
        """
        if frequency < 30.0 or frequency > 60.0:
            return np.zeros(self.buffer_size)  # Output silence if outside fire band
            
        # Construct the time array for this buffer step
        t = np.arange(self.buffer_size) * self.dt + self.time_index
        
        # Phase Inversion Equation: sin(wt + phi + pi) where pi forces the 180° flip
        # Over-driving the amplitude slightly (attenuation factor) helps break flame boundary layers
        driving_amplitude = min(1.0, amplitude * target_attenuation_factor)
        
        # Generate the phase-inverted anti-wave
        inverse_wave = driving_amplitude * np.sin(2 * np.pi * frequency * t + np.pi)
        
        # Advance the global time index to maintain perfect phase alignment across buffer boundaries
        self.time_index += self.buffer_size * self.dt
        
        return inverse_wave

    def map_to_hex_bus_voltages(self, inverse_wave):
        """
        Normalizes the floating-point wave (-1.0 to +1.0) onto the 
        native RT 0.0V - 1.0V multi-state analog hardware bus.
        Centering the wave at 0.5V matches the amplifier bias point.
        """
        # Map range [-1.0, 1.0] -> [0.0, 1.0]
        normalized_voltages = (inverse_wave + 1.0) / 2.0
        
        # Enforce strict 16-state logic levels (clipping to the nearest 0.0625V step)
        hex_stepped_voltages = np.round(normalized_voltages * 15) / 15.0
        
        return hex_stepped_voltages
