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


class SS4FApproaches(BaseSlide):
    TITLE = r'S4F and Standpoint Logic: Product and Fusion'

    def create_content(self):
        s = self.slide

        # === Phase 1: S4F with single standpoint ===
        # Create S4F structure (single standpoint with inner + outer ellipse)
        s4f = S4FStructure(show_world_labels=True, color=LIGHT_GRAY).to_edge(
            LEFT).shift(UP*1.8 + RIGHT*2)
        s4f_label = TexWrapper(r'S4F', font_size=FONT_SIZE_TEXT).next_to(
            s4f, DOWN, buff=0.3)

        # s4f.shift(UP)

        standp = StandpointStructure().next_to(s4f, RIGHT, buff=3)
        standp_label = TexWrapper(
            r'Standpoint Logic', font_size=FONT_SIZE_TEXT).next_to(standp, DOWN, buff=0.3)

        s.add(standp, s4f_label, standp_label)

        # Show S4F structure (worlds and label included in VGroup)
        s.add(s4f)

        standp2 = StandpointStructure(
            scale_factor=2, show_world_labels=True).next_to(s4f, DOWN, buff=1)

        s.wait()
        s.next_slide()

        s.add(standp2)

        # Label below standp2
        standp2_label = TexWrapper(r'\textit{Standpoint S4F}', font_size=FONT_SIZE_TEXT).next_to(standp2, DOWN, buff=0.3)
        s.add(standp2_label)

        s.wait()
        s.next_slide()

        # Transform each world into a small S4F structure
        mini_s4fs = []
        all_worlds = list(standp2.s1_worlds) + \
            list(standp2.shared_worlds) + list(standp2.s2_worlds)

        for world in all_worlds:
            # Create a small S4F at the world's position
            mini_s4f = S4FStructure(
                scale_factor=0.4,
                show_world_labels=False,
                color=LIGHT_GRAY,
                dot_scale=2.0  # makes dots 2x thicker

            )
            mini_s4f.move_to(world.get_center())
            mini_s4fs.append(mini_s4f)

        # Animate transformation from worlds to mini S4Fs
        s.play(*[
            ReplacementTransform(world, mini_s4f)
            for world, mini_s4f in zip(all_worlds, mini_s4fs)
        ])

        s.wait()
        s.next_slide()

        s4f_standp = StandpointStructure(
            show_world_labels=True).next_to(standp2, RIGHT, buff=2.5).shift(DOWN*0.15)
        s.add(s4f_standp)

        s.wait()
        s.next_slide()

        # Create outer ellipses behind each standpoint
        sf = s4f_standp._scale_factor
        outer_size = (
            S4FStructure.BASE_OUTER_SIZE[0] * sf, S4FStructure.BASE_OUTER_SIZE[1] * sf)

        # Offset from inner to outer (inverse of S4FStructure's inner offset)
        inner_to_outer_offset = [-x *
                                 sf for x in S4FStructure.BASE_INNER_OFFSET]

        # S1 outer ellipse (positioned behind s1, touching at right-bottom edge)
        s1_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=0.2, color=BLACK, fill_color=BLUE, stroke_width=1.5
        ).rotate(-30 * DEGREES).move_to(s4f_standp.s1.get_center()).shift(inner_to_outer_offset).set_z_index(-1)

        # S2 outer ellipse (positioned behind s2, mirrored offset for opposite rotation)
        # mirror to touch at left-bottom
        s2_outer_offset = [-inner_to_outer_offset[0],
                           inner_to_outer_offset[1], 0]
        s2_outer = Ellipse(
            height=outer_size[0], width=outer_size[1],
            fill_opacity=0.2, color=BLACK, fill_color=RED, stroke_width=1.5
        ).rotate(30 * DEGREES).move_to(s4f_standp.s2.get_center()).shift(s2_outer_offset).set_z_index(-1)

        # Ensure s4f_standp is always in front
        s4f_standp.set_z_index(1)

        # Create outer-only worlds for each standpoint
        font_size = S4FStructure.BASE_FONT_SIZE * sf
        dot_radius = S4FStructure.BASE_DOT_RADIUS * sf

        s1_center = s4f_standp.s1.get_center()
        s1_outer_worlds = VGroup(
            labeled_dot(s1_center + [-0.9*sf, 0.6*sf, 0],
                        r"\pi_4", RIGHT, font_size, True, dot_radius),
            labeled_dot(s1_center + [-0.85*sf, 0.3*sf, 0],
                        r"\pi_5", RIGHT, font_size, True, dot_radius),
        )

        s2_center = s4f_standp.s2.get_center()
        s2_outer_worlds = VGroup(
            labeled_dot(s2_center + [0.75*sf, 0.5*sf, 0],
                        r"\pi_8", RIGHT, font_size, True, dot_radius),
            labeled_dot(s2_center + [0.65*sf, 0.15*sf, 0],
                        r"\pi_9", RIGHT, font_size, True, dot_radius),
        )

        # Animate the outer ellipses growing from behind
        s.play(
            GrowFromCenter(s1_outer),
            GrowFromCenter(s2_outer),
        )

        # Animate outer worlds appearing
        s.play(
            FadeIn(s1_outer_worlds),
            FadeIn(s2_outer_worlds),
        )

        s4f_standp_label = TexWrapper(r'\textit{S4F Standpoint}', font_size=FONT_SIZE_TEXT).next_to(s4f_standp, DOWN, buff=0.3)
        s.add(s4f_standp_label)

        # s.wait()
        # s.next_slide()

        # # === Phase 2: Transition to Standpoint Logic ===
        # # Fade out outer ellipse and outer-only worlds
        # s.play(
        #     FadeOut(s4f.outer),
        #     FadeOut(s4f.outer_worlds),
        # )

        # s.wait()
        # s.next_slide()

        # # === Phase 3: Standpoint Logic (two overlapping standpoints) ===
        # # Create standpoint structure
        # standpoint = StandpointStructure(s1_color=BLUE, s2_color=RED)
        # standpoint.scale(1.5).shift(UP)

        # # Replace S4F with standpoint structure (animate S2 appearing)
        # s.play(
        #     FadeOut(s4f.inner),
        #     FadeOut(s4f.middle),
        #     FadeOut(s4f.inner_worlds),
        #     FadeOut(s4f.label),
        # )

        # # Add standpoint structure (s1 first, then animate s2 appearing)
        # s.add(standpoint.s1_mask, standpoint.s1, standpoint.s1_label)
        # s.add(standpoint.s1_worlds, standpoint.shared_worlds)  # Only s1 visible worlds
        # s.play(GrowFromCenter(standpoint.s2))
        # s.add(standpoint.s2_mask, standpoint.s2_label, standpoint.s2_worlds)

        # s.wait()
        # s.next_slide()

        # # === Phase 4: S4FS (two standpoints with inner + outer) ===
        # # FadeOut standpoint (labels and worlds are now included in VGroup)
        # s.play(FadeOut(standpoint))

        # # Create full S4FS structure
        # s4fs = S4FSStructure(s1_color=BLUE, s2_color=RED)
        # s4fs.scale(1.5).shift(UP)

        # # Show full S4FS (all components now included in VGroup)
        # s.add(s4fs)

        # s.wait()
        # s.next_slide()


class SS4FApproachesScene(Slide):
    def construct(self):
        SS4FApproaches(self, show_footer=True,
                       slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
