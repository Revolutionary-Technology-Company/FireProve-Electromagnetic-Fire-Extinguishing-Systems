#!/usr/bin/env python3
"""
FireProve Multi-Turret Mesh Network - Target Allocation System
Enables peer-to-peer coordination so turrets divide targets and maintain coverage.
"""

class TurretMeshNode:
    def __init__(self, turret_id):
        self.turret_id = turret_id
        self.active_target_coords = None
        self.network_registry = {}  # Stores other turrets' active targets

    def receive_radio_broadcast(self, sender_id, target_coords):
        """Processes incoming radio telemetry from nearby friendly turrets."""
        if target_coords is None:
            # If another turret cleared its target, remove it from the registry
            if sender_id in self.network_registry:
                del self.network_registry[sender_id]
        else:
            # Update the global map with what the other turret is currently fighting
            self.network_registry[sender_id] = target_coords

    def evaluate_new_target(self, detected_fires_list):
        """
        Scans a list of detected fire coordinates. 
        Selects the closest unassigned fire to ensure full area coverage.
        """
        # Find all coordinates currently being suppressed by other nodes
        claimed_targets = list(self.network_registry.values())
        
        for fire in detected_fires_list:
            # Skip if another turret is already suppressing this exact area
            if fire in claimed_targets:
                continue
                
            # Claim the first available unassigned fire zone
            self.active_target_coords = fire
            return fire
            
        # If all fires are claimed but a secondary flare-up is expanding, reinforce closest target
        if detected_fires_list:
            self.active_target_coords = detected_fires_list[0]
            return self.active_target_coords
            
        self.active_target_coords = None
        return None

    def broadcast_status(self):
        """Generates the data payload to transmit over the thick copper radio module."""
        return {
            "id": self.turret_id,
            "target": self.active_target_coords
        }
