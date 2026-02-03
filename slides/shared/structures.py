"""
Reusable structures for S4F and Standpoint Logic slides.
"""

from manim import *
from slides.shared.wrappers import MathTexWrapper
from slides.shared.common import FONT_SIZE_TEXT

# Custom colors
LIGHT_BLUE = "#ADD8E6"


def labeled_dot(point, label=None, direction=RIGHT, font_size=FONT_SIZE_TEXT, show_label=True, dot_radius=0.03):
    """Create a dot (world) at a given point, optionally with a label."""
    dot = Dot(point=point, radius=dot_radius, color=BLACK)
    if show_label and label:
        tex = MathTexWrapper(label, font_size=font_size).next_to(dot, direction, buff=0.05)
        return VGroup(dot, tex)
    return VGroup(dot)


class S4FStructure(VGroup):
    """
    S4F structure: Single standpoint with inner ellipse (core) and outer ellipse (field).

    The outer ellipse represents the "field of focus" W_f,
    the inner ellipse represents the "core worlds" W_s.

    Includes worlds positioned inside the ellipses.
    """
    # Base dimensions (at scale=1.0)
    BASE_INNER_SIZE = (1.0, 1.2)
    BASE_OUTER_SIZE = (1.1, 1.8)
    BASE_INNER_OFFSET = [0.27, -0.175, 0]
    BASE_FONT_SIZE = 20
    BASE_DOT_RADIUS = 0.03

    def __init__(
        self,
        color=LIGHT_GRAY,
        rotation=-30,
        inner_opacity=1,
        outer_opacity=0.55,
        stroke_width=1.5,
        scale_factor=1.5,
        show_world_labels=True,
        dot_scale=1.0,  # multiplier for dot radius (e.g., 2.0 = double thickness)
        **kwargs
    ):
        super().__init__(**kwargs)

        self.color = color
        self._scale_factor = scale_factor
        self._show_world_labels = show_world_labels

        # Scale dimensions
        s = scale_factor
        inner_size = (self.BASE_INNER_SIZE[0] * s, self.BASE_INNER_SIZE[1] * s)
        outer_size = (self.BASE_OUTER_SIZE[0] * s, self.BASE_OUTER_SIZE[1] * s)
        inner_offset = [x * s for x in self.BASE_INNER_OFFSET]
        font_size = self.BASE_FONT_SIZE * s
        dot_radius = self.BASE_DOT_RADIUS * s * dot_scale

        # Outer ellipse (field of focus W_f)
        self.outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=outer_opacity, color=BLACK, fill_color=color, stroke_width=stroke_width
        ).rotate(rotation * DEGREES)

        # Inner ellipse (core worlds W_s)
        self.inner = Ellipse(
            height=inner_size[0], width=inner_size[1],
            fill_opacity=inner_opacity, color=BLACK, fill_color=color, stroke_width=stroke_width
        ).rotate(rotation * DEGREES).shift(inner_offset)

        # Create worlds relative to ellipse positions
        self._create_worlds(inner_offset, font_size, dot_radius)

        # Create label
        # self.label = MathTexWrapper(r'\spform{S}', font_size=font_size)
        # self.label.next_to(self.outer, UP, buff=0.1 * s)

        # Add ellipses and worlds to VGroup so they transform together
        self.add(self.outer, self.inner, self.all_worlds)

    def _create_worlds(self, inner_offset, font_size, dot_radius):
        """Create worlds positioned relative to the ellipses."""
        s = self._scale_factor
        show = self._show_world_labels

        # Inner worlds (inside inner ellipse)
        self.inner_worlds = VGroup(
            labeled_dot([inner_offset[0] - 0.2*s, inner_offset[1] + 0.15*s, 0], r"\pi_1", RIGHT, font_size, show, dot_radius),
            labeled_dot([inner_offset[0] + 0.1*s, inner_offset[1] - 0.1*s, 0], r"\pi_2", RIGHT, font_size, show, dot_radius),
            labeled_dot([inner_offset[0] - 0.1*s, inner_offset[1] - 0.3*s, 0], r"\pi_3", RIGHT, font_size, show, dot_radius),
        )
        # Outer-only worlds (between inner and outer ellipse)
        self.outer_worlds = VGroup(
            labeled_dot([-0.5*s, 0.3*s, 0], r"\pi_4", RIGHT, font_size, show, dot_radius),
            labeled_dot([-0.6*s, -0.05*s, 0], r"\pi_5", RIGHT, font_size, show, dot_radius),
        )
        self.all_worlds = VGroup(*self.inner_worlds, *self.outer_worlds)


