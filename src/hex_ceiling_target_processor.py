#!/usr/bin/env python3
"""
FireProve Turret System - Hexadecimal CEILING Target Vector Processor
Optimized for inverted, drop-down ceiling mount models. Handles 180-degree physical 
orientation flips for native 16-state analog logic voltage routing (0.0V - 1.0V).
"""

import math

class HexCeilingTargetProcessor:
    def __init__(self, mic_spacing_mm=150.0):
        # Physical distance constant between opposing microphone capsule planes
        self.d = mic_spacing_mm / 1000.0  # Convert to meters
        self.speed_of_sound = 343.0        # m/s at ~20°C
        
        # 16-State Hexadecimal Native Analog Voltage Lookups
        self.HEX_STATES = [i * 0.0625 for i in range(16)] # 0.0V to 0.9375V (1.0V ceiling cap)

    def voltage_to_hex_index(self, voltage):
        """Converts raw voltage to closest native 16-state logic index."""
        clamped = max(0.0, min(1.0, voltage))
        closest_state = min(self.HEX_STATES, key=lambda x: abs(x - clamped))
        return self.HEX_STATES.index(closest_state)

    def hex_index_to_voltage(self, index):
        """Converts internal 16-state index back to a hardware control voltage."""
        clamped_idx = max(0, min(15, int(index)))
        return self.HEX_STATES[clamped_idx]

    def compute_spatial_angles(self, t1, t2, t3, t4):
        """
        Calculates Azimuth and Elevation for an INVERTED ceiling deployment.
        Because the turret hangs upside down, the tracking directions are swapped:
        Mic 1: Down-Left, Mic 2: Down-Right, Mic 3: Up-Left, Mic 4: Up-Right
        """
        # Flips the vertical tracking vector because the assembly is upside down
        delta_t_vert = (t3 + t4) - (t1 + t2)
        
        # Horizontal differential delta vector (Azimuth extraction)
        delta_t_horiz = (t1 + t3) - (t2 + t4)
        
        # Max delay limit = distance between mics / speed of sound
        max_delay = self.d / self.speed_of_sound
        
        # Normalize and clamp time delays to prevent arcsin domain violations
        norm_v = max(-1.0, min(1.0, (delta_t_vert * self.speed_of_sound) / self.d))
        norm_h = max(-1.0, min(1.0, (delta_t_horiz * self.speed_of_sound) / self.d))
        
        elevation_rad = math.asin(norm_v)
        azimuth_rad = math.asin(norm_h)
        
        return math.degrees(azimuth_rad), math.degrees(elevation_rad)

    def calculate_motor_voltages(self, az_error, el_error):
        """
        Maps inverted ceiling angular tracking errors directly to 0-1V motor control rails.
        0.5V state = Zero angular velocity (perfect tracking match lock).
        """
        # Map proportional error windows into a 0.0V - 1.0V voltage span
        # Max velocity drive cap arbitrarily set to a 15-degree offset window
        k_p = 1.0 / 30.0 
        
        v_az = 0.5 + (az_error * k_p)
        v_el = 0.5 + (el_error * k_p)
        
        # Force boundaries strictly to native 16-state analog logic targets
        final_v_az = self.hex_index_to_voltage(self.voltage_to_hex_index(v_az))
        final_v_el = self.hex_index_to_voltage(self.voltage_to_hex_index(v_el))
        
        return final_v_az, final_v_el
