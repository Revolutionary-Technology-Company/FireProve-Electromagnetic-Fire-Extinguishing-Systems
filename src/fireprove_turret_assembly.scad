// FireProve Titanium Acoustic Suppression Turret Assembly
// Design Parameters matching RT Hexadecimal Architecture Specs

$fn = 64;

// Global Dimensions (Inches converted to mm for OpenSCAD standard)
inch_to_mm = 25.4;
bore_diameter = 4.8 * inch_to_mm;
barrel_length = 54.8 * inch_to_mm;
wall_thickness = 5; // 5mm thick structural titanium walls

module matx_enclosure() {
    // Micro-ATX form factor space (244mm x 244mm motherboard plate)
    // Enclosure scaled to fit PSU, cooling, and RTX 50 TUF GPU
    color("DarkSlateGray", 0.8) {
        difference() {
            cube([350, 300, 400], center=true);
            cube([350 - wall_thickness*2, 300 - wall_thickness*2, 400 - wall_thickness*2], center=true);
        }
    }
    // RTX 50 TUF GPU Space Representation (approx 340mm length, triple slot)
    translate([20, -50, -50]) color("Black") cube([340, 65, 150], center=true);
    // Micro-ATX Motherboard Plate with Hex-Logic Traces spacing
    translate([-10, 0, -140]) color("Green") cube([244, 244, 4], center=true);
}

module pyramidal_mics() {
    // 4 microphones: 2 at +45 deg up, 2 at -45 deg down
    color("Gold") {
        // Upper Left (+45 Up)
        translate([-100, 150, 100]) rotate([45, 0, 45]) cylinder(r=10, h=30, center=true);
        // Upper Right (+45 Up)
        translate([100, 150, 100]) rotate([45, 0, -45]) cylinder(r=10, h=30, center=true);
        // Lower Left (-45 Down)
        translate([-100, 150, -100]) rotate([-45, 0, 45]) cylinder(r=10, h=30, center=true);
        // Lower Right (-45 Down)
        translate([100, 150, -100]) rotate([-45, 0, -45]) cylinder(r=10, h=30, center=true);
    }
}

module titanium_compression_speaker() {
    // Heavy-duty titanium driver base sitting behind the barrel throat
    color("Silver") {
        cylinder(r1=bore_diameter*0.8, r2=bore_diameter/2, h=120, center=true);
        // Internal Titanium Compliance Ring & Dome housing
        translate([0, 0, -70]) cylinder(r=bore_diameter*0.9, h=30, center=true);
    }
}

module rifled_cannon_barrel() {
    // 4.8-inch bore, 54.8-inch long resonant barrel
    color("LightGray", 0.9) {
        difference() {
            // Outer Barrel Shell
            cylinder(r=(bore_diameter/2) + wall_thickness, h=barrel_length, center=false);
            // Inner Bore Hollow
            translate([0, 0, -1]) cylinder(r=bore_diameter/2, h=barrel_length + 2, center=false);
            
            // Decorative Helical Rifling Cut Visualization
            for(a = [0 : 45 : 360]) {
                rotate([0, 0, a]) 
                translate([bore_diameter/2 - 1, 0, 0])
                linear_extrude(height = barrel_length, twist = 360, convexity = 10)
                square([3, 3], center=true);
            }
        }
    }
}

// Complete Turret Main Assembly
module main_assembly() {
    // Lower Chassis Enclosure
    translate([0, 0, -200]) matx_enclosure();
    
    // Pyramidal Array Orientation
    translate([0, 0, 50]) pyramidal_mics();
    
    // Suppression Mechanism Core (Rotated and Pitched Axis)
    rotate([0, 0, 0]) { // Azimuth adjustment
        translate([0, 0, 100]) {
            // Speaker / Driver unit at the rear base of the cannon
            translate([0, 0, -60]) rotate([90, 0, 0]) titanium_compression_speaker();
            // Cannon barrel projecting forward out of the driver throat
            translate([0, 0, 0]) rotate([90, 0, 0]) rifled_cannon_barrel();
        }
    }
}

main_assembly();
