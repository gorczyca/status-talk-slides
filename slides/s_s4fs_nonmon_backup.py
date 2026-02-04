from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.colors import BRILLIANT_BLUE
from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 999  # backup slide; exclude from main count if desired


class SS4fsNonmonBackup(BaseSlide):
    TITLE = r'Backup: S4F Standpoint'

    def create_content(self):
        s = self.slide

        # Credulous & sceptical reasoning details (blue)
        cred_title = TexWrapper(
            r"\textbf{Credulous and sceptical reasoning}",
            font_size=24,
            color=BRILLIANT_BLUE
        ).to_edge(LEFT, buff=0.8).shift(UP*2.2)

        cred_line_intro = MathTexWrapper(
            r"\text{Let } T \subseteq \langs \text{ be a theory, } \xi \in \langs \text{ a formula, and atom } z \in \Atoms \text{ not in } T \cup \{\xi\}.",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(cred_title, DOWN, buff=0.25, aligned_edge=LEFT)

        cred_line1 = MathTexWrapper(
            r"1.~T \approx_{\text{cred}} \xi \text{ iff } T^{\xi}_{\text{cred}} \text{ has a minimal model, where }",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(cred_line_intro, DOWN, buff=0.2, aligned_edge=LEFT)

        cred_line1_def = MathTexWrapper(
            r"T^{\xi}_{\text{cred}} := T \cup \{(\Box_{*}\neg\Box_{*}z \land \Box_{*}\neg\Box_{*}\xi) \rightarrow \Box_{*} z\}",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(cred_line1, DOWN, buff=0.12, aligned_edge=LEFT)

        cred_line2 = MathTexWrapper(
            r"2.~T \not\approx_{\text{scep}} \xi \text{ iff } T^{\xi}_{\text{scep}} \text{ has a minimal model, where }",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(cred_line1_def, DOWN, buff=0.2, aligned_edge=LEFT)

        cred_line2_def = MathTexWrapper(
            r"T^{\xi}_{\text{scep}} := T \cup \{(\Box_{*}\neg\Box_{*}z \land \neg\Box_{*}\neg\Box_{*}\xi) \rightarrow \Box_{*} z\}",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(cred_line2, DOWN, buff=0.12, aligned_edge=LEFT)

        # Expansion details (blue)
        exp_title = TexWrapper(
            r"\textbf{Expansions}",
            font_size=24,
            color=BRILLIANT_BLUE
        ).next_to(cred_line2_def, DOWN, buff=0.6, aligned_edge=LEFT)

        exp_line1 = MathTexWrapper(
            r"U \subseteq \langs \text{ is an expansion of } T \text{ iff } U = \{\psi \in \langs \mid T \cup \{\neg \standbs \phi \mid \standbs \phi \in \langs \setminus U\} \vDash_{\slogic} \psi\}.",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(exp_title, DOWN, buff=0.2, aligned_edge=LEFT)

        exp_line2 = MathTexWrapper(
            r"\sffsstruct \text{ is a minimal model of } T \text{ iff } Th(\sffsstruct):=\{\psi \in \langs \mid \sffsstruct \Vdash \psi\} \text{ is an expansion of } T.",
            font_size=20,
            color=BRILLIANT_BLUE
        ).next_to(exp_line1, DOWN, buff=0.15, aligned_edge=LEFT)

        s.add(cred_title, cred_line_intro, cred_line1, cred_line1_def, cred_line2, cred_line2_def,
              exp_title, exp_line1, exp_line2)
        s.wait()


class SS4fsNonmonBackupScene(Slide):
    def construct(self):
        SS4fsNonmonBackup(self, show_footer=False, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
