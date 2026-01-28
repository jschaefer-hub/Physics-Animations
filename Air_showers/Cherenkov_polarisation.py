


from manimlib.constants import RED_B
from tkinter import CENTER
from matplotlib.dates import MO
from manimlib import *
  
# ---------------------
#     Scenes
# ---------------------

class lightspeed(Scene):
    def construct(self):
        Polarization.construct(self,
         speed_of_light = 2 # particle at lightspeed
         )

class sublight(Scene):
    def construct(self):
        Polarization.construct(self,
         speed_of_light = 20 # speed of light is much faster than the particle
         )

class superluminal(Scene):
    def construct(self):
        Polarization.construct(self,
         speed_of_light = 1.5 # speed of light is slightly slower than the particle
         )


# ---------------------
#     Scene Code
# ---------------------
class PolarizableMolecules(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create the enclosing circle/ellipse
        self.frame = Circle(radius=0.5)
        self.frame.set_fill(WHITE, opacity=1)
        self.frame.set_stroke(BLUE_E, width=0)
        
        # Setup the two charges
        self.pos_charge = Text("+", font_size=30, opacity = 2).set_color(RED_A)
        self.neg_charge = Text("-", font_size=54, opacity = 2).set_color(BLACK)
        
        # Initial positions of charges (centered)
        self.add(self.frame, self.pos_charge, self.neg_charge)
        
        # Scale factor for stretching of the molecule
        self.scale_stretch = 5.0 

    def update_molecule(self, test_charge_loc):
        """
        Update the molecule's position and orientation based on 
        the test charge's position.
        """

        self.stretch_molecule(test_charge_loc)
        self.rotate_to_mob(test_charge_loc)

    def rotate_to_mob(self, test_charge_loc):
        """
        Rotate the molecule to face the test charge.
        """
        
        # Calculate the angle onto which we need to rotate
        angle = angle_of_vector(
            test_charge_loc - self.frame.get_center()
            )
        
        # and rotate by the angle
        self.rotate(angle)

    def stretch_molecule(self, test_charge_loc):
        """
        Stretch the molecule based on the test charge's position.
        """

        target_vector = test_charge_loc - self.frame.get_center()
        target_distance = get_norm(target_vector)

        # Determine strenght of stretch 1/r^2
        strength = self.scale_stretch / (target_distance + 0.5)**1.2

        #     The minimum stretch is no change to molecule (1)
        stretch_strength = np.clip(strength, 1.0, 1.7)
        
        #     Elongate in the direction of the charge
        self.frame.stretch(stretch_strength, 0)

        #     And compress in the perpendicular direction
        self.frame.stretch(max(1/stretch_strength,0.8), 1)

        # Shift the charges
        strength_clip = np.clip(strength, 0, 1.7)
        self.pos_charge.move_to(self.get_center() + RIGHT * strength_clip/4)
        self.neg_charge.move_to(self.get_center() + LEFT * strength_clip/4)
    
class Polarization(Scene):
    def construct(self, speed_of_light):


        self.speed_of_light = speed_of_light

        # Set the framerate
        self.framerate = 60

        # ------------------------
        #    Grid of Molecules
        # ------------------------
        # List of molecule objects
        Molecules = VGroup()
        
        n_rows = 7
        n_columns = 6

        # Instanciate the molecules
        for i in range(n_rows*n_columns):
            m = PolarizableMolecules()
            m.stretch(1.2, dim=0)
            Molecules.add(m)
            
        # Distribute them over a grid
        Molecules.arrange_in_grid(
            n_rows, 
            n_columns, 
            buff=1  # Spacing between dots
        )
        
        # Save the state of the molecules (non-rotated)
        for m in Molecules:
            m.save_state()
            
        # Add them to the scene
        self.add(Molecules)
        
        # ------------------------
        #    Camera Setup
        # ------------------------
        # Lets autoscale the width and length of the frame
        self.camera.frame.set_width(Molecules.get_width()*1)
        self.camera.frame.set_height(Molecules.get_height()*1.2)

        # Move the frame to the center of the molecules
        self.camera.frame.move_to(Molecules.get_center())

        # ------------------------
        #    Test charge
        # ------------------------

        # Create a group to hold the charge point and its label
        test_charge = VGroup() 
        dot = Dot(radius=0.3)
        dot.set_color(BLUE)
        
        # Add LaTeX label to the dot
        label = Tex("\\mu")
        label.set_color(WHITE)
        label.set_width(dot.get_width() * 0.6) # Scale to fit inside
        label.move_to(dot.get_center())
        
        # Add them and move to the starting position
        test_charge.add(dot, label)
        test_charge.move_to([0,10,0])
        
        # ----------------------------
        #     History Tracking
        # ----------------------------
        # To realise the time delay based on the speed of light we track 
        # the position of the charge over time

        # 
        lockback_time = 100      # [s]
        history_steps = lockback_time*self.framerate
        
        # This will be used as a ring-buffer to store the simulation timestamp 
        # per frame
        self.history_time = np.zeros(history_steps)


        # Create the history buffer for the charged test particle
        # Note: We set the start position for all look back times so every 
        # molecule initially knows where the charge is. 
        self.history_pos = [
            test_charge.get_center().copy() for _ in range(history_steps)
        ]

        # ----------------------------
        # Lightspeed influence circle
        # ----------------------------
        # Indicates the circle of influence of the charges original position 
        # with respect to the initial position of the charge

        Influence_circle = Circle(radius=0.1)
        Influence_circle.set_stroke(WHITE, width=3)
        Influence_circle.move_to(test_charge.get_center())
        
        Influence_text = Text("Lightspeed influence", font_size=30)
        Influence_text.set_color(WHITE)

        # Initial position of text
        Influence_text.next_to(Influence_circle, DOWN, buff=0.1)
        
        self.add(Influence_circle, Influence_text)

        # ----------------------------
        #      Trajectory arrow
        # ----------------------------
        # Create the arrow
        arrow = Arrow([0,10,0], [0,-7,0], color=BLUE)
        
        arrow_text = Text("Trajectory", font_size=24)
        arrow_text.next_to(arrow.end, DOWN, buff=-0.2)
        
        self.add(arrow, arrow_text)


        # ----------------------------
        #     Update Callback
        # ----------------------------
        def update_system(mob, dt):
            """
            Update the simulation state for each frame
            """

            # Update history 
            # Shift all times back by one and add the new timestamp 
            # (used as ringbuffer)
            # Note: dt is the time since last frame in the updater
            self.history_time = np.roll(self.history_time, -1)
            self.history_time[-1] = self.history_time[-2] + dt
            current_time = self.history_time[-1]

            # Also track the position of the test charge
            self.history_pos = np.roll(self.history_pos, -1, axis = 0)
            self.history_pos[-1] = test_charge.get_center().copy()

            # Update Lightspeed influence circle 
            radius = self.speed_of_light * current_time
            opacity = 2.0 / (1.0 + 0.5 * radius**2) # Decays as 1/r^2 (intensity)
            opacity = np.clip(opacity, 0, 1)
            
            Influence_circle.become(
                Circle(radius=radius)
                .set_stroke(WHITE, width=10, opacity=opacity)
                .move_to(Influence_circle.get_center())
            )
            
            # Move text with the circle
            Influence_text.next_to(Influence_circle, DOWN, buff=0.7)
            Influence_text.set_opacity(opacity)


            # Update Molecules
            for i, m in enumerate(Molecules):
                m_loc =  m.get_center()
                
                # For each test charge position in the history, we compute
                # the physical distance between the molecule and the charge.
                physical_distances = np.linalg.norm(self.history_pos - m_loc, axis=1)
                
                # For each test charge position in the history, we compute
                # the distance light would have travelled since the simulation start.
                light_travel_distances = self.speed_of_light * (current_time-self.history_time)
                
                # Now we just need to find the closest value in physical_distances to light_travel_distances
                # Note:
                # We compare element by element as each physical distance has an associated light travel distance 
                # with respect to the current simulation time
                reachable = light_travel_distances >= physical_distances
                
                # If none are reachable, we skip this molecule and mark it as unengaged
                if np.sum(reachable) == 0:
                    m.frame.set_fill(WHITE, opacity=0.1)
                    continue
                
                # Reachable is now a list [True, True, False, False, ...]
                # Given the current simulation time, the chargelocation which influences 
                # the molecule in this moment is the one which is "just" reachable (so the True->False transition)
                # The index we want is tha last one where the boolean is non-zero
                retarded_time_index = np.flatnonzero(reachable)[-1]

                # restore the particle to original position and update
                m.restore()
                m.update_molecule(self.history_pos[retarded_time_index])


        # Add updater to Molecules
        Molecules.add_updater(update_system)

        # Play animation by moving test charge downwards
        self.play(
            test_charge.animate.move_to([0,-10,0]),
            run_time=10, 
            rate_func=linear
        )