from manim import (
    ThreeDScene,
    ThreeDAxes,
    ParametricFunction,
    Dot,
    Dot3D,
    Line,
    ValueTracker,
    always_redraw,
    MathTex,
    Text,
    FadeIn,
    FadeOut,
    Create,
    Write,
    DEGREES,
    PI,
    BLUE,
    YELLOW,
    RED,
    GREEN,
    UP,
    RIGHT,
)
import numpy as np


class ComplexSineWave(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            z_range=[0, 6.5, 1],
            x_length=6,
            y_length=6,
            z_length=5,
        )
        axes.z_axis.set_opacity(0)

        circle_2d = ParametricFunction(
            lambda t: axes.c2p(np.cos(t), np.sin(t), 0),
            t_range=[0, 2 * PI],
            color=BLUE,
        )
        theta = ValueTracker(0)

        dot_2d = always_redraw(
            lambda: Dot(axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()), 0), color=YELLOW)
        )
        real_drop = always_redraw(
            lambda: Line(
                axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()), 0),
                axes.c2p(np.cos(theta.get_value()), 0, 0),
                color=RED,
            )
        )
        imag_drop = always_redraw(
            lambda: Line(
                axes.c2p(np.cos(theta.get_value()), np.sin(theta.get_value()), 0),
                axes.c2p(0, np.sin(theta.get_value()), 0),
                color=GREEN,
            )
        )

        title = Text("Complex sine wave and projections", font_size=36)
        title.to_edge(UP)
        re_label = MathTex(r"\Re(z)", font_size=30)
        im_label = MathTex(r"\Im(z)", font_size=30)
        re_label.next_to(axes.c2p(1.5, 0, 0), RIGHT)
        im_label.next_to(axes.c2p(0, 1.5, 0), UP)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(re_label), FadeIn(im_label))
        self.play(Create(circle_2d))
        self.play(FadeIn(dot_2d), FadeIn(real_drop), FadeIn(imag_drop))
        self.play(theta.animate.set_value(2 * PI), run_time=4, rate_func=lambda t: t)
        self.wait(0.5)

        x_label = axes.get_x_axis_label(MathTex(r"\Re(z)", font_size=30))
        y_label = axes.get_y_axis_label(MathTex(r"\Im(z)", font_size=30))
        z_label = axes.get_z_axis_label(MathTex("t", font_size=30))

        z_scale = 0.5
        time_span = 4 * PI

        base_circle = ParametricFunction(
            lambda t: axes.c2p(np.cos(t), np.sin(t), 0),
            t_range=[0, 2 * PI],
            color=BLUE,
            stroke_width=2,
        )
        helix = always_redraw(
            lambda: ParametricFunction(
                lambda u: axes.c2p(np.cos(u), np.sin(u), z_scale * u),
                t_range=[0, theta.get_value()],
                color=YELLOW,
                stroke_width=4,
            )
        )
        dot_3d = always_redraw(
            lambda: Dot3D(
                point=axes.c2p(
                    np.cos(theta.get_value()),
                    np.sin(theta.get_value()),
                    z_scale * theta.get_value(),
                ),
                color=YELLOW,
                radius=0.07,
            )
        )
        real_curve = always_redraw(
            lambda: ParametricFunction(
                lambda u: axes.c2p(np.cos(u), 0, z_scale * u),
                t_range=[0, theta.get_value()],
                color=RED,
                stroke_width=3,
            )
        )
        imag_curve = always_redraw(
            lambda: ParametricFunction(
                lambda u: axes.c2p(0, np.sin(u), z_scale * u),
                t_range=[0, theta.get_value()],
                color=GREEN,
                stroke_width=3,
            )
        )
        real_link = always_redraw(
            lambda: Line(
                dot_3d.get_center(),
                axes.c2p(np.cos(theta.get_value()), 0, z_scale * theta.get_value()),
                color=RED,
                stroke_width=2,
            )
        )
        imag_link = always_redraw(
            lambda: Line(
                dot_3d.get_center(),
                axes.c2p(0, np.sin(theta.get_value()), z_scale * theta.get_value()),
                color=GREEN,
                stroke_width=2,
            )
        )

        self.play(FadeOut(title), run_time=0.2)
        self.play(axes.z_axis.animate.set_opacity(1), FadeIn(z_label), run_time=1.2)
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(FadeIn(x_label), FadeIn(y_label))
        self.play(Create(base_circle))
        self.play(FadeIn(dot_3d), FadeIn(real_link), FadeIn(imag_link))
        self.play(Create(helix), Create(real_curve), Create(imag_curve), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.play(theta.animate.set_value(theta.get_value() + time_span), run_time=8, rate_func=lambda t: t)
        self.wait(1)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
