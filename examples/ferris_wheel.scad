// Ferris Wheel Model - Final Detailed Version

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
wheel_separation = 12; // Distance between the two wheel rims

// Sanity Checks and Assertions
assert(wheel_radius > 0, "Wheel radius must be positive");
assert(num_cabins > 2, "Must have at least 3 cabins");
assert(base_height > wheel_radius + cabin_size[2], "Base height too low! Cabins will hit the ground.");
assert(wheel_separation > cabin_size[1], "Wheel separation too small! Cabins will hit the wheels.");

$fn = 20; // Smoothness

// Animation parameter (0 to 1)
rotation_angle = $t * 360;

module rounded_cube(size, r) {
    // 2D extrusion is much faster than 3D hull of spheres
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
                translate([0, 0, cabin_size[2]/2])
                    cube([cabin_size[0] + 1, cabin_size[1] + 1, 0.5], center=true);
            }
            // Windows
            translate([0, 0, 1])
                cube([cabin_size[0]+2, cabin_size[1]-1.5, cabin_size[2]-3.5], center=true);
            translate([0, 0, 1])
                cube([cabin_size[0]-2.5, cabin_size[1]+2, cabin_size[2]-3.5], center=true);
        }
    
    // Seats inside
    color("SaddleBrown")
    translate([0, 0, -cabin_size[2]/2 - cabin_size[2]/2 + 1.5])
        cube([cabin_size[0]-1.5, cabin_size[1]-1.5, 0.5], center=true);

    // Hanger Assembly (Simplified to a bar connecting the wheels)
    color("DimGray")
    rotate([90, 0, 0])
    cylinder(r=0.6, h=wheel_separation + rim_width + 2, center=true);
}

module wheel_structure() {
    // Outer rim
    color("GhostWhite")
    difference() {
        cylinder(r=wheel_radius, h=rim_width, center=true);
        cylinder(r=wheel_radius - rim_thickness, h=rim_width + 0.1, center=true);
    }
    
    // Inner rim
    color("GhostWhite")
    difference() {
        cylinder(r=wheel_radius * 0.7, h=rim_width, center=true);
        cylinder(r=wheel_radius * 0.7 - rim_thickness, h=rim_width + 0.1, center=true);
    }
    
    // Spokes
    color("LightSlateGray")
    for (i = [0 : num_cabins-1]) {
        angle = i * (360 / num_cabins);
        rotate([0, 0, angle]) {
            translate([wheel_radius/2, 0, 0])
                cube([wheel_radius, spoke_width, spoke_width], center=true);
            
            // Simple cross bracing using cylinders (faster render than hull)
            translate([wheel_radius * 0.83, 0, 0])
                rotate([0, 0, 15])
                cube([wheel_radius * 0.3, spoke_width/2, spoke_width/2], center=true);
             translate([wheel_radius * 0.83, 0, 0])
                rotate([0, 0, -15])
                cube([wheel_radius * 0.3, spoke_width/2, spoke_width/2], center=true);
        }
    }
    
    // Center hub plate
    color("SlateGray")
    difference() {
        cylinder(r=5, h=rim_width*1.2, center=true);
        for(r = [0:60:360]) rotate([0,0,r]) translate([3.5,0,0]) cylinder(r=0.5, h=10, center=true);
    }
    
    // Hub decoration
    color("Gold")
    translate([0,0,rim_width/2]) cylinder(r=1.5, h=1);
}

module support_frame() {
    color("SteelBlue")
    union() {
        // Legs
        hull() {
            translate([0, 0, base_height]) rotate([90, 0, 0]) cylinder(r=1.5, h=support_width, center=true);
            translate([base_spread/2, 0, 0]) cube([2, support_width, 2], center=true);
        }
        mirror([1, 0, 0]) hull() {
            translate([0, 0, base_height]) rotate([90, 0, 0]) cylinder(r=1.5, h=support_width, center=true);
            translate([base_spread/2, 0, 0]) cube([2, support_width, 2], center=true);
        }
        
        // Cross bracing
        translate([0, 0, base_height * 0.6]) cube([base_spread * 0.4, support_width * 0.8, 1], center=true);
        translate([0, 0, base_height * 0.3]) cube([base_spread * 0.7, support_width * 0.8, 1], center=true);
    }
    
    // Bearing Block
    color("DarkSlateGray")
    translate([0, 0, base_height])
        rotate([90, 0, 0])
        cylinder(r=3, h=support_width + 2, center=true);
}

module fence_segment(length) {
    color("Sienna")
    union() {
        translate([-length/2, 0, 2.5]) cube([2, 2, 5], center=true);
        translate([length/2, 0, 2.5]) cube([2, 2, 5], center=true);
        translate([0, 0, 4]) cube([length, 0.5, 0.5], center=true);
        translate([0, 0, 2]) cube([length, 0.5, 0.5], center=true);
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
            translate([0, -2, 1]) cube([5, 4, 4], center=true); // Window
            translate([0, 4, -1]) cube([4, 4, 8], center=true); // Door
        }
    // Ledge
    color("SaddleBrown")
    translate([0, -3.5, 3]) cube([6, 1, 0.5], center=true);
    
    // Roof
    color("White")
    translate([0, 0, 11])
        cylinder(r1=5, r2=0, h=3, $fn=4);
}

module stairs() {
    color("SaddleBrown")
    for(i = [0:4]) {
        translate([0, i*2, i])
            cube([10, 2, 1], center=true);
    }
}

module ferris_wheel() {
    // Lift wheel up
    translate([0, 0, base_height]) {
        rotate([90, 0, 0])
        rotate([0, 0, rotation_angle]) {
            // First Wheel
            translate([0, 0, -wheel_separation/2]) wheel_structure();
            // Second Wheel
            translate([0, 0, wheel_separation/2]) wheel_structure();
            
            // Connecting rods and cabins
            for (i = [0 : num_cabins-1]) {
                angle = i * (360 / num_cabins);
                
                // Cabin (includes the connecting bar)
                // Using explicit coordinates to avoid rotation of the cabin's frame
                translate([wheel_radius * cos(angle), wheel_radius * sin(angle), 0])
                    rotate([0, 0, -rotation_angle]) // Counter-rotate to keep upright
                    rotate([-90, 0, 0]) // Fix orientation relative to world
                    cabin();
            }
        }
    }
    
    // Supports - moved out to clear the wider wheel assembly
    translate([0, wheel_separation/2 + 6, 0]) support_frame();
    translate([0, -wheel_separation/2 - 6, 0]) support_frame();
    
    // Axle
    color("Silver")
    translate([0, 0, base_height])
        rotate([90, 0, 0])
        cylinder(r=1.2, h=wheel_separation + 20, center=true);

    // Base platform
    color("DarkGreen")
    translate([0, 0, -1])
        cube([base_spread * 2.5, 60 + wheel_separation, 2], center=true);
        
    // Path to entrance
    color("Gray")
    translate([0, 20 + wheel_separation/2, -0.9])
        cube([12, 40, 2.1], center=true);

    // Entrance stairs
    translate([0, 15 + wheel_separation/2, 1]) stairs();
        
    // Fences
    translate([base_spread * 0.7, 0, 0]) rotate([0, 0, 90]) fence_segment(40 + wheel_separation);
    translate([-base_spread * 0.7, 0, 0]) rotate([0, 0, 90]) fence_segment(40 + wheel_separation);
    translate([0, -20 - wheel_separation/2, 0]) fence_segment(base_spread * 1.4);
    
    // Ticket Booth
    translate([-20, 20 + wheel_separation/2, 0]) rotate([0, 0, -30]) ticket_booth();
}

ferris_wheel();
