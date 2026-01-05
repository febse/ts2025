from manim import (
    Scene, Axes, Text, MathTex, Create, Write, FadeIn, FadeOut, Transform,
    UP, DOWN, LEFT, RIGHT, ORIGIN, UR, UL,
    BLUE, YELLOW, GREEN, RED, WHITE, PI,
    Circle, Dot, Line, DashedLine, VGroup, ValueTracker, VMobject,
    always_redraw, rate_functions
)
import numpy as np


class SineWavesDifferentFrequencies(Scene):
    def construct(self):
        # Title (doubled runtime)
        # title = Text("Angular Frequency and the Sine Wave", font_size=36)
        # title.to_edge(UP, buff=0.3)
        # self.play(Write(title), run_time=2)
        
        # self.play(FadeOut(title))
        
        # Storage for completed frequency displays
        completed_displays = []
        
        # Now animate for frequencies 1, 2, 3, 0.5 Hz
        for i, omega in enumerate([1, 2, 3, 0.5]):
            components = self.show_angular_frequency_full(omega, i, completed_displays)
            completed_displays.append(components)
        
        # All frequencies are now displayed as static sine waves
        # Wait a bit to show the final stacked result
        # self.wait(2)
        
        # Now move all displays back to center and reanimate
        # Position them vertically aligned, centered
        scale_up_factor = 1 / 0.3  # Inverse of scale_factor used earlier
        
        # Calculate vertical positions for 4 displays
        # They should be centered vertically as a group
        # The small displays were spaced at 1.2 units apart
        # After scaling up, we need slightly less spacing to fit on screen

        spacing = 1.2 * scale_up_factor * 0.75  # Scale with adjustment factor to fit screen
        total_height = (len(completed_displays) - 1) * spacing
        start_y = total_height / 2
        
        # Move all displays to center positions, vertically aligned
        animations = []

        for i, components in enumerate(completed_displays):
            y_position = start_y - i * spacing
            target_position = UP * y_position
            animations.append(
                components['display_group'].animate.scale(scale_up_factor).move_to(target_position)
            )
        
        self.play(*animations, run_time=2)
        self.wait(0.5)
        
        # Create a group of all display groups to scale them together
        all_displays_group = VGroup(*[comp['display_group'] for comp in completed_displays])
        
        # Scale the entire group to fit on screen (equal scaling in both directions)
        self.play(
            all_displays_group.animate.scale(0.4),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Reanimate all frequencies
        for components in completed_displays:
            # Reset tracker to 0
            components['t_tracker'].set_value(0)
            
            # Re-add the rotating elements
            self.add(components['rotating_dot'], components['radius_line'], components['im_line'])
            
            # Create updaters for continuous animation
            angular_freq = components['angular_freq']
            circle_axes = components['circle_axes']
            sine_axes = components['sine_axes']
            t_tracker = components['t_tracker']
            
            def make_update_dot(af, ca, tt):
                def update_dot(mob):
                    t = tt.get_value()
                    mob.move_to(ca.c2p(
                        np.cos(af * t),
                        np.sin(af * t)
                    ))
                return update_dot
            
            def make_update_radius(af, ca, tt):
                def update_radius(mob):
                    t = tt.get_value()
                    mob.put_start_and_end_on(
                        ca.c2p(0, 0),
                        ca.c2p(np.cos(af * t), np.sin(af * t))
                    )
                return update_radius
            
            def make_update_im_line(af, ca, tt):
                def update_im_line(mob):
                    t = tt.get_value()
                    x = np.cos(af * t)
                    y = np.sin(af * t)
                    if abs(y) < 0.001:
                        y_end = 0.001 if y >= 0 else -0.001
                    else:
                        y_end = 0
                    mob.put_start_and_end_on(
                        ca.c2p(x, y),
                        ca.c2p(x, y_end)
                    )
                return update_im_line
            
            def make_update_path(af, sa, tt):
                def update_path(mob):
                    t = tt.get_value()
                    if t > 0.01:
                        num_points = max(2, int(t * 100))
                        t_vals = np.linspace(0, t, num_points)
                        points = [sa.c2p(tv, np.sin(af * tv)) for tv in t_vals]
                        mob.clear_points()
                        if len(points) > 1:
                            mob.set_points_as_corners(points)
                    else:
                        mob.clear_points()
                return update_path
            
            components['rotating_dot'].add_updater(make_update_dot(angular_freq, circle_axes, t_tracker))
            components['radius_line'].add_updater(make_update_radius(angular_freq, circle_axes, t_tracker))
            components['im_line'].add_updater(make_update_im_line(angular_freq, circle_axes, t_tracker))
            components['traced_path'].add_updater(make_update_path(angular_freq, sine_axes, t_tracker))
        
        # Animate all simultaneously for 2 seconds
        tracker_animations = []
        for components in completed_displays:
            tracker_animations.append(
                components['t_tracker'].animate.set_value(2)
            )
        
        self.play(*tracker_animations, run_time=4, rate_func=rate_functions.linear)
        self.wait(1)
    
    def show_angular_frequency_full(self, f, index, completed_displays):
        """Show animation for a given frequency (in Hz), then shrink and stack"""
        
        # omega is frequency in Hz, convert to angular frequency (rad/s)
        # f_angular = 2π * f
        angular_freq = 2 * PI * f
        
        # Create two side-by-side plots
        # Left: Unit circle in complex plane
        circle_axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=4,
            y_length=4,
            axis_config={"color": BLUE},
            tips=False,
        )
        circle_axes.shift(LEFT * 3.5 + DOWN * 0.5)
        
        # Right: Sine wave over time (0 to 2 seconds)
        sine_axes = Axes(
            x_range=[0, 2, 0.5],  # 0 to 2 seconds
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [],
            },
            y_axis_config={
                "numbers_to_include": [-1, 0, 1],
                "font_size": 20,
            },
            tips=False,
        )
        sine_axes.shift(RIGHT * 2.5 + DOWN * 0.5)
        
        # Add labels for circle axes
        circle_x_label = MathTex("\\text{Re}", font_size=24)
        circle_x_label.next_to(circle_axes.get_x_axis().get_end(), RIGHT, buff=0.1)
        circle_y_label = MathTex("\\text{Im}", font_size=24)
        circle_y_label.next_to(circle_axes.get_y_axis().get_end(), UP, buff=0.1)
        
        # Add labels for sine axes
        sine_x_label = MathTex("t \\text{ (s)}", font_size=24)
        sine_x_label.next_to(sine_axes.get_x_axis().get_end(), RIGHT, buff=0.1)
        sine_y_label = MathTex("\\sin(2\\pi f t)", font_size=24)
        sine_y_label.next_to(sine_axes.get_y_axis().get_end(), UP, buff=0.1)
        
        # Add custom x-axis labels for sine plot (in seconds, 0 to 2)
        x_tick_labels = VGroup()
        # Show labels at 0, 0.5, 1, 1.5, 2 seconds
        for t_sec in [0, 0.5, 1, 1.5, 2]:
            label = MathTex(f"{t_sec:.1f}" if t_sec != int(t_sec) else f"{int(t_sec)}", font_size=20)
            label.next_to(sine_axes.c2p(t_sec, 0), DOWN, buff=0.2)
            x_tick_labels.add(label)
        
        # Frequency label
        if f == 0.5:
            omega_label = MathTex(f"f = \\frac{{1}}{{2}}\\text{{ Hz}}", font_size=32, color=YELLOW)
        else:
            omega_label = MathTex(f"f = {int(f) if f == int(f) else f}\\text{{ Hz}}", font_size=32, color=YELLOW)
        omega_label.next_to(sine_axes, UP, buff=0.3)
        
        # Draw axes (doubled runtime)
        self.play(
            Create(circle_axes),
            Create(sine_axes),
            Write(circle_x_label),
            Write(circle_y_label),
            Write(sine_x_label),
            Write(sine_y_label),
            Write(x_tick_labels),
            Write(omega_label),
            run_time=2
        )
        self.wait(0.6)
        
        # Unit circle (doubled runtime)
        unit_circle = Circle(radius=circle_axes.x_axis.unit_size, color=WHITE)
        unit_circle.move_to(circle_axes.c2p(0, 0))
        self.play(Create(unit_circle), run_time=2)
        self.wait(0.6)
        
        # Create a regular ValueTracker for the initial animation
        t_tracker = ValueTracker(0)
        
        # Rotating point on unit circle
        rotating_dot = Dot(color=RED, radius=0.08)
        rotating_dot.move_to(circle_axes.c2p(1, 0))
        
        # Radius line from center to rotating point
        radius_line = Line(
            start=circle_axes.c2p(0, 0),
            end=circle_axes.c2p(1, 0),
            color=YELLOW,
            stroke_width=2
        )
        
        # Vertical line showing imaginary component
        im_line = DashedLine(
            start=circle_axes.c2p(1, 0),
            end=circle_axes.c2p(1, 0.01),
            color=GREEN,
            stroke_width=2,
            dash_length=0.05
        )
        
        # Add updaters for circle elements
        def update_dot(mob):
            t = t_tracker.get_value()
            mob.move_to(circle_axes.c2p(
                np.cos(angular_freq * t),
                np.sin(angular_freq * t)
            ))
        
        def update_radius(mob):
            t = t_tracker.get_value()
            mob.put_start_and_end_on(
                circle_axes.c2p(0, 0),
                circle_axes.c2p(np.cos(angular_freq * t), np.sin(angular_freq * t))
            )
        
        def update_im_line(mob):
            t = t_tracker.get_value()
            x = np.cos(angular_freq * t)
            y = np.sin(angular_freq * t)
            # Avoid zero-length lines
            if abs(y) < 0.001:
                y_end = 0.001 if y >= 0 else -0.001
            else:
                y_end = 0
            mob.put_start_and_end_on(
                circle_axes.c2p(x, y),
                circle_axes.c2p(x, y_end)
            )
        
        rotating_dot.add_updater(update_dot)
        radius_line.add_updater(update_radius)
        im_line.add_updater(update_im_line)
        
        # Add the rotating elements
        self.add(rotating_dot, radius_line, im_line)
        self.wait(0.4)
        
        # Create traced path for sine wave
        traced_path = VMobject(color=RED, stroke_width=3)
        
        def update_path(mob):
            """Update the traced sine wave path"""
            t = t_tracker.get_value()  # Time in seconds (0 to 2, looping)
            if t > 0.01:
                # Sample points along the sine curve from 0 to current t
                num_points = max(2, int(t * 100))
                t_vals = np.linspace(0, t, num_points)
                # Plot sin(ω * t) where ω is angular frequency
                points = [sine_axes.c2p(tv, np.sin(angular_freq * tv)) for tv in t_vals]
                
                # Clear and redraw
                mob.clear_points()
                if len(points) > 1:
                    mob.set_points_as_corners(points)
            else:
                # At the start of a loop, clear the path
                mob.clear_points()
        
        traced_path.add_updater(update_path)
        self.add(traced_path)
        
        # Animate for 2 seconds (initial display in center)
        # Runtime is doubled to 4 seconds for smoother animation
        self.play(
            t_tracker.animate.set_value(2),
            run_time=4,
            rate_func=rate_functions.linear
        )
        self.wait(1)
        
        # Clear all updaters before shrinking - we want static display
        rotating_dot.clear_updaters()
        radius_line.clear_updaters()
        im_line.clear_updaters()
        traced_path.clear_updaters()
        
        # Remove the rotating elements - we only want to keep the final sine wave
        self.play(
            FadeOut(rotating_dot),
            FadeOut(radius_line),
            FadeOut(im_line),
            run_time=1
        )
        
        # Group everything together for shrinking and moving (no rotating elements)
        display_group = VGroup(
            circle_axes, sine_axes,
            circle_x_label, circle_y_label,
            sine_x_label, sine_y_label,
            x_tick_labels, omega_label,
            unit_circle, traced_path
        )
        
        # Calculate position in stack (at the top right)
        # Each display is 1.2 units tall in the stack
        scale_factor = 0.3
        y_position = 3 - index * 1.2
        target_position = UP * y_position + RIGHT * 3.5
        
        # Shrink and move to stacked position (doubled runtime)
        self.play(
            display_group.animate.scale(scale_factor).move_to(target_position),
            run_time=2
        )
        self.wait(0.6)
        
        # Display is now static - no further animation in background
        # Store components for potential reanimation in a dict
        components = {
            't_tracker': t_tracker,
            'rotating_dot': rotating_dot,
            'radius_line': radius_line,
            'im_line': im_line,
            'traced_path': traced_path,
            'circle_axes': circle_axes,
            'sine_axes': sine_axes,
            'angular_freq': angular_freq,
            'display_group': display_group
        }
        
        return components


