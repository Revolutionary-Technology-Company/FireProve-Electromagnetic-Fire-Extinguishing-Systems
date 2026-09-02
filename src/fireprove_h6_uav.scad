// ============================================================================
// FireProve System - H6 Heavy-Lift Fire Suppressor Hexacopter UAV
// Features a structural 6-rotor airframe with a drop-down gimbal payload
// ============================================================================

$fn = 40; // Render optimization setting

ROTOR_ARM_LENGTH = 750;   // 1.5-meter total motor-to-motor diameter
BARREL_DIAMETER  = 121.92; // 4.8 inches inner bore

module Hexacopter_H6_Airframe() {
    // 1. Central Core Avionics & Mainframe Deck
    color("DarkSlateGray") difference() {
        cylinder(h=120, d=340, center=true);
        // Center-bored payload routing bay for high-current wiring loops
        cylinder(h=125, d=60, center=true);
    }
    
    // 2. Thick 3oz Copper Protected Esc/Battery Mounting Trays
    for (b =) {
        rotate([0, 0, b]) translate([0, 130, 0]) 
            color("Teal") cube([140, 80, 40], center=true);
    }

    // 3. 6-Rotor Radial Structural Arms (60-Degree Interlocking Layout)
    for (a = [0 : 60 : 359]) {
        rotate([0, 0, a]) union() {
            // High-tensile carbon-fiber support beams
            color("DimGray") translate([ROTOR_ARM_LENGTH/2, 0, 0]) 
                cube([ROTOR_ARM_LENGTH, 35, 35], center=true);
                
            // Heavy-duty brushless motor pods at outer tips
            color("Gold") translate([ROTOR_ARM_LENGTH, 0, 25]) 
                cylinder(h=50, d=70, center=true);
                
            // Large 32-inch high-performance carbon props
            color("Black") translate([ROTOR_ARM_LENGTH, 0, 52]) 
                cylinder(h=4, d=450, center=true);
        }
    }
    
    // 4. Heavy-Duty Carbon Fiber Deflection Landing Legs
    for (leg = [-1, 1]) {
        scale([leg, 1, 1]) translate([180, 0, -180]) 
            color("Charcoal") cube([25, 400, 300], center=true);
    }
    
    // 5. Bottom Slung Motorized Drop-Down Gimbal Pod
    translate([0, 0, -140]) union() {
        color("LightSlateGray") cylinder(h=60, d=200, center=true); // Pan motor mount
        
        // 6. Suspended 54.8" Contra-Helical Titanium Barrel Cannon Assembly
        translate([0, 0, -60]) rotate([0, 45, 0]) difference() {
            color("Silver") cylinder(h=300, d=BARREL_DIAMETER + 30, center=true);
            cylinder(h=302, d=BARREL_DIAMETER, center=true); // Clear resonant sound bore
        }
    }
}

// Render execution call point
Hexacopter_H6_Airframe();
