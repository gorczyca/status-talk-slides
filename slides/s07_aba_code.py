from manim import *
from manim_slides import Slide

from slides.shared.asp_lexer import get_asp_code, set_asp_lexer, create_code_block
from slides.shared.base_slide import BaseSlide
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE
from slides.shared.block_diagram import BlockDiagram

from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 7

FONT_SIZE_CODE = 17

set_asp_lexer()

def replace_animate(s, v1, v2):
    s.play(FadeOut(v1), FadeIn(v2))

def animate_scroll(s, cur, nxt):
    nxt.next_to(cur, DOWN, buff=0)
    shift = cur.get_center() - nxt.get_center()
    s.play(
        cur.animate.shift(shift),
        nxt.animate.shift(shift),
        FadeOut(cur)
    )
    # s.play(FadeOut(cur))
    s.next_slide()


class S07ABACode(BaseSlide):
    TITLE = r'Extension to ABA Disputes: Code'

    def create_content(self):
        s = self.slide


        self._active = {}
        def show_step(code_obj, ranges, on=0.25, rt=0.3, pad=0.04, top_trim=0):
            if code_obj in self._active:
                s.play(*[r.animate.set_opacity(0)
                    for r in self._active[code_obj]], run_time=rt/2)
                s.remove(self._active[code_obj])
                del self._active[code_obj]
            if ranges:
                new_rects = VGroup(
                    *[create_code_block(code_obj, a, b, opacity=on, pad=pad, top_trim=top_trim) for a, b in ranges])
                for r in new_rects:
                    r.set_opacity(0)
                s.add(new_rects)
                s.play(*[r.animate.set_opacity(on) for r in new_rects], run_time=rt)
                self._active[code_obj] = new_rects

        # code_python = Code(
        #     tab_width=2, code_file="./code/control.py",
        #     language='python',
        #     formatter_style='one-dark'  # tried with perldoc, gruvbox-dark, vs, dracula, one-dark, monokai, nord-darker, paraiso-dark, solarized-dark, coffee, github-dark, stata-dark
        # ).set(width=6).move_to(ORIGIN)     
        
        # s.add(code_python)
        # s.wait()
        # s.next_slide()    
 

        diagram = BlockDiagram().move_to(ORIGIN)
        s.add(diagram)
        
        # s.next_slide()    
        # s.play(ReplacementTransform(code_python, diagram))

        c1 = get_asp_code('./code/aba-encoding/01-base.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True).move_to(ORIGIN)
        C2_LINE_START = 9
        C3_LINE_START = 24
        C4_LINE_START = 44
        C5_LINE_START = 56

        c2 = get_asp_code('./code/aba-encoding/02-update-state-1.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True, line_numbers_from=C2_LINE_START).move_to(ORIGIN)
        c3 = get_asp_code('./code/aba-encoding/03-update-state-2.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True, line_numbers_from=C3_LINE_START)
        c4 = get_asp_code('./code/aba-encoding/04-update-state-3.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True, line_numbers_from=C4_LINE_START)
        c5 = get_asp_code('./code/aba-encoding/05-step.lp', font_size=FONT_SIZE_CODE, add_line_numbers=True, line_numbers_from=C5_LINE_START).move_to(ORIGIN)
        
        s.wait()
        s.next_slide()
        replace_animate(s, diagram, c1)
        s.next_slide()

        show_step(c1, [(3,3)])
        s.next_slide()
        show_step(c1, [(7,7)])

        s.next_slide()
        show_step(c1, [])
        animate_scroll(s, c1, c2)
        s.next_slide()

        animate_scroll(s, c2, c3)

        s.next_slide()
        show_step(c3, [(11,20)])
        s.next_slide()
        show_step(c3, [])

        animate_scroll(s, c3, c4)
        s.next_slide()
        show_step(c4, [(10,11)])
        s.next_slide()
        show_step(c4, [])

        animate_scroll(s, c4, c5)

        s.next_slide()
        show_step(c5, [(2,2)])
        s.next_slide()
        show_step(c5, [(3,3)])
        s.next_slide()
        show_step(c5, [])


class S07AbaCodeScene(Slide):
    def construct(self):
        S07ABACode(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
