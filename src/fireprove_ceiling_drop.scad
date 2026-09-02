// ============================================================================
// FireProve System - Recessed Drop-Down Ceiling Mount Variant
// Designed for flush-mount installation within standard 2x2 structural grids
// ============================================================================

$fn = 60; // Global render resolution limit

// Standard T-Bar ceiling tile dimensions (mm)
TILE_SIZE_X = 609.6; // 24 inches
TILE_SIZE_Y = 609.6; // 24 inches
BARREL_DIAMETER = 121.92; // 4.8 inches inner bore

module Ceiling_Turret_Assembly() {
    // 1. Structural T-Bar Perimeter Frame Support
    color("DimGray") difference() {
        cube([TILE_SIZE_X, TILE_SIZE_Y, 20], center=true);
        // Central circular core deployment hatch
        cylinder(h=25, d=350, center=true);
    }
    
    // 2. Sealed Upper Micro-ATX Plated Enclosure Box (Sits above plenum space)
    translate([0, 0, 160]) color("LightSlateGray") difference() {
        cube([400, 400, 300], center=true);
        // Interior cavity footprint space for Micro-ATX board & RTX 50 TUF
        translate([0, 0, -10]) cube([370, 370, 280], center=true);
    }
    
    // 3. Motorized Scissor Lift / Z-Axis Deployment Carriage Assembly
    translate([0, 0, 30]) color("DarkSlateGray") union() {
        // Vertical support rods tracking motor movements
        translate([-120, -120, 0]) cylinder(h=150, d=20, center=true);
        translate([120, -120, 0]) cylinder(h=150, d=20, center=true);
        translate([-120, 120, 0]) cylinder(h=150, d=20, center=true);
        translate([120, 120, 0]) cylinder(h=150, d=20, center=true);
    }
    
    // 4. Low-Profile Motorized Azimuth Swivel Turret (Pops below ceiling line)
    translate([0, 0, -60]) union() {
        color("Teal") cylinder(h=60, d=280, center=true); // Rotational pan driver
        
        // 5. Shortened 54.8" Resonant Contra-Helical Titanium Barrel Sleeve
        // Angled downwards to monitor room floor sectors
        translate([0, 0, -40]) rotate([0, 45, 0]) difference() {
            color("Silver") cylinder(h=240, d=BARREL_DIAMETER + 30, center=true);
            cylinder(h=242, d=BARREL_DIAMETER, center=true); // Clear sound core
        }
        
        // 6. Pyramidal 4-Microphone Tracking Ring Flange
        color("Gold") difference() {
            translate([0, 0, -10]) cylinder(h=15, d=300, center=true);
            cylinder(h=20, d=278, center=true);
        }
    }
}

// Render execution call point
Ceiling_Turret_Assembly();
