from pathlib import Path
from re import L

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper
from slides.shared.common import FONT_SIZE_TEXT
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 13


class SSs4fSyntax(BaseSlide):
    TITLE = r'Standpoint S4F: Syntax \& Semantics'

    def create_content(self):
        s = self.slide

        # Create standpoint structure - centered vertically on the right
        standp = StandpointStructure(
            scale_factor=2,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).to_edge(RIGHT, buff=1).shift(UP * 1)

        # Set opacity on the ellipses to show overlap
        # standp.s1.set_fill(opacity=0.2)
        # standp.s2.set_fill(opacity=0.2)

        # Get all worlds from the standpoint
        all_worlds = list(standp.s1_worlds) + \
            list(standp.shared_worlds) + list(standp.s2_worlds)

        # Create mini S4F structures at each world position
        mini_s4fs = []
        for world in all_worlds:
            # Create a small S4F at the world's position
            mini_s4f = S4FStructure(
                scale_factor=0.4,
                show_world_labels=False,
                dot_scale=2.0
            )
            mini_s4f.move_to(world.get_center())
            mini_s4fs.append(mini_s4f)

        # Language definition
        lang_title = TexWrapper(
            r"Language $\langk$:",
            font_size=FONT_SIZE_TEXT
        ).to_edge(LEFT, buff=1).shift(UP * 2)

        lang_grammar = MathTexWrapper(
            r"\psi ::= \know\alpha \mid \neg\psi \mid \psi \land \psi \mid \know\psi",
            font_size=FONT_SIZE_TEXT
        ).next_to(lang_title, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.2)

        # Simple theory definition
        simple_title = TexWrapper(
            r"An $\mathbb{S}$S4F \textbf{simple} theory $T$:",
            font_size=FONT_SIZE_TEXT
        ).next_to(lang_grammar, DOWN, buff=0.5, aligned_edge=LEFT).shift(LEFT * 0.2)

        simple_condition = TexWrapper(
            r"Each $\varphi\in T$ is of the form $\varphi = \standbs \psi$ with $\psi \in \langk$.",
            font_size=FONT_SIZE_TEXT
        ).next_to(simple_title, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.2)

        # Default rule translation (initial, without modalities) - structured for matching
        default_rule_initial = MathTexWrapper(
            r"\default{\phi}{\psi'}{\psi}", r"\leadsto", r"(", r"\know", r"\phi", r"\land", r"\know", r"\neg", r"\know", r"\neg", r"\psi'", r")", r"\limplies", r"\know", r"\psi",
            font_size=FONT_SIZE_TEXT
        ).next_to(simple_condition, DOWN, buff=0.5, aligned_edge=LEFT)

        # Default rule with standpoint modalities - structured for matching
        default_rule_with_modalities = MathTexWrapper(
            r"\standbs", r"\left[", r"\default{\phi}{\psi'}{\psi}", r"\right]", r"\leadsto", r"\standbs", r"\left[", r"(", r"\know", r"\phi", r"\land", r"\know", r"\neg", r"\know", r"\neg", r"\psi'", r")", r"\limplies", r"\know", r"\psi", r"\right]",
            font_size=FONT_SIZE_TEXT
        ).next_to(simple_condition, DOWN, buff=0.5, aligned_edge=LEFT)

        # Semantics at the bottom
        # K modality semantics
        sem_k = MathTexWrapper(
            r"\sffstructS, \pi, w \modelfor \know\varphi \quad :\Longleftrightarrow \quad \begin{cases} \sffstructS, \pi, w' \modelfor \varphi \text{ for all } w' \in \zeta_o(\pi) \cup \zeta_i(\pi) & \text{if } w \in \zeta_o(\pi) \\ \sffstructS, \pi, w' \modelfor \varphi \text{ for all } w' \in \zeta_i(\pi) & \text{if } w \in \zeta_i(\pi) \end{cases}",
            font_size=FONT_SIZE_TEXT
        ).to_edge(DOWN, buff=0.65).to_edge(LEFT, buff=1)

        # Box modality semantics
        sem_box = MathTexWrapper(
            r"\sffstructS, \pi, w \modelfor \standbs\varphi \quad :\Longleftrightarrow \quad \sffstructS, \pi', w' \modelfor \varphi \text{ for all } \pi' \in \sigma(s) \text{ and } w' \in \zeta_o(\pi') \cup \zeta_i(\pi')",
            font_size=FONT_SIZE_TEXT
        ).next_to(sem_k, UP, buff=0.3, aligned_edge=LEFT)

        # 1. Add standpoint base structure (including labels) and mini S4Fs + language
        s.add(standp.s1, standp.s1_label)
        s.add(standp.s2, standp.s2_label)
        for mini_s4f in mini_s4fs:
            s.add(mini_s4f)
        s.add(lang_title, lang_grammar)
        s.wait()
        s.next_slide()

        # 2. Add simple theory definition
        s.add(simple_title, simple_condition)
        s.wait()
        s.next_slide()

        # 3. Add default rule translation (initial)
        s.add(default_rule_initial)
        s.wait()
        s.next_slide()

        # 4. Transform to add standpoint modalities
        s.play(TransformMatchingTex(default_rule_initial, default_rule_with_modalities))
        s.wait()
        s.next_slide()

        # 5. Add semantics
        s.add(sem_k, sem_box)
        s.wait()



class SSs4fSyntaxScene(Slide):
    def construct(self):
        SSs4fSyntax(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
