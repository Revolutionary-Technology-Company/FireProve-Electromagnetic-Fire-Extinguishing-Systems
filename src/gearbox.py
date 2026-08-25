// ============================================================================
// FireProve System - Lockheed-Style Gimbal Gearbox Design Blueprint
// Combines high-torque self-locking worm gearboxes with an azimuth slip-ring conduit
// ============================================================================

$fn = 60; // Render resolution global setting

// Global Mechanical Configuration Parameters
BARREL_DIAMETER = 121.92;      // 4.8 inches in mm
SLIP_RING_HOLE    = 40.0;       // Axial center cable clearance hole
WALL_THICKNESS    = 15.0;       // Reinforced chassis structural thickness

// --- 1. Main Assembly Assembly Vector Loop ---
module Complete_Gimbal_Assembly() {
    // Ground Foundation Level (Azimuth Platform Base)
    color("LightSlateGray") Base_Foundation_Plate();
    
    // Bottom Azimuth/Pan Gearbox Hub (Continuous 360-degree rotation)
    translate([0, 0, 20]) {
        color("Teal") Azimuth_Gearbox_Housing();
        color("Gold") translate([0, 85, 45]) rotate([0, 90, 0]) Worm_Drive_Screw(length=120);
    }
    
    // Yoke Support Bracket & Upper Elevation/Tilt Gearbox Hub
    translate([0, 0, 160]) {
        color("DarkSlateGray") Elevation_Yoke_Bracket();
        
        // Tilt Gearbox Offsets (Mounted on the left arm of the Yoke)
        translate([-95, 0, 150]) rotate([0, 90, 0]) {
            color("Teal") Elevation_Gearbox_Housing();
            color("Gold") translate([0, 65, -15]) rotate([90, 0, 0]) Worm_Drive_Screw(length=90);
        }
        
        // Central 4.8" Resonant Titanium Barrel Sleeve Assembly
        translate([0, 0, 150]) rotate([0, 0, 0]) {
            color("Silver") Titanium_Barrel_Sleeve();
        }
    }
}

// --- 2. Module Implementations ---

module Base_Foundation_Plate() {
    difference() {
        cylinder(h=20, d=320, center=false);
        // Central clearance bore for high-current rotational slip rings
        cylinder(h=22, d=SLIP_RING_HOLE+5, center=false);
        // Structural mounting bolt layout (8x perimeter pass-throughs)
        for (a = [0 : 45 : 359]) {
            rotate([0, 0, a]) translate([140, 0, -1]) cylinder(h=22, d=12);
        }
    }
}

module Azimuth_Gearbox_Housing() {
    difference() {
        union() {
            // Main rotating pan gear shell
            cylinder(h=120, d=240, center=false);
            // Worm screw cross-shaft enclosure projection
            translate([-70, 60, 25]) cube([140, 50, 40]);
        }
        // Hollow internal chamber for the 120-tooth worm gear wheel
        translate([0, 0, WALL_THICKNESS]) cylinder(h=120, d=210, center=false);
        // Core center channel pass-through for cable slip ring conduit
        translate([0, 0, -1]) cylinder(h=125, d=SLIP_RING_HOLE, center=false);
        // Horizontal drive-shaft tunnel for worm screw
        translate([-80, 85, 45]) rotate([0, 90, 0]) cylinder(h=160, d=30);
    }
}

module Elevation_Yoke_Bracket() {
    union() {
        // Base plate interface connected to the azimuth rotation stage
        difference() {
            cylinder(h=20, d=238, center=false);
            cylinder(h=22, d=SLIP_RING_HOLE, center=false);
        }
        // Twin rigid upright vertical fork arms (Symmetric spacing)
        for (i = [-1, 1]) {
            scale([i, 1, 1]) translate([80, -40, 20]) difference() {
                cube([30, 80, 180]);
                // Main tilt pivot bearing capture seats
                translate([-5, 40, 150]) rotate([0, 90, 0]) cylinder(h=40, d=50);
            }
        }
    }
}

module Elevation_Gearbox_Housing() {
    difference() {
        union() {
            // Elevation tilt worm gear capsule
            cylinder(h=40, d=160, center=true);
            // Tangential input motor face block
            translate([0, 50, 0]) cube([40, 40, 30], center=true);
        }
        // Center keyed drive shaft channel linked to barrel sleeve pivot
        cylinder(h=45, d=35, center=true);
        // High-torque transverse worm input cross-bore
        translate([0, 65, 0]) rotate([90, 0, 0]) cylinder(h=110, d=20, center=true);
    }
}

module Worm_Drive_Screw(length) {
    union() {
        // Core steel/bronze transmission linkage shaft
        cylinder(h=length, d=18, center=true);
        // Simulated structural self-locking envelope
        cylinder(h=length-30, d=28, center=true);
    }
}

module Titanium_Barrel_Sleeve() {
    rotate([0, 90, 0]) difference() {
        union() {
            // Main heavily reinforced titanium central sleeve jacket
            cylinder(h=200, d=BARREL_DIAMETER + 40, center=true);
            // Lateral pivot shaft trunnions traversing through yoke bearings
            cylinder(h=250, d=45, center=true);
        }
        // Deep internal pass-through cavity accepting the 4.8" rifled tube
        cylinder(h=202, d=BARREL_DIAMETER, center=true);
    }
}

// Render execution call point
Complete_Gimbal_Assembly();

