from pathlib import Path

from manim import *
from manim_slides import Slide

from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import TexWrapper, MathTexWrapper, latex_block
from slides.shared.colors import BRILLIANT_BLUE
from slides.shared.structures import S4FStructure, StandpointStructure, S4FSStructure, labeled_dot

from slides.shared.slide_count import SLIDES, SLIDES_NO

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

SLIDE_NO = 14


class SS4fNonmon(BaseSlide):
    TITLE = r'Standpoint S4F: Non-Monotonicity'

    def create_content(self):
        s = self.slide

        # Create standpoint structure - centered vertically on the left (larger)
        standp = StandpointStructure(
            scale_factor=2.5,
            show_world_labels=True,
            s1_color=BLUE,
            s2_color=RED
        ).to_edge(LEFT, buff=1).shift(UP * 1)

        # Get all worlds from the standpoint
        all_worlds = list(standp.s1_worlds) + \
            list(standp.shared_worlds) + list(standp.s2_worlds)

        # Create mini S4F structures at each world position
        mini_s4fs = []
        for world in all_worlds:
            # Create a small S4F at the world's position
            mini_s4f = S4FStructure(
                scale_factor=0.5,
                show_world_labels=False,
                dot_scale=2.0
            )
            mini_s4f.move_to(world.get_center())
            mini_s4fs.append(mini_s4f)

        # 1. Standpoint structure with mini S4Fs
        s.add(standp.s1, standp.s1_label)
        s.add(standp.s2, standp.s2_label)
        for mini_s4f in mini_s4fs:
            s.add(mini_s4f)
        s.wait()
        s.next_slide()

        # 2. Animate outer worlds moving to inner part for all mini S4Fs
        animations = []
        for mini_s4f in mini_s4fs:
            # Get the center of the inner ellipse for each mini S4F
            inner_center = mini_s4f.inner.get_center()

            # Move each outer world to a position inside the inner ellipse
            for i, outer_world in enumerate(mini_s4f.outer_worlds):
                # Calculate target position inside inner ellipse
                # Position them to avoid overlap - spread them out more
                if i == 0:
                    # First world goes more to the right
                    offset_x = 0.3 * mini_s4f._scale_factor
                    offset_y = 0.1 * mini_s4f._scale_factor
                elif i == 1:
                    # Second world goes to the left
                    offset_x = -0.25 * mini_s4f._scale_factor
                    offset_y = -0.03 * mini_s4f._scale_factor
                else:
                    # Additional worlds (if any) use angle-based positioning
                    offset_angle = (i - 2) * PI / max(1, len(mini_s4f.outer_worlds) - 2)
                    offset_x = 0.2 * mini_s4f._scale_factor * np.cos(offset_angle)
                    offset_y = -0.15 * mini_s4f._scale_factor * np.sin(offset_angle)

                target_pos = inner_center + np.array([offset_x, offset_y, 0])
                animations.append(outer_world.animate.move_to(target_pos))

        s.play(*animations)
        s.wait()
        s.next_slide()

        # 3. Entailment example on the right side
        entailment_title = TexWrapper(
            r"\textbf{Problem:}",
            font_size=24
        )

        entailment_formula = MathTexWrapper(
            r"\{\standb{\sts} \know a, \standb{\stu} \know b\} \mathrel{\mid\mkern-3mu\approx}_{\text{cred}} \standb{\sts} \know b",
            font_size=24
        )

        entailment_explanation = TexWrapper(
            r"$\sffstructS$ with $\stan(\sts)=\stan(\stu) = \set{\pr}$ and $\eval(\pr) = \set{a,b}$ is a minimal model",
            font_size=20,
            color=BRILLIANT_BLUE
        )

        # Arrange entailment section vertically
        entailment_block = VGroup(
            entailment_title,
            entailment_formula,
            entailment_explanation
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        # Shift explanation to the right
        entailment_explanation.shift(RIGHT * 0.25+UP*0.1)

        # Position to the right of standpoint and center vertically
        entailment_block.next_to(standp, RIGHT, buff=2.5).shift(DOWN * 0.5)

        # Minimal model explanation
        minimal_model_title = TexWrapper(
            r"\textbf{Minimal model:}",
            font_size=24
        ).next_to(standp, DOWN, buff=.25, aligned_edge=LEFT)

        minimal_model_desc = TexWrapper(
            r"\parbox{8.5cm}{\raggedright ``Freeze'' arbitrary structure + precisification-wise S4F minimization (Schwarz \& Truszczyński, 1993).}",
            font_size=24
        ).next_to(minimal_model_title, DOWN, buff=0.2, aligned_edge=LEFT)

        # Complexity result
        complexity_block = latex_block(
            r"``\textsc{Does a simple $\mathbb{S}$S4F theory $T$ have a minimal model}?'' is $\Sigma^P_2$-complete.",
            color=BRILLIANT_BLUE,
            body_font_size=20
        ).next_to(minimal_model_desc, DOWN, buff=0.5, aligned_edge=LEFT)

        # 3. Minimal model explanation
        s.add(minimal_model_title, minimal_model_desc)
        s.wait()
        s.next_slide()

        # 4. Complexity result
        s.add(complexity_block)
        s.wait()
        s.next_slide()

        # 5. Problem: entailment example
        s.add(entailment_block)
        s.wait()



class SS4fNonmonScene(Slide):
    def construct(self):
        SS4fNonmon(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
