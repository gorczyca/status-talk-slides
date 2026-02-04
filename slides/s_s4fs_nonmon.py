from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper, latex_block
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot
from slides.shared.colors import BRILLIANT_BLUE

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 1


class SS4fsNonmon(BaseSlide):
    TITLE = r'S4F Standpoint: Non-Monotonicity'

    def create_content(self):
        s = self.slide

        # --- Left S4F-standpoint structure (with one outer world per standpoint) ---
        standp_left = StandpointStructure(
            scale_factor=1.2,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).to_corner(UL, buff=1).shift(DOWN * 0.8)

        sf_left = standp_left._scale_factor
        outer_size_left = (
            S4FStructure.BASE_OUTER_SIZE[0] * sf_left,
            S4FStructure.BASE_OUTER_SIZE[1] * sf_left
        )
        inner_to_outer_offset_left = [-x * sf_left
                                      for x in S4FStructure.BASE_INNER_OFFSET]

        s1_outer_left = Ellipse(
            height=outer_size_left[0], width=outer_size_left[1],
            fill_opacity=0.35, color=BLACK, fill_color=BLUE, stroke_width=1.5
        ).rotate(-30 * DEGREES).move_to(standp_left.s1.get_center()).shift(
            inner_to_outer_offset_left).set_z_index(0)

        s2_outer_offset_left = [-inner_to_outer_offset_left[0],
                                inner_to_outer_offset_left[1], 0]
        s2_outer_left = Ellipse(
            height=outer_size_left[0], width=outer_size_left[1],
            fill_opacity=0.35, color=BLACK, fill_color=RED, stroke_width=1.5
        ).rotate(30 * DEGREES).move_to(standp_left.s2.get_center()).shift(
            s2_outer_offset_left).set_z_index(0)

        standp_left.set_z_index(1)
        font_size_left = S4FStructure.BASE_FONT_SIZE * sf_left
        dot_radius_left = S4FStructure.BASE_DOT_RADIUS * sf_left

        s1_center_left = standp_left.s1.get_center()
        s2_center_left = standp_left.s2.get_center()

        # One outer world for each standpoint (left structure)
        s1_outer_world_left = labeled_dot(
            s1_center_left + [-0.9*sf_left, 0.6*sf_left, 0],
            r"\pi_8", RIGHT, font_size_left, True, dot_radius_left
        )
        # Keep outer worlds as solid black dots (same style as inner worlds)
        s1_outer_world_left[0].set_fill(BLACK, opacity=1.0).set_stroke(BLACK, width=1.2)

        s2_outer_world_left = labeled_dot(
            s2_center_left + [0.75*sf_left, 0.5*sf_left, 0],
            r"\pi_9", RIGHT, font_size_left, True, dot_radius_left
        )
        s2_outer_world_left[0].set_fill(BLACK, opacity=1.0).set_stroke(BLACK, width=1.2)

        # --- Right S4F-standpoint structure (empty outer worlds) ---
        standp_right = StandpointStructure(
            scale_factor=1.2,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).next_to(standp_left, RIGHT, buff=2.2, aligned_edge=UP)

        sf_right = standp_right._scale_factor
        outer_size_right = (
            S4FStructure.BASE_OUTER_SIZE[0] * sf_right,
            S4FStructure.BASE_OUTER_SIZE[1] * sf_right
        )
        inner_to_outer_offset_right = [-x * sf_right
                                       for x in S4FStructure.BASE_INNER_OFFSET]

        s1_outer_right = Ellipse(
            height=outer_size_right[0], width=outer_size_right[1],
            fill_opacity=0.35, color=BLACK, fill_color=BLUE, stroke_width=1.5
        ).rotate(-30 * DEGREES).move_to(standp_right.s1.get_center()).shift(
            inner_to_outer_offset_right).set_z_index(0)

        s2_outer_offset_right = [-inner_to_outer_offset_right[0],
                                 inner_to_outer_offset_right[1], 0]
        s2_outer_right = Ellipse(
            height=outer_size_right[0], width=outer_size_right[1],
            fill_opacity=0.35, color=BLACK, fill_color=RED, stroke_width=1.5
        ).rotate(30 * DEGREES).move_to(standp_right.s2.get_center()).shift(
            s2_outer_offset_right).set_z_index(0)

        standp_right.set_z_index(1)

        # --- Preference relation symbol ---
        pref_symbol = MathTexWrapper(
            r'\triangleleft',
            font_size=56
        ).move_to((standp_left.get_center() + standp_right.get_center()) / 2)

        # --- Add to slide ---
        s.add(standp_left, s1_outer_left, s2_outer_left,
              s1_outer_world_left, s2_outer_world_left)
        s.add(standp_right, s1_outer_right, s2_outer_right)
        s.add(pref_symbol)
        s.wait()
        s.next_slide()

        minimal_label = TexWrapper(
            r"\textbf{Minimal model:}",
            font_size=24
        ).next_to(standp_left, DOWN, buff=0.35, aligned_edge=LEFT).shift(LEFT * 0.6)

        # Partition of modal subformulas (placed below the structures)
        partition_text = TexWrapper(
            r"Represent $\sffsstruct$ by a partition $(\Phi,\Psi)$ of $\{\standbs\phi \mid \standbs\phi \in \mathit{Subf}(T)\}$,",
            font_size=24
        ).next_to(minimal_label, DOWN, buff=0.25, aligned_edge=LEFT)

        adapt_text = TexWrapper(
            r"then adapt the Schwarz \& Truszczynski (1993) procedure.",
            font_size=24
        ).next_to(partition_text, DOWN, buff=0.1, aligned_edge=LEFT)

        complexity_block = latex_block(
            r"``\textsc{Does $T\subseteq \langss$ have a minimal model}?'' is $\Sigma^P_2$-complete.",
            color=BRILLIANT_BLUE,
            body_font_size=20
        ).next_to(adapt_text, DOWN, buff=0.5, aligned_edge=LEFT)

        # Reveal textual content: header + partition + adaptation together, then complexity box
        s.add(minimal_label, partition_text, adapt_text)
        s.wait()
        s.next_slide()

        s.add(complexity_block)
        s.wait()

        # === Default theories (copied from motivation slide, bottom-right) ===
        defaults_font_size = 20
        formula_1_s = MathTexWrapper(r'\standb{\snih}\Bigg[', r'\default{\atoma\land\atomb}{\atomx}{\atomp}', r'\Bigg]', font_size=defaults_font_size)
        formula_2_s = MathTexWrapper(r'\standb{\srot}\Bigg[', r'\default{(\atoma\land\atomb)\lor(\atoma\land\atomc)\lor(\atomb\land\atomc)}{\atomx}{\atomp}', r'\Bigg]', font_size=defaults_font_size).next_to(formula_1_s, DOWN, aligned_edge=LEFT)
        formula_3_s = MathTexWrapper(r'\standb{\saes}\Bigg[', r'\default{\atoma\land(\atomb\lor\atomc)}{\atomy}{\atomp}', r'\Bigg]', font_size=defaults_font_size).next_to(formula_2_s, DOWN, aligned_edge=LEFT)
        a_c = MathTexWrapper(r'\atoma\land\atomc', font_size=defaults_font_size).next_to(formula_3_s, DOWN, aligned_edge=LEFT)
        neg_y = MathTexWrapper(r'\neg\atomy', font_size=defaults_font_size)

        group_1 = VGroup(formula_1_s, formula_2_s, formula_3_s, a_c).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        group_1.to_edge(RIGHT, buff=0.8).align_to(standp_left, UP).shift(LEFT * 1.5)
        neg_y.next_to(a_c, DOWN, aligned_edge=LEFT, buff=0.15)

        s.add(formula_1_s, formula_2_s, formula_3_s, a_c)

        brace_5 = Brace(group_1, direction=RIGHT, buff=0.2, color=BLACK)
        brace_5_conclusion = MathTexWrapper(r'\models', r'\big\{', r'\standb{\srot}\atomp,', r'\standb{\saes}\atomp',   r'\big\}', font_size=defaults_font_size)
        brace_6_conclusion = brace_5_conclusion.copy()
        brace_5.put_at_tip(brace_5_conclusion)
        s.wait()
        s.next_slide()
        s.play(GrowFromCenter(brace_5))
        s.wait()
        s.next_slide()
        s.play(FadeIn(brace_5_conclusion))

        group_1.add(neg_y)
        brace_6 = Brace(group_1, direction=RIGHT, buff=0.2, color=BLACK)
        brace_6.put_at_tip(brace_6_conclusion)
        s.wait()
        s.next_slide()
        s.play(
            FadeIn(neg_y),
            Transform(brace_5, brace_6),
            Transform(brace_5_conclusion, brace_6_conclusion)
        )

        saes_cross = Cross(brace_5_conclusion[3], color=RED, stroke_width=3).scale(1.05)
        s.wait()
        s.next_slide()
        s.play(FadeIn(saes_cross))

        # --- Additional results summary (bottom) ---
        add_title = TexWrapper(
            r"\textbf{Additional results:}",
            font_size=24
        )
        add_items = VGroup(
            TexWrapper(r"$\bullet$ Credulous and sceptical reasoning", font_size=22),
            TexWrapper(r"$\bullet$ Expansions", font_size=22),
            TexWrapper(r"$\bullet$ Disjunctive ASP implementation", font_size=22),
        ).arrange(RIGHT, buff=1.5, aligned_edge=DOWN)

        add_items.next_to(complexity_block, DOWN, buff=1, aligned_edge=LEFT)
        add_title.next_to(add_items, UP, buff=0.2, aligned_edge=LEFT)

        # reveal header then bullets
        s.add(add_title)
        # s.wait()
        # s.next_slide()
        for item in add_items:
            s.wait()
            s.next_slide()
            s.add(item)


class SS4fsNonmonScene(Slide):
    def construct(self):
        SS4fsNonmon(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
