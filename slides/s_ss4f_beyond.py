from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper, latex_block
from slides.shared.colors import BRILLIANT_BLUE
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 15


class SS4fBeyond(BaseSlide):
    TITLE = r'Standpoint S4F: Beyond Simple Theories'

    def create_content(self):
        s = self.slide

        # Left side content
        # Problem section (top left)
        problem_title = TexWrapper(
            r"\textbf{Beyond ``atomic'' standpoint modalities:}",
            font_size=24
        ).to_corner(UL, buff=1).shift(DOWN * 0.5)

        problem_formula = MathTexWrapper(
            r"\{\standb{\sts} \know a \lor \neg\standb{\sts} \know a\} \mathrel{\mid\mkern-3mu\approx}_{\text{cred}} \standb{\sts} \know a",
            font_size=24
        ).next_to(problem_title, DOWN, buff=0.3, aligned_edge=LEFT)

        # Unrestricted syntax section
        unrest_syn_title = TexWrapper(
            r"\textbf{Unrestricted syntax} $\langk^\Box$:",
            font_size=24
        ).next_to(problem_formula, DOWN, buff=0.5, aligned_edge=LEFT)

        # Syntax formula
        syn_grammar = MathTexWrapper(
            r"\varphi ::= a \mid \neg\varphi \mid \varphi \land \varphi \mid \know\varphi \mid \standbs\varphi",
            font_size=24
        ).next_to(unrest_syn_title, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 0.3)

        # Two standpoint structures with preference (below syntax, on left side)
        # Left structure: with one outer world in some nested S4F structures
        standp_left = StandpointStructure(
            scale_factor=1.4,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).next_to(syn_grammar, DOWN, buff=0.5).shift(LEFT * 1)

        # Get all worlds from left standpoint
        all_worlds_left = list(standp_left.s1_worlds) + \
            list(standp_left.shared_worlds) + list(standp_left.s2_worlds)

        # Create mini S4F structures at each world position (with one outer world visible)
        mini_s4fs_left = []
        for idx, world in enumerate(all_worlds_left):
            mini_s4f = S4FStructure(
                scale_factor=0.3,
                show_world_labels=False,
                dot_scale=3
            )
            mini_s4f.move_to(world.get_center())
            # Show one outer world in first (S1) and last (S2) worlds only
            if idx == 0 or idx == len(all_worlds_left) - 1:
                mini_s4f.outer_worlds[1].set_opacity(0)  # Hide second outer world, keep first
            else:
                for w in mini_s4f.outer_worlds:
                    w.set_opacity(0)  # Hide all outer worlds
            mini_s4fs_left.append(mini_s4f)

        # Right structure: no outer worlds at all
        standp_right = StandpointStructure(
            scale_factor=1.4,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).next_to(standp_left, RIGHT, buff=1.5)

        # Get all worlds from right standpoint
        all_worlds_right = list(standp_right.s1_worlds) + \
            list(standp_right.shared_worlds) + list(standp_right.s2_worlds)

        # Create mini S4F structures without outer worlds
        mini_s4fs_right = []
        for world in all_worlds_right:
            mini_s4f = S4FStructure(
                scale_factor=0.3,
                show_world_labels=False,
                dot_scale=3
            )
            mini_s4f.move_to(world.get_center())
            # Hide all outer worlds
            for w in mini_s4f.outer_worlds:
                w.set_opacity(0)
            mini_s4fs_right.append(mini_s4f)

        # Preference symbol between structures
        pref_symbol = MathTexWrapper(
            r'\triangleleft',
            font_size=56
        ).move_to((standp_left.get_center() + standp_right.get_center()) / 2)

        # Hardness result (below structures on left side)
        hardness_result = latex_block(
            r"``\textsc{Does  $T\subseteq \langk^\Box$ have a minimal model}?'' is $\Sigma^P_3$-hard.",
            color=BRILLIANT_BLUE,
            body_font_size=20
        ).next_to(standp_left, DOWN, buff=0.5, aligned_edge=LEFT)

        # QBF translation (right side, all in blue)
        qbf_title = TexWrapper(
            r"QBF formula:",
            font_size=24,
            color=BRILLIANT_BLUE
        ).to_corner(UR, buff=1).shift(DOWN * 1.5 + LEFT * 4)

        qbf_formula = MathTexWrapper(
            r"\Phi := \exists s_1,\ldots,s_m\forall p_1,\ldots,p_n\exists r_1,\ldots,r_l\Psi",
            font_size=20,
            color=BRILLIANT_BLUE
        ).to_corner(UR, buff=1).shift(DOWN * 1.5 + LEFT * 2)

        # trans_text = TexWrapper(
        #     r"where $\Psi$ is a general, quantifier-free formula. The translation $trans(\Phi)$ into an $\mathbb{S}$S4F formula is given by:",
        #     font_size=20,
        #     color=BRILLIANT_BLUE
        # ).next_to(qbf_formula, DOWN, buff=0.3, aligned_edge=LEFT)

        # Translation formulas
        trans_formulas = MathTexWrapper(
            r"\begin{aligned}"
            r"trans(\Phi) :=&\ (\mathbf{K}p_1 \lor \mathbf{K}\neg p_1) \land \ldots \land (\mathbf{K}p_1 \lor \mathbf{K}\neg p_n)) & \land\ (4.1) \\"
            r"&\ (\neg((p_1 \leftrightarrow \Box_* q_1) \land \ldots \land (p_n \leftrightarrow \Box_* q_n)) \lor (p_1 \land \ldots \land p_n)) & \land\ (4.2) \\"
            r"&\ (\mathbf{MK}q_1 \land \ldots \land \mathbf{MK}q_n) & \land\ (4.3) \\"
            r"&\ ((\Box_* s_1 \lor \Box_* \neg s_1) \land \ldots \land (\Box_* s_m \lor \Box_* \neg s_m)) & \land\ (4.4) \\"
            r"&\ ((\mathbf{K}r_1 \lor \mathbf{K}\neg r_1) \land \ldots \land (\mathbf{K}r_l \lor \mathbf{K}\neg r_l)) & \land\ (4.5) \\"
            r"&\ \Diamond_*(p_1 \land \ldots \land p_n) & \land\ (4.6) \\"
            r"&\ \Psi & (4.7)"
            r"\end{aligned}",
            font_size=18,
            color=BRILLIANT_BLUE
        ).next_to(qbf_formula, DOWN, buff=0.3, aligned_edge=LEFT)

        # Add all elements
        # 1. Problem statement
        s.add(problem_title, problem_formula)
        s.wait()
        s.next_slide()

        # 2. Unrestricted syntax
        s.add(unrest_syn_title, syn_grammar)
        s.wait()
        s.next_slide()

        # 3. Standpoint structures with nested S4F components
        s.add(standp_left.s1, standp_left.s1_label)
        s.add(standp_left.s2, standp_left.s2_label)
        for mini_s4f in mini_s4fs_left:
            s.add(mini_s4f)
        s.add(standp_right.s1, standp_right.s1_label)
        s.add(standp_right.s2, standp_right.s2_label)
        for mini_s4f in mini_s4fs_right:
            s.add(mini_s4f)
        s.add(pref_symbol)
        s.wait()
        s.next_slide()

        # 4. Hardness result
        s.add(hardness_result)
        s.wait()
        s.next_slide()

        # 5. QBF translation details
        s.add(qbf_title, qbf_formula, trans_formulas)
        s.wait()



class SS4fBeyondScene(Slide):
    def construct(self):
        SS4fBeyond(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
