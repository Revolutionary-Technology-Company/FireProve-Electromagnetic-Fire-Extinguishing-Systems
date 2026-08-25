// ============================================================================
// FireProve System - Bidirectional (Contra-Helical) Acoustic Resonance Barrel
// Features intersecting left- and right-handed helical internal grooves
// ============================================================================

$fn = 100; // High resolution for complex helical geometry sweeps

// Design Dimensions (mm)
BARREL_INNER_D   = 121.92; // 4.8 inches inner bore
BARREL_OUTER_D   = 150.00; // Reinforced heavy-wall titanium
BARREL_LENGTH    = 400.00; // Segment length for rendering efficiency
GROOVE_DEPTH     = 2.5;    // Depth of acoustic channel tracks
GROOVE_WIDTH     = 6.0;    // Width of tracks
THREADS_PER_TURN = 6;      // Number of parallel groove starts
TWIST_PITCH      = 500;    // Axial distance (mm) for one full 360-degree rotation

module Individual_Helical_Groove(is_left_handed = false) {
    direction = is_left_handed ? 1 : -1;
    // Model a continuous helical thread track using a progressive twist sweep
    linear_extrude(height = BARREL_LENGTH + 10, center = true, twist = direction * (360 * (BARREL_LENGTH / TWIST_PITCH)), slices = 200, convexity = 10) {
        for (i = [0 : THREADS_PER_TURN - 1]) {
            rotate([0, 0, i * (360 / THREADS_PER_TURN)]) {
                translate([BARREL_INNER_D / 2, 0, 0])
                    square([GROOVE_DEPTH * 2, GROOVE_WIDTH], center = true);
            }
        }
    }
}

module Dual_Threaded_Acoustic_Barrel() {
    difference() {
        // 1. Solid Heavy-Wall Titanium Main Barrel Body
        color("Silver") cylinder(h = BARREL_LENGTH, d = BARREL_OUTER_D, center = true);
        
        // 2. Primary Core Pass-Through (Clear Bore Hole)
        cylinder(h = BARREL_LENGTH + 2, d = BARREL_INNER_D, center = true);
        
        // 3. Right-Handed (Clockwise) Helical Grooves
        color("DimGray") Individual_Helical_Groove(is_left_handed = false);
        
        // 4. Left-Handed (Counter-Clockwise) Helical Grooves
        color("Charcoal") Individual_Helical_Groove(is_left_handed = true);
    }
}

// Render execution call point
Dual_Threaded_Acoustic_Barrel();