class StandpointStructure(VGroup):
    """
    Standpoint Logic structure: Two overlapping standpoint ellipses.

    Each standpoint has its own ellipse. They may overlap to show shared worlds.
    No outer "field" ellipses - just the standpoint regions.
    """
    # Base dimensions (at scale=1.0)
    BASE_ELLIPSE_SIZE = (1.0, 1.2)
    BASE_S1_POSITION = [-0.3, 0, 0]
    BASE_S2_POSITION = [0.3, 0, 0]
    BASE_FONT_SIZE = 20
    BASE_DOT_RADIUS = 0.03

    def __init__(
        self,
        s1_color=BLUE,
        s2_color=RED,
        s1_rotation=-30,
        s2_rotation=30,
        opacity=0.6,
        stroke_width=1.5,
        scale_factor=1.5,
        show_world_labels=True,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.s1_color = s1_color
        self.s2_color = s2_color
        self._scale_factor = scale_factor
        self._show_world_labels = show_world_labels

        # Scale dimensions
        s = scale_factor
        ellipse_size = (self.BASE_ELLIPSE_SIZE[0] * s, self.BASE_ELLIPSE_SIZE[1] * s)
        s1_position = [x * s for x in self.BASE_S1_POSITION]
        s2_position = [x * s for x in self.BASE_S2_POSITION]
        font_size = self.BASE_FONT_SIZE * s
        dot_radius = self.BASE_DOT_RADIUS * s

        # S1 ellipse
        self.s1 = Ellipse(
            height=ellipse_size[0], width=ellipse_size[1],
            fill_opacity=opacity, color=BLACK, fill_color=s1_color, stroke_width=stroke_width
        ).rotate(s1_rotation * DEGREES).shift(s1_position)

        # S1 white mask (for layering when both shown)
        self.s1_mask = Ellipse(
            height=ellipse_size[0], width=ellipse_size[1],
            fill_opacity=1.0, color=WHITE, fill_color=WHITE, stroke_width=0
        ).rotate(s1_rotation * DEGREES).shift(s1_position)

        # S2 ellipse
        self.s2 = Ellipse(
            height=ellipse_size[0], width=ellipse_size[1],
            fill_opacity=opacity, color=BLACK, fill_color=s2_color, stroke_width=stroke_width
        ).rotate(s2_rotation * DEGREES).shift(s2_position)

        # S2 white mask
        self.s2_mask = Ellipse(
            height=ellipse_size[0], width=ellipse_size[1],
            fill_opacity=1.0, color=WHITE, fill_color=WHITE, stroke_width=0
        ).rotate(s2_rotation * DEGREES).shift(s2_position)

        # Create worlds relative to ellipse positions
        self._create_worlds(s1_position, s2_position, font_size, dot_radius)

        # Create labels
        self.s1_label = MathTexWrapper(r'\spform{S1}', font_size=font_size)
        self.s1_label.move_to(self.s1.get_top()).shift(DOWN * 0.15 * s)
        self.s2_label = MathTexWrapper(r'\spform{S2}', font_size=font_size)
        self.s2_label.move_to(self.s2.get_top()).shift(DOWN * 0.15 * s)

        # Add ellipses, worlds, and labels to group so they transform together
        self.add(self.s1_mask, self.s2_mask, self.s1, self.s2, self.all_worlds, self.s1_label, self.s2_label)

    def _create_worlds(self, s1_pos, s2_pos, font_size, dot_radius):
        """Create worlds positioned relative to the ellipses."""
        s = self._scale_factor
        show = self._show_world_labels
        s1_pos = np.array(s1_pos)
        s2_pos = np.array(s2_pos)

        # S1 exclusive worlds
        self.s1_worlds = VGroup(
            labeled_dot(s1_pos + [-0.45*s, 0.15*s, 0], r"\pi_1", RIGHT, font_size, show, dot_radius),
            labeled_dot(s1_pos + [-0.35*s, -0.15*s, 0], r"\pi_2", RIGHT, font_size, show, dot_radius),
        )
        # Shared worlds (in overlap region)
        center = (s1_pos + s2_pos) / 2
        self.shared_worlds = VGroup(
            labeled_dot(center + [-0.1*s, -0.05*s, 0], r"\pi_3", RIGHT, font_size, show, dot_radius),
        )
        # S2 exclusive worlds
        self.s2_worlds = VGroup(
            labeled_dot(s2_pos + [0.2*s, 0.15*s, 0], r"\pi_6", RIGHT, font_size, show, dot_radius),
            labeled_dot(s2_pos + [0.15*s, -0.15*s, 0], r"\pi_7", RIGHT, font_size, show, dot_radius),
        )
        self.all_worlds = VGroup(*self.s1_worlds, *self.shared_worlds, *self.s2_worlds)


class S4FSStructure(VGroup):
    """
    S4FS structure: Two standpoints, each with inner + outer ellipse.

    Combines S4F (field of focus) with multiple standpoints.
    Each standpoint has a core (inner) and field (outer) region.
    """
    def __init__(
        self,
        s1_color=BLUE,
        s2_color=RED,
        s1_rotation=-30,
        s2_rotation=30,
        s1_inner_pos=[0.25, -0.15, 0],
        s1_outer_pos=[0, 0, 0],
        s2_inner_pos=[0.85, -0.15, 0],
        s2_outer_pos=[1.1, -0.025, 0],
        inner_opacity=0.6,
        outer_opacity=0.3,
        stroke_width=1.5,
        inner_size=(1.0, 1.2),
        outer_size=(1.1, 1.8),
        **kwargs
    ):
        super().__init__(**kwargs)

        # S1 outer (field)
        self.s1_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=outer_opacity, color=BLACK, fill_color=s1_color, stroke_width=stroke_width
        ).rotate(s1_rotation * DEGREES).shift(s1_outer_pos)

        # S1 middle mask
        self.s1_middle = Ellipse(
            height=inner_size[0], width=inner_size[1],
            fill_opacity=1.0, color=WHITE, fill_color=WHITE, stroke_width=0
        ).rotate(s1_rotation * DEGREES).shift(s1_inner_pos)

        # S1 inner (core)
        self.s1_inner = Ellipse(
            height=inner_size[0], width=inner_size[1],
            fill_opacity=inner_opacity, color=BLACK, fill_color=s1_color, stroke_width=stroke_width
        ).rotate(s1_rotation * DEGREES).shift(s1_inner_pos)

        # S2 outer (field)
        self.s2_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=outer_opacity, color=BLACK, fill_color=s2_color, stroke_width=stroke_width
        ).rotate(s2_rotation * DEGREES).shift(s2_outer_pos)

        # S2 middle mask
        self.s2_middle = Ellipse(
            height=inner_size[0], width=inner_size[1],
            fill_opacity=1.0, color=WHITE, fill_color=WHITE, stroke_width=0
        ).rotate(s2_rotation * DEGREES).shift(s2_inner_pos)

        # S2 inner (core)
        self.s2_inner = Ellipse(
            height=inner_size[0], width=inner_size[1],
            fill_opacity=inner_opacity, color=BLACK, fill_color=s2_color, stroke_width=stroke_width
        ).rotate(s2_rotation * DEGREES).shift(s2_inner_pos)

        # Create worlds
        self._create_worlds(s1_inner_pos, s1_outer_pos, s2_inner_pos, s2_outer_pos)

        # Create labels
        self.s1_label = MathTexWrapper(r'\spform{S1}', font_size=FONT_SIZE_TEXT)
        self.s1_label.next_to(self.s1_inner, UP, buff=0.1)
        self.s1_label_outer = MathTexWrapper(r'\spform{S1}', font_size=FONT_SIZE_TEXT)
        self.s1_label_outer.next_to(self.s1_outer, UP + LEFT, buff=0.05)
        self.s2_label = MathTexWrapper(r'\spform{S2}', font_size=FONT_SIZE_TEXT)
        self.s2_label.next_to(self.s2_inner, UP, buff=0.1)
        self.s2_label_outer = MathTexWrapper(r'\spform{S2}', font_size=FONT_SIZE_TEXT)
        self.s2_label_outer.next_to(self.s2_outer, UP + RIGHT, buff=0.05)

        # Add ellipses, worlds, and labels so they transform together
        self.add(
            self.s1_outer, self.s2_outer,
            self.s1_middle, self.s2_middle,
            self.s1_inner, self.s2_inner,
            self.all_worlds,
            self.s1_label, self.s1_label_outer,
            self.s2_label, self.s2_label_outer
        )

    def _create_worlds(self, s1_inner, s1_outer, s2_inner, s2_outer):
        """Create worlds positioned relative to the ellipses."""
        s1_inner = np.array(s1_inner)
        s2_inner = np.array(s2_inner)

        # S1 inner worlds
        self.s1_inner_worlds = VGroup(
            labeled_dot(s1_inner + [-0.2, 0.2, 0], r"\pi_1", RIGHT),
            labeled_dot(s1_inner + [-0.15, -0.1, 0], r"\pi_2", RIGHT),
        )
        # Shared/center world
        center = (s1_inner + s2_inner) / 2
        self.shared_worlds = VGroup(
            labeled_dot(center + [0, 0.15, 0], r"\pi_3", RIGHT),
        )
        # S1 outer-only worlds
        self.s1_outer_worlds = VGroup(
            labeled_dot(s1_inner + [-0.55, 0.35, 0], r"\pi_4", RIGHT),
            labeled_dot(s1_inner + [-0.6, 0.05, 0], r"\pi_5", RIGHT),
        )
        # S2 inner worlds
        self.s2_inner_worlds = VGroup(
            labeled_dot(s2_inner + [0.15, 0.2, 0], r"\pi_6", RIGHT),
            labeled_dot(s2_inner + [0.1, -0.1, 0], r"\pi_7", RIGHT),
        )
        # S2 outer-only worlds
        self.s2_outer_worlds = VGroup(
            labeled_dot(s2_inner + [0.45, 0.25, 0], r"\pi_8", RIGHT),
        )

        self.all_worlds = VGroup(
            *self.s1_inner_worlds, *self.shared_worlds, *self.s1_outer_worlds,
            *self.s2_inner_worlds, *self.s2_outer_worlds
        )
