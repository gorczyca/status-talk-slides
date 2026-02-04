from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 1


class SS4fsSyntax(BaseSlide):
    TITLE = r'S4F Standpoint: Syntax \& Semantics'

    def create_content(self):
        s = self.slide

        # (Removed) main center-right Standpoint structure and its mini S4Fs
        # The slide now uses only the static S4F-Standpoint figure in the bottom-right.

        # === Language and definitions (left side) ===
        intro = TexWrapper(
            r"Language $\mathcal{L}^{\preceq}_{\mathcal{S}}$:",
            font_size=FONT_SIZE_TEXT
        ).to_edge(LEFT, buff=1).shift(UP * 2)

        grammar = MathTexWrapper(
            r"\varphi ::= s \preceq u \mid \psi \text{ where } \psi ::= p \mid \neg\psi \mid \psi_1 \land \psi_2 \mid \standbs \psi",
            font_size=FONT_SIZE_TEXT
        ).next_to(intro, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 0.2)

        default_rule_initial = MathTexWrapper(
            r"\default{\phi}{\psi'}{\psi}", r"\leadsto", r"(", r"\know", r"\phi", r"\land", r"\know", r"\neg", r"\know", r"\neg", r"\psi'", r")", r"\limplies", r"\know", r"\psi",
            font_size=FONT_SIZE_TEXT
        ).next_to(grammar, DOWN, buff=0.5, aligned_edge=LEFT)

        default_rule_with_modalities = MathTexWrapper(
            r"\standbs", r"\left[", r"\default{\phi}{\psi'}{\psi}", r"\right]", r"\leadsto", r"(", r"\standbs", r"\phi", r"\land", r"\standbs", r"\neg", r"\standbs", r"\neg", r"\psi'", r")", r"\limplies", r"\standbs", r"\psi",
            font_size=FONT_SIZE_TEXT
        ).next_to(grammar, DOWN, buff=0.5, aligned_edge=LEFT)

        # Semantics at the bottom (standpoint modality and ordering)
        sem_order = MathTexWrapper(
            r"\sffsstruct, \pi \modelfor s \preceq u \quad :\Longleftrightarrow \quad \sigma(s) \subseteq \sigma(u) \text{ and } \tau(s) \subseteq \tau(u)",
            font_size=FONT_SIZE_TEXT
        ).to_edge(DOWN, buff=0.65).to_edge(LEFT, buff=1).shift(UP*.75)

        sem_box = MathTexWrapper(
            r"\sffsstruct, \pi \modelfor \standbs\psi \quad :\Longleftrightarrow \quad \begin{cases} \sffsstruct, \pi' \modelfor \psi \text{ for all } \pi' \in \sigma(s) \cup \tau(s) & \text{if } \pi \in \tau(\ast) \\ \sffsstruct, \pi' \modelfor \psi \text{ for all } \pi' \in \sigma(s) & \text{otherwise} \end{cases}",
            font_size=FONT_SIZE_TEXT
        ).next_to(sem_order, UP, buff=0.25, aligned_edge=LEFT)

        # === Static S4F Standpoint figure (center-right, same as removed) ===
        s4f_standp = StandpointStructure(
            scale_factor=1.425,  # match previous small appearance (1.5 * 0.95)
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).to_edge(RIGHT, buff=1).shift(UP * 1+LEFT*0.3)

        # Create outer ellipses behind each standpoint to make it an "S4F Standpoint" (final static look)
        sf = s4f_standp._scale_factor
        outer_size = (
            S4FStructure.BASE_OUTER_SIZE[0] * sf, S4FStructure.BASE_OUTER_SIZE[1] * sf)
        inner_to_outer_offset = [-x * sf for x in S4FStructure.BASE_INNER_OFFSET]

        s1_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=0.35, color=BLACK, fill_color=BLUE, stroke_width=1.5
        ).rotate(-30 * DEGREES).move_to(s4f_standp.s1.get_center()).shift(inner_to_outer_offset).set_z_index(-1)

        s2_outer_offset = [-inner_to_outer_offset[0], inner_to_outer_offset[1], 0]
        s2_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=0.35, color=BLACK, fill_color=RED, stroke_width=1.5
        ).rotate(30 * DEGREES).move_to(s4f_standp.s2.get_center()).shift(s2_outer_offset).set_z_index(-1)

        s4f_standp.set_z_index(1)

        font_size = S4FStructure.BASE_FONT_SIZE * sf
        dot_radius = S4FStructure.BASE_DOT_RADIUS * sf

        s1_center = s4f_standp.s1.get_center()
        s1_outer_worlds = VGroup(
            labeled_dot(s1_center + [-0.9*sf, 0.6*sf, 0], r"\pi_4", RIGHT, font_size, True, dot_radius),
            labeled_dot(s1_center + [-0.85*sf, 0.3*sf, 0], r"\pi_5", RIGHT, font_size, True, dot_radius),
        )

        s2_center = s4f_standp.s2.get_center()
        s2_outer_worlds = VGroup(
            labeled_dot(s2_center + [0.75*sf, 0.5*sf, 0], r"\pi_8", RIGHT, font_size, True, dot_radius),
            labeled_dot(s2_center + [0.65*sf, 0.15*sf, 0], r"\pi_9", RIGHT, font_size, True, dot_radius),
        )
        # === Add content to slide with the same step structure as `s_ss4f_syntax.py` ===
        # 1. Add language header + static S4F figure (bottom-right)
        s.add(intro, grammar)
        # static S4F figure
        s.add(s4f_standp, s1_outer, s2_outer, s1_outer_worlds, s2_outer_worlds)
        s.wait()
        s.next_slide()

        # 3. Add default rule initial
        s.add(default_rule_initial)
        s.wait()
        s.next_slide()

        # 4. Transform to add standpoint modalities
        s.play(TransformMatchingTex(default_rule_initial, default_rule_with_modalities))
        s.wait()
        s.next_slide()

        # 5. Add semantics
        s.add(sem_box, sem_order)
        s.wait()

class SS4fsSyntaxScene(Slide):
    def construct(self):
        SS4fsSyntax(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
