from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper, latex_block
from slides.shared.colors import BRILLIANT_BLUE
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 11


class SS4fBackgroundNonmon(BaseSlide):
    TITLE = r'Background: Non-Monotonicity in S4F'

    def create_content(self):
        s = self.slide

        # Create left S4F structure (with one outer world)
        s4f_left = S4FStructure(
            scale_factor=1.0,
            show_world_labels=True
        ).to_corner(UL).shift(DOWN)
        # Remove one outer world to keep only one
        s4f_left.outer_worlds[1].set_opacity(0)

        # Create right S4F structure (no outer worlds)
        s4f_right = S4FStructure(
            scale_factor=1.0,
            show_world_labels=True
        ).next_to(s4f_left, RIGHT, buff=1)
        # Remove all outer worlds
        for w in s4f_right.outer_worlds:
            w.set_opacity(0)

        # Preference relation triangle between structures
        pref_symbol = MathTexWrapper(
            r'\triangleleft',
            font_size=40
        ).move_to((s4f_left.get_center() + s4f_right.get_center()) / 2)

        # Definition block below structures
        definition = latex_block(
            r"\parbox{7cm}{$\sffstruct$ is a \textbf{minimal model of} $T \subseteq\langk$ iff:\\\qquad 1. $\sffstruct\modelfor T$\\\quad 2. for all $\sffstruct'$ s.t.\ $\sffstruct'\spref\sffstruct$: $\sffstruct'\nmodelfor T$}",
            color=BRILLIANT_BLUE,
            body_font_size=24
        ).next_to(s4f_left, DOWN, buff=.25, aligned_edge=LEFT)

        # Encodings section below the definition
        enc_font = 24

        # Default Logic
        default_title = VGroup(
            TexWrapper(r"\textbf{Default Logic:}", font_size=enc_font),
            MathTexWrapper(r"\default{\phi}{\psi'}{\psi}", font_size=enc_font)
        ).arrange(RIGHT, buff=0.2)
        default_enc = MathTexWrapper(
            r"\leadsto\ (\know\phi\land\know\neg\know\neg\psi')\limplies\know\psi",
            font_size=enc_font
        )
        default_block = VGroup(default_title, default_enc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        default_block.next_to(definition, DOWN, buff=0.2, aligned_edge=LEFT)

        # Logic Programs
        lp_title = VGroup(
            TexWrapper(r"\textbf{Logic Programs:}", font_size=enc_font),
            # MathTexWrapper(r"p_0 \limpliedby p_1,\ldots,p_m, \lpnot p_{m+1}, \ldots, \lpnot p_{m+n}", font_size=enc_font)
            MathTexWrapper(r"p_0 \limpliedby p_1, \lpnot p_{2}", font_size=enc_font)
        ).arrange(RIGHT, buff=0.2)
        lp_enc = MathTexWrapper(
            r"\leadsto\ (\know p_1 \land\know\neg\know p_{2})\limplies \know p_0",
            font_size=enc_font
        )
        lp_block = VGroup(lp_title, lp_enc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        lp_block.next_to(default_block, DOWN, buff=0.25, aligned_edge=LEFT)

        # Argumentation Frameworks
        af_title = VGroup(
            TexWrapper(r"\textbf{Argumentation:}", font_size=enc_font),
            MathTexWrapper(r"\tuple{A,R} \text{ and } a\in A, \tuple{a,b}\in R", font_size=enc_font)
        ).arrange(RIGHT, buff=0.2)
        af_enc = MathTexWrapper(
            r"\leadsto\ \know\neg\know\neg a\limplies \know a, \quad \know a \limplies \know \neg b",
            font_size=enc_font
        )
        af_block = VGroup(af_title, af_enc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        af_block.next_to(lp_block, DOWN, buff=0.25, aligned_edge=LEFT)

        # Algorithm on the right side
        algo_title_font = 24
        algo_formula_font = 20

        algo_step1 = TexWrapper(
            r"Represent $\sffstruct$ by a partition $(\Phi,\Psi)$ of $\{\know\phi \mid \know\phi \in \mathit{Subf}(T)\}$.",
            font_size=algo_title_font
        )
        algo_step2 = MathTexWrapper(
            r"\text{Let } \Theta = A \cup \{\neg\know\phi \mid \phi \in \Phi\} \cup \{\know\psi \mid \psi \in \Psi\} \cup \Psi",
            font_size=algo_formula_font,
            color=BRILLIANT_BLUE
        )
        algo_intro_block = VGroup(algo_step1, algo_step2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        algo_step2.shift(RIGHT * 0.5)

        algo_check_header = TexWrapper(
            r"\textbf{Check if:}",
            font_size=algo_title_font
        )

        algo_check1_title = TexWrapper(
            r"\textbf{1.} Guessed beliefs can all be true?",
            font_size=algo_title_font
        )
        algo_check1_formula = TexWrapper(
            r"$\Theta$ is prop. consistent",
            font_size=algo_formula_font,
            color=BRILLIANT_BLUE
        )
        algo_check1_block = VGroup(algo_check1_title, algo_check1_formula).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        algo_check1_formula.shift(RIGHT * 0.5)

        algo_check2_title = TexWrapper(
            r"\textbf{2.} Rejected beliefs don't follow from the accepted ones?",
            font_size=algo_title_font
        )
        algo_check2_formula = TexWrapper(
            r"$\forall\varphi \in \Phi$: $\Theta \not\vdash \varphi$",
            font_size=algo_formula_font,
            color=BRILLIANT_BLUE
        )
        algo_check2_block = VGroup(algo_check2_title, algo_check2_formula).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        algo_check2_formula.shift(RIGHT * 0.5)

        algo_check3_title = TexWrapper(
            r"\textbf{3.} Structure is minimal?",
            font_size=algo_title_font
        )
        algo_check3_formula = TexWrapper(
            r"$\forall\psi \in \Psi$: $A \cup \{\neg\know\varphi \mid \varphi \in \Phi\} \vdash_{\text{S4F}} \psi$",
            font_size=algo_formula_font,
            color=BRILLIANT_BLUE
        )
        algo_check3_block = VGroup(algo_check3_title, algo_check3_formula).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        algo_check3_formula.shift(RIGHT * 0.5)

        algorithm_block = VGroup(
            algo_intro_block,
            algo_check_header,
            algo_check1_block,
            algo_check2_block,
            algo_check3_block
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        algorithm_block.next_to(s4f_right, RIGHT, buff=2.5).align_to(s4f_right, UP)

        # Complexity result in bottom right
        complexity_block = latex_block(
            r"``\textsc{Does $T\subseteq \langk$ have a minimal model}?'' is $\Sigma^P_2$-complete.",
            color=BRILLIANT_BLUE,
            body_font_size=20
        ).to_corner(DR, buff=0.5).shift(UP*1)

        # 1. Structures + relation
        s.add(s4f_left, s4f_right, pref_symbol)
        s.wait()
        s.next_slide()

        # 2. Minimal model definition
        s.add(definition)
        s.wait()
        s.next_slide()

        # 3. Other formalisms
        s.add(default_block, lp_block, af_block)
        s.wait()
        s.next_slide()

        # 4. Represent
        s.add(algo_intro_block)
        s.wait()
        s.next_slide()

        # 5. Check if header
        s.add(algo_check_header)
        s.wait()
        s.next_slide()

        # 5.1 Condition 1
        s.add(algo_check1_block)
        s.wait()
        s.next_slide()

        # 5.2 Condition 2
        s.add(algo_check2_block)
        s.wait()
        s.next_slide()

        # 5.3 Condition 3
        s.add(algo_check3_block)
        s.wait()
        s.next_slide()

        # 6. Complexity result
        s.add(complexity_block)
        s.wait()



class SS4fBackgroundNonmonScene(Slide):
    def construct(self):
        SS4fBackgroundNonmon(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
