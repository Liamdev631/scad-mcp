// Ferris Wheel Model - Refined Version

// Parameters
wheel_radius = 40;
rim_width = 2;
rim_thickness = 1;
spoke_width = 0.6;
num_cabins = 12;
cabin_size = [8, 6, 8]; // Length, Width, Height
support_width = 4;
base_height = 50;
base_spread = 30; // Spread of the A-frame at the bottom

$fn = 20; // Smoothness

// Animation parameter (0 to 1)
rotation_angle = $t * 360;

module rounded_cube(size, r) {
    // 2D extrusion is much faster than 3D hull of spheres
    // Rounds the vertical edges (Z-axis)
    translate([r, r, 0])
        linear_extrude(size[2])
        offset(r=r)
        square([size[0]-2*r, size[1]-2*r]);
}

module cabin() {
    // Main body with rounded corners
    color("FireBrick")
    translate([0, 0, -cabin_size[2]/2]) // Hang from the top point
        difference() {
            union() {
                translate([-cabin_size[0]/2, -cabin_size[1]/2, -cabin_size[2]/2])
                    rounded_cube(cabin_size, 1);
                
                // Roof overhang
                translate([0, 0, cabin_size[2]/2 + 0.5])
                    cube([cabin_size[0] + 1, cabin_size[1] + 1, 0.5], center=true);
            }
            // Windows
            // Side windows
            translate([0, 0, 1])
                cube([cabin_size[0]+2, cabin_size[1]-1.5, cabin_size[2]-3.5], center=true);
            // Front/Back windows
            translate([0, 0, 1])
                cube([cabin_size[0]-2.5, cabin_size[1]+2, cabin_size[2]-3.5], center=true);
        }
    
    // Seats inside
    color("SaddleBrown")
    translate([0, 0, -cabin_size[2]/2 - cabin_size[2]/2 + 1.5])
        cube([cabin_size[0]-1.5, cabin_size[1]-1.5, 0.5], center=true);

    // Hanger Assembly
    color("DimGray")
    union() {
        // Vertical rod
        translate([0, 0, 0])
            cylinder(r=0.3, h=cabin_size[2]/2 + 2);
        // Cross bar at top
        translate([0, 0, cabin_size[2]/2 + 2])
            rotate([90, 0, 0])
            cylinder(r=0.4, h=cabin_size[1], center=true);
        // Side arms down to cabin pivot
        for(y = [-cabin_size[1]/2, cabin_size[1]/2]) {
             translate([0, y, 0])
                cylinder(r=0.3, h=cabin_size[2]/2 + 2);
        }
    }
}

module wheel_structure() {
    // Outer rim
    color("GhostWhite")
    difference() {
        cylinder(r=wheel_radius, h=rim_width, center=true);
        cylinder(r=wheel_radius - rim_thickness, h=rim_width + 0.1, center=true);
    }
    
    // Inner rim (structural)
    color("GhostWhite")
    difference() {
        cylinder(r=wheel_radius * 0.7, h=rim_width, center=true);
        cylinder(r=wheel_radius * 0.7 - rim_thickness, h=rim_width + 0.1, center=true);
    }
    
    // Spokes (Truss style)
    color("LightSlateGray")
    for (i = [0 : num_cabins-1]) {
        angle = i * (360 / num_cabins);
        
        rotate([0, 0, angle]) {
            // Main radial spoke
            translate([wheel_radius/2, 0, 0])
                cube([wheel_radius, spoke_width, spoke_width], center=true);
            
            // Cross bracing (X pattern between spokes)
            // Use simple cylinders for bracing instead of hull if performance is an issue,
            // but hull of small spheres is usually okay.
            // Diagonal 1: Inner (current) to Outer (next)
            hull() {
                translate([wheel_radius * 0.7, 0, 0]) sphere(r=spoke_width/2);
                rotate([0, 0, 360/num_cabins]) translate([wheel_radius, 0, 0]) sphere(r=spoke_width/2);
            }
            // Diagonal 2: Outer (current) to Inner (next)
             hull() {
                translate([wheel_radius, 0, 0]) sphere(r=spoke_width/2);
                rotate([0, 0, 360/num_cabins]) translate([wheel_radius * 0.7, 0, 0]) sphere(r=spoke_width/2);
            }
        }
    }
    