class AngularFrequencyCompare(Scene):
    """Alternative version showing all frequencies at once for comparison"""
    
    def construct(self):
        # Title
        title = Text("Comparing Angular Frequencies", font_size=36)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create axes for sine waves
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []},
            tips=False,
        )
        axes.shift(DOWN * 0.5)
        
        # Add custom x-axis labels (in terms of π)
        x_tick_labels = VGroup()
        tick_positions = [0, PI, 2*PI, 3*PI, 4*PI]
        label_strings = ["0", r"\pi", r"2\pi", r"3\pi", r"4\pi"]
        
        for pos, label_str in zip(tick_positions, label_strings):
            label = MathTex(label_str, font_size=24)
            label.next_to(axes.c2p(pos, 0), DOWN, buff=0.2)
            x_tick_labels.add(label)
        
        # Add axis labels
        x_label = MathTex("t", font_size=28)
        x_label.next_to(axes.get_x_axis().get_end(), RIGHT)
        
        self.play(Create(axes), Write(x_tick_labels), Write(x_label))
        self.wait(0.5)
        
        # Create sine waves for different angular frequencies
        colors = [RED, YELLOW, GREEN, BLUE]
        omegas = [1, 2, 3, 4]
        
        for i, (omega, color) in enumerate(zip(omegas, colors)):
            # Offset each sine wave vertically for visibility
            offset = 3 - 1.5 * i
            
            sine_graph = axes.plot(
                lambda t, w=omega, off=offset: np.sin(w * t) + off,
                x_range=[0, 4 * PI],
                color=color,
                stroke_width=3
            )
            
            # Label
            label = MathTex(f"\\omega = {omega}", font_size=24, color=color)
            label.next_to(axes.c2p(4 * PI, offset), RIGHT, buff=0.2)
            
            self.play(Create(sine_graph), Write(label), run_time=2)
            self.wait(0.5)
        
        self.wait(3)

