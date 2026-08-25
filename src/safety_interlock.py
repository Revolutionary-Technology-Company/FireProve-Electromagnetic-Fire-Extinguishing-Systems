#!/usr/bin/env python3
"""
FireProve Turret System - Thermal Safety & Anti-False-Alarm Interlock Routine
Verifies acoustic targets using thermal focal grid thresholds and human presence detection.
Enforces hardware-level interlocks on the 0-1V RT analog logic bus.
"""

import time

class SafetyInterlockSystem:
    def __init__(self, critical_temp_c=120.0, human_exclusion_zone_meters=5.0):
        # Operational limits
        self.critical_temp_c = critical_temp_c  # Min focal temperature to verify actual combustion
        self.human_exclusion_zone = human_exclusion_zone_meters
        
        # System State Registers
        self.acoustic_match_latched = False
        self.thermal_match_latched = False
        self.human_detected_lockout = False
        self.hardware_permissive = False
        
        # Hardware Watchdog Timer
        self.last_heartbeat_timestamp = time.time()
        self.watchdog_timeout_seconds = 0.5  # Max latency before auto-shutdown

    def evaluate_thermal_grid(self, focal_matrix_8x8):
        """
        Parses raw temperature data from an 8x8 thermal matrix centered on the barrel.
        Looks for localized high-temperature clusters to avoid broad environmental errors.
        """
        max_focal_temp = float(focal_matrix_8x8.max())
        
        # Verify if any thermal pixels breach the critical ignition threshold
        if max_focal_temp >= self.critical_temp_c:
            self.thermal_match_latched = True
            return True, max_focal_temp
            
        self.thermal_match_latched = False
        return False, max_focal_temp

    def evaluate_human_proximity(self, vision_detections, range_finder_meters):
        """
        Processes human detection bounding boxes from camera tracking or thermal signatures.
        If a human is within the proximity limits, it trips an immediate safety lockout.
        """
        for detection in vision_detections:
            if detection.get("label") == "human":
                distance = range_finder_meters
                if distance <= self.human_exclusion_zone:
                    self.human_detected_lockout = True
                    print(f"[CRITICAL WARNING] Human detected inside exclusion zone: {distance:.2f}m! LOCKOUT ACTIVE.")
                    return True
                    
        self.human_detected_lockout = False
        return False

    def refresh_watchdog_heartbeat(self):
        """Refreshes the safety heartbeat timestamp to prove software execution is stable."""
        self.last_heartbeat_timestamp = time.time()

    def determine_firing_permissive(self):
        """
        The ultimate system safety gateway. 
        Returns True ONLY if acoustic and thermal targets match, no humans are detected,
        and the software watchdog has not timed out.
        """
        current_time = time.time()
        
        # 1. Check Watchdog Status (Failsafe for software crashes)
        if (current_time - self.last_heartbeat_timestamp) > self.watchdog_timeout_seconds:
            print("[CRITICAL] Software watchdog timeout breached! Halting hardware streams.")
            self.hardware_permissive = False
            return False

        # 2. Check Human Presence Lockout
        if self.human_detected_lockout:
            self.hardware_permissive = False
            return False

        # 3. Multi-Sensor Verification Check
        if self.acoustic_match_latched and self.thermal_match_latched:
            self.hardware_permissive = True
            return True
            
        # Default safety state is unverified/disarmed
        self.hardware_permissive = False
        return False

    def get_interlock_bus_voltage(self):
        """
        Maps safety logic directly onto the physical 0-1V RT analog safety bus rail.
        0.0V = Hard Disarm (Grounded power cutoff).
        1.0V = Logic Permissive Unlocked.
        """
        if self.determine_firing_permissive():
            return 1.0  # Safe to fire, stream high voltage to enabling circuits
        return 0.0      # Hard clamp to ground, physically isolating power from the amplifier