    // Center hub plate
    color("SlateGray")
    difference() {
        cylinder(r=5, h=rim_width*1.2, center=true);
        // Bolt holes
        for(r = [0:60:360]) rotate([0,0,r]) translate([3.5,0,0]) cylinder(r=0.5, h=10, center=true);
    }
    
    // Hub decoration cap
    color("Gold")
    translate([0,0,rim_width/2]) cylinder(r=1.5, h=1);
}

module support_leg() {
    // Tapered leg
    hull() {
        translate([0, 0, base_height]) rotate([90, 0, 0]) cylinder(r=1.5, h=support_width, center=true);
        translate([base_spread/2, 0, 0]) cube([2, support_width, 2], center=true);
    }
}

module support_frame() {
    color("SteelBlue")
    union() {
        // Left Leg
        support_leg();
        // Right Leg
        mirror([1, 0, 0]) support_leg();
        
        // Cross bracing
        translate([0, 0, base_height * 0.6]) cube([base_spread * 0.4, support_width * 0.8, 1], center=true);
        translate([0, 0, base_height * 0.3]) cube([base_spread * 0.7, support_width * 0.8, 1], center=true);
    }
    
    // Bearing Block at top
    color("DarkSlateGray")
    translate([0, 0, base_height])
        rotate([90, 0, 0])
        cylinder(r=3, h=support_width + 2, center=true);
}

module fence_segment(length) {
    color("Sienna")
    union() {
        // Posts
        translate([-length/2, 0, 2.5]) cube([2, 2, 5], center=true);
        translate([length/2, 0, 2.5]) cube([2, 2, 5], center=true);
        // Rails
        translate([0, 0, 4]) cube([length, 0.5, 0.5], center=true);
        translate([0, 0, 2]) cube([length, 0.5, 0.5], center=true);
        // Pickets
        for(x = [-length/2+2 : 3 : length/2-2]) {
             translate([x, 0, 2.5]) cube([1, 0.2, 4], center=true);
        }
    }
}

module ticket_booth() {
    color("Crimson")
    translate([0, 0, 5])
        difference() {
            cube([6, 6, 10], center=true);
            // Window
            translate([0, -2, 1]) cube([5, 4, 4], center=true);
            // Door
            translate([0, 4, -1]) cube([4, 4, 8], center=true);
        }
    // Roof
    color("White")
    translate([0, 0, 11])
        cylinder(r1=5, r2=0, h=3, $fn=4);
}

module ferris_wheel() {
    // Lift wheel up
    translate([0, 0, base_height]) {
        rotate([90, 0, 0]) // Orient wheel vertical
        rotate([0, 0, rotation_angle]) { // Animation rotation
            wheel_structure();
            
            // Cabins
            for (i = [0 : num_cabins-1]) {
                angle = i * (360 / num_cabins);
                // Using explicit coordinates to avoid rotation of the cabin's frame
                translate([wheel_radius * cos(angle), wheel_radius * sin(angle), 0])
                    rotate([0, 0, -angle - rotation_angle]) // Counter-rotate to keep upright
                    rotate([-90, 0, 0]) // Fix orientation relative to world
                    cabin();
            }
        }
    }
    
    // Supports on both sides
    translate([0, 6, 0]) support_frame();
    translate([0, -6, 0]) support_frame();
    
    // Axle
    color("Silver")
    translate([0, 0, base_height])
        rotate([90, 0, 0])
        cylinder(r=1.5, h=16, center=true);

    // Base platform
    color("DarkGreen")
    translate([0, 0, -1])
        cube([base_spread * 1.8, 50, 2], center=true);
        
    // Entrance ramp/steps
    color("SaddleBrown")
    translate([0, 18, 1])
        cube([10, 10, 2], center=true);
        
    // Fences
    translate([base_spread * 0.7, 0, 0]) rotate([0, 0, 90]) fence_segment(40);
    translate([-base_spread * 0.7, 0, 0]) rotate([0, 0, 90]) fence_segment(40);
    translate([0, -20, 0]) fence_segment(base_spread * 1.4);
    
    // Ticket Booth
    translate([-20, 20, 0]) rotate([0, 0, -30]) ticket_booth();
}

ferris_wheel();
