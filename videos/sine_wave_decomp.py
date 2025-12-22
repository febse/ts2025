from manim import (
    Scene, Axes, Text, MathTex, Create, Write, UP, DOWN, UR, RIGHT,
    BLUE, YELLOW, GREEN, PI, DashedLine, VGroup
)
import numpy as np


class SineWaveDecomp(Scene):
    def construct(self):
        # Set up axes with tick labels
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [],  # We'll add custom π labels
            },
            y_axis_config={
                "numbers_to_include": np.arange(-1.5, 2, 0.5),
                "font_size": 24,
            },
            tips=False,
        )
        
        # Create custom x-axis labels in terms of π
        x_tick_labels = VGroup()
        tick_positions = [0, 1, 2, 3, 4, 5]
        label_strings = ["0", r"\pi", r"2\pi", 
                        r"3\pi", r"4\pi", r"5\pi"]
        
        for pos, label_str in zip(tick_positions, label_strings):
            if pos == 0:
                label = MathTex("0", font_size=24)
            else:
                label = MathTex(label_str, font_size=24)
            label.next_to(axes.coords_to_point(pos, 0), DOWN, buff=0.2)
            label.shift(RIGHT * 0.1)  # Shift labels to the right
            x_tick_labels.add(label)
        
        # Add axis labels
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("y", direction=UP, buff=0.3)
        
        # Title
        title = Text("Sine Wave: 2 Periods over [0, 5]", font_size=36)
        title.to_edge(UP)
        
        # Frequency: 2 periods over 5 units
        # Angular frequency: ω = 2π * 1 = 2
        frequency = 1 / 2 * PI
        angular_freq = 2 * PI * frequency
        
        # Create the sine wave function
        def sine_func(t):
            return np.sin(angular_freq * t)
        
        # Create the sine wave graph
        sine_graph = axes.plot(
            sine_func,
            x_range=[0, 5],
            color=YELLOW,
            stroke_width=3
        )
        
        # Add equation label
        # equation = MathTex(
        #     r"y = \sin\left(\frac{4\pi}{5}t\right)",
        #     font_size=40
        # )
        # equation.to_corner(UR, buff=0.5)
        
        # Add frequency label
        freq_label = Text(
            f"Frequency: {frequency:.2f} Hz",
            font_size=24
        )
        freq_label.to_corner(UR, buff=0.5)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        self.play(Write(x_tick_labels))
        self.wait(0.5)
        self.play(Write(freq_label))
        self.wait(0.5)
        self.play(Create(sine_graph), run_time=3)
        self.wait(2)
        
        # Highlight the two periods
        period1_line = DashedLine(
            start=axes.coords_to_point(0, 1.2),
            end=axes.coords_to_point(2.5, 1.2),
            color=GREEN,
            stroke_width=2,
            dash_length=0.1
        )
        
        period2_line = DashedLine(
            start=axes.coords_to_point(2.5, 1.2),
            end=axes.coords_to_point(5, 1.2),
            color=GREEN,
            stroke_width=2,
            dash_length=0.1
        )
        
        period1_label = Text("Period 1", font_size=20, color=GREEN)
        period1_label.next_to(period1_line, UP, buff=0.1)
        period2_label = Text("Period 2", font_size=20, color=GREEN)
        period2_label.next_to(period2_line, UP, buff=0.1)
        
        self.play(
            Create(period1_line),
            Write(period1_label)
        )
        self.wait(0.5)
        self.play(
            Create(period2_line),
            Write(period2_label)
        )
        self.wait(2)

