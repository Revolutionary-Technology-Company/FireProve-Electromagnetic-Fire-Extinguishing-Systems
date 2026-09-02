#!/usr/bin/env python3
"""
FireProve H6 Variant - Mission-Locked Flight Safety Controller
Overrides standard Return-to-Home (RTH) procedures to enforce continuous fire suppression 
until the sector heat profile reaches zero, unless home base is compromised.
"""

import time

class MissionLockedFlightController:
    def __init__(self, home_lat=47.313, home_lon=-122.179):
        # Hardcoded geographical anchor coordinates for base station
        self.home_latitude = home_lat
        self.home_longitude = home_lon
        
        # Live Operational Registers
        self.home_base_compromised = False
        self.target_fire_extinguished = False
        self.emergency_alternate_landing_active = False

    def evaluate_home_base_safety(self, home_thermal_sensor_reading, critical_temp_threshold_c=80.0):
        """
        Monitors the physical landing pad platform telemetry.
        If a fire breaks out at home base, it trips the emergency alternate flag.
        """
        if home_thermal_sensor_reading >= critical_temp_threshold_c:
            print("[CRITICAL ALERT] Home base telemetry detects ignition threshold breach!")
            self.home_base_compromised = True
            return True
            
        self.home_base_compromised = False
        return False

    def verify_mission_completion(self, active_sector_heat_intensity):
        """
        Evaluates active fire suppression performance metrics.
        Returns True only when the flame's structural enthalpy is entirely broken.
        """
        if active_sector_heat_intensity <= 0.0:
            print("[Mission] Target fire signature collapsed to zero heat intensity.")
            self.target_fire_extinguished = True
            return True
            
        self.target_fire_extinguished = False
        return False

    def handle_return_to_home_request(self, active_heat_intensity, home_pad_temp, flight_control_instance):
        """
        The critical logic gate managing drone return permissions.
        Enforces your exact operational constraints:
        1. Cannon holds station and fights the fire until the heat signature is gone.
        2. If home base catches fire, it blocks the home path to prevent losing the drone.
        """
        # Step A: Update live state parameters
        self.verify_mission_completion(active_heat_intensity)
        self.evaluate_home_base_safety(home_pad_temp)

        # Rule 1: Fire is still raging in the active sector
        if not self.target_fire_extinguished:
            # Check if home base is simultaneously burning down
            if self.home_base_compromised:
                print("[OVERRIDE] Fire at Home Base AND active sector. Holding orbital containment vector.")
                return "HOLD_ORBITAL_STATION"
                
            print("[BLOCKED] RTH request denied. Fire signature is active. Maintaining acoustic suppression.")
            return "CONTINUE_SUPPRESSION_MISSION"

        # Rule 2: Fire is completely out, but home base has caught fire
        if self.target_fire_extinguished and self.home_base_compromised:
            print("[EMERGENCY OVERRIDE] Sector clear, but Home Base is burning! Diverting to safe alternate coordinates.")
            self.emergency_alternate_landing_active = True
            self.execute_emergency_alternate_divert(flight_control_instance)
            return "DIVERT_TO_ALTERNATE"

        # Rule 3: Fire is out and home base is perfectly safe
        if self.target_fire_extinguished and not self.home_base_compromised:
            print("[PERMISSIVE UNLOCKED] Sector clear, home base safe. Initiating standard hardware RTH loop.")
            flight_control_instance.execute_hardware_return_to_home()
            return "EXECUTING_STANDARD_RTH"

    def execute_emergency_alternate_divert(self, flight_control_instance):
        """Pilots the heavy-lift drone to a pre-defined safe buffer zone away from the burning base."""
        # Calculate a safe offset coordinate location (e.g., 200m away from the burning base station layout)
        alt_lat = self.home_latitude + 0.002
        alt_lon = self.home_longitude + 0.002
        
        print(f"[Divert] Tracking straight-line path to Safe Alternate Coordinates: {alt_lat:.5f}, {alt_lon:.5f}")
        
        # Update flight instance targets to use safe alternate zones instead of the burning home grid
        flight_control_instance.current_lat = alt_lat
        flight_control_instance.current_lon = alt_lon
        print("[Divert] Emergency alternate landing achieved. Cutting motors.")
