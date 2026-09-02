#!/usr/bin/env python3
"""
Univac IX Mainframe - Edwards FireWorks Automated Reporting Interface
Converts live aerial drone telemetry matrices into prioritized CSV payloads
formatted for direct injection into Edwards FireWorks life safety workstations.
"""

import os
import csv
import time

class EdwardsFireworksReporter:
    def __init__(self, target_csv_path="C:/Edwards/FireWorks/Data/live_events.csv"):
        # Target directory path matching the Edwards FireWorks database directory configuration
        self.target_csv_path = target_csv_path
        self._initialize_log_headers()

    def _initialize_log_headers(self):
        """Creates the reporting file structure with correct console viewport headers if missing."""
        dir_name = os.path.dirname(self.target_csv_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        if not os.path.exists(self.target_csv_path):
            with open(self.target_csv_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                # Formatted headers to map directly into FireWorks Event/Device tables
                writer.writerow(["Timestamp", "Node_ID", "Event_Priority", "Latitude", "Longitude", "Heat_Intensity", "Cannon_Status"])
            print(f"[*] FireWorks Link: Initialized secure reporting log at {self.target_csv_path}")

    def format_priority_state(self, heat_intensity, human_lockout_active):
        """
        Maps raw parameters to standard Edwards FireWorks color-coded priorities.
        Returns: 'CRITICAL' (Red), 'ALERT' (Yellow), or 'NOMINAL' (Green).
        """
        if human_lockout_active:
            return "CRITICAL_LOCKOUT" # Prioritizes life safety exceptions
        elif heat_intensity > 100.0:
            return "CRITICAL"         # Active flame breakthrough event
        elif heat_intensity > 0.0:
            return "ALERT"            # Smoldering hot-spot track signature
        return "NOMINAL"

    def transmit_event_to_fireworks(self, drone_id, lat, lon, heat_intensity, cannon_firing, human_lockout):
        """Appends a real-time event status packet to the Edwards Workstation file watcher."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        priority = self.format_priority_state(heat_intensity, human_lockout)
        status_string = "DISCHARGING_ANTI_WAVE" if cannon_firing else "SCANNING_SPECTRUM"

        try:
            with open(self.target_csv_path, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, drone_id, priority, f"{lat:.5f}", f"{lon:.5f}", f"{heat_intensity:.1f}", status_string])
            return True
        except IOError:
            print(f"[!] Error: FireWorks file lock conflict. Workstation buffer may be busy.")
            return False
