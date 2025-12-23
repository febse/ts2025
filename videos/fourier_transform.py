from manim import (
	Scene,
	ComplexPlane,
	Arrow,
	VGroup,
	MathTex,
	Tex,
	FadeIn,
	Write,
	BLUE,
	GREEN,
	YELLOW,
	DOWN,
)
import numpy as np


class ComplexDotProduct(Scene):
	"""
	Show two vectors in the complex plane and their complex (Hermitian) dot product
	as another vector: <z1, z2> = conj(z1) * z2.
	"""

	def construct(self):
		# Complex plane setup
		plane = ComplexPlane(
			x_range=[-4, 4, 1],
			y_range=[-3, 3, 1],
			background_line_style={"stroke_opacity": 0.4},
		).add_coordinates()
		self.play(FadeIn(plane))

		# Define two complex numbers (vectors)
		z1 = 1.5 + 1j * 1.0
		z2 = -0.5 + 1j * 1.8

		# Arrows for z1 and z2
		arrow_z1 = Arrow(plane.n2p(0), plane.n2p(z1), color=BLUE, buff=0)
		arrow_z2 = Arrow(plane.n2p(0), plane.n2p(z2), color=GREEN, buff=0)

		# Labels near arrow tips
		label_z1 = MathTex(r"z_1").scale(0.8).next_to(arrow_z1.get_end(), direction=(0.4, 0.4, 0))
		label_z2 = MathTex(r"z_2").scale(0.8).next_to(arrow_z2.get_end(), direction=(0.4, 0.4, 0))

		self.play(FadeIn(VGroup(arrow_z1, arrow_z2)))
		self.play(Write(VGroup(label_z1, label_z2)))

		# Compute Hermitian inner product: <z1, z2> = conj(z1) * z2
		inner = np.conjugate(z1) * z2

		# Arrow representing the complex dot product
		arrow_inner = Arrow(plane.n2p(0), plane.n2p(inner), color=YELLOW, buff=0)
		label_inner = MathTex(r"\langle z_1, z_2 \rangle").scale(0.8).next_to(
			arrow_inner.get_end(), direction=(0.4, 0.4, 0)
		)

		# Text showing the numeric value
		inner_text = Tex(
			rf"$\overline{{z_1}}\,z_2 = {inner.real:.2f} + {inner.imag:.2f}i$"
		).scale(0.6)
		inner_text.to_edge(
			DOWN
		)  # Place the numeric value at the bottom for readability

		self.play(FadeIn(arrow_inner))
		self.play(Write(label_inner))
		self.play(Write(inner_text))

		# Keep the final frame for a moment
		self.wait(2)

