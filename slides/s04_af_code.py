from re import S
from turtle import width
from webbrowser import Opera
from manim import *
from manim_slides import Slide
import numpy as np

from pygments import highlight
from pygments.lexers.prolog import PrologLexer
from pygments.lexer import RegexLexer
from pygments.token import Keyword, Name, Number, String, Operator, Punctuation, Comment, Text
# from pygments.lexers import register
import manim.mobject.text.code_mobject as cm
import pygments.lexers as pyg_lex


from pygments.style import Style
from pygments.styles import get_style_by_name, STYLE_MAP

from pathlib import Path
from slides.shared.base_slide import BaseSlide
from slides.shared.common import highlight_box
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE


from slides.shared.slide_count import SLIDES, SLIDES_NO
SLIDE_NO = 4


class ASPLexer(RegexLexer):
    name = "ASP"
    aliases = ["asp", "clingo"]
    filenames = ["*.lp"]
    tokens = {
        "root": [
            (r"%.*?$", Comment.Single),
            (r"#(show|const|include|program|external|minimize|maximize|heuristic)\b", Keyword),
            # (r"(not|#count|#sum|#min|#max|#int)\b", Keyword),
            (r"(#count|#sum|#min|#max|#int)\b", Keyword),
            # (r":-|-->|<-|==|!=|<=|>=|=|\+|-|\*|/", Operator),
            (r"[A-Z][A-Za-z0-9_]*", Name.Variable),
            (r"[a-z][A-Za-z0-9_]*", Name),
            (r"\d+", Number),
            (r'"[^"]*"', String),
            # (r"[(),.\[\]{};:<>]", Punctuation),
            (r"[(),.\[\]{}]", Operator),
            (r"\s+", Text),
        ],
    }


_orig = pyg_lex.get_lexer_by_name


def _asp_get(alias, **opts):
    return ASPLexer(**opts) if alias.lower() in ("asp", "clingo") else _orig(alias, **opts)


pyg_lex.get_lexer_by_name = _asp_get
cm.get_lexer_by_name = _asp_get


STYLE_MAP["aspvs"] = "__main__:ASPVSStyle"   # register alias
setattr(cm, "DEFAULT_CODE_STYLE", "aspvs")   # force Code's default style
setattr(cm, "DEFAULT_STYLE", "aspvs")        # (covers other versions)

# style = get_style_by_name("one-dark")
# style.styles[Punctuation] = "#7aa2f7"  # brighter blue for parens



def create_code_block(code, a, b, color=YELLOW, opacity=0.05, pad=0.04, top_trim=0.0):
    lines = code.code_lines
    chunk = VGroup(*lines[a-1:b])
    r = SurroundingRectangle(chunk, buff=pad).set_fill(color, opacity).set_stroke(width=0)

    # left-locked horizontal stretch to code width
    r.align_to(code, LEFT)
    sx = code.width / r.width if r.width else 1.0
    r.stretch(sx, dim=0, about_point=r.get_left())

    # trim only the top (bottom stays put)
    if top_trim > 0:
        trim = min(top_trim, r.height - 1e-6)
        sy = (r.height - trim) / r.height
        r.stretch(sy, dim=1, about_point=r.get_bottom())

    return r





class S04AFCode(BaseSlide):
    TITLE = r"Multi-shot ASP for Dung's AFs"

    def create_content(self):
        s = self.slide

        def fixed_arrow_graph(n1, n2, tip_h=0.2, tip_w=0.16, stroke=2, color=BLACK):
            c1, c2 = n1.get_center(), n2.get_center()
            v = c2 - c1
            u = normalize(v)
            ang = angle_of_vector(v)
            p1 = n1.point_at_angle(ang)
            p2 = n2.point_at_angle(ang + PI)
            end = p2 - u * tip_h
            shaft = Line(p1, end, color=color, stroke_width=stroke)
            w = rotate_vector(u, PI / 2) * (tip_w / 2)
            base_center = end
            apex = end + u * tip_h
            tip = Polygon(apex, base_center - w, base_center + w).set_fill(color, 1).set_stroke(width=0)
            return VGroup(shaft, tip)

        # First show the graph

        Y_SHIFT = 0.5
        X_SHIFT = 2
        RADIUS = 0.3
        c_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(r"c").set_z_index(99))
        d_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(r"d").set_z_index(99)).next_to(c_node, RIGHT*X_SHIFT)
        a_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(r"a").set_z_index(99)).next_to(d_node, RIGHT*X_SHIFT).shift(DOWN*Y_SHIFT)
        e_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(r"e").set_z_index(99)).next_to(c_node, LEFT*X_SHIFT).shift(DOWN*Y_SHIFT)
        b_node = Circle(radius=RADIUS, color=BLACK).add(MathTexWrapper(r"b").set_z_index(99)).next_to(c_node, LEFT*X_SHIFT).shift(UP*Y_SHIFT)

        edges = [(a_node, e_node), (b_node, c_node), (c_node, d_node), (d_node, a_node), (e_node, b_node), (e_node, c_node)]

        graph_obj = VGroup(a_node, b_node, c_node, d_node, e_node, *[fixed_arrow_graph(u, v) for u, v in edges]).scale(0.8)
        graph_obj.move_to(ORIGIN).shift(UP*2)
        s.play(Write(graph_obj))

        # Then show the encoding of the graph
        s.wait()
        s.next_slide()

        code_asp_instance = Code(
            tab_width=2,
            code_string=Path("./code/af-instance.lp").read_text(encoding="utf-8"),
            language='asp',
            formatter_style='one-dark'  # tried with perldoc, gruvbox-dark, vs, dracula, one-dark, monokai, nord-darker, paraiso-dark, solarized-dark, coffee, github-dark, stata-dark
        ).set(width=2.5).next_to(graph_obj, DOWN)
        # ).set(width=2.5).next_to(code_asp, RIGHT, aligned_edge=UP)
        # graph_obj.move_to(code_asp_instance, DOWN, aligned_edge=LEFT)

        s.play(FadeIn(code_asp_instance))

        instance_group = VGroup(graph_obj, code_asp_instance)

        s.next_slide()
        s.play(FadeOut(instance_group))


        code_asp = Code(
            tab_width=2,
            code_string=Path("./code/af.lp").read_text(encoding="utf-8"),
            language='asp',
            # line_spacing=0.7,        # tighter vertically
            formatter_style='one-dark'  # tried with perldoc, gruvbox-dark, vs, dracula, one-dark, monokai, nord-darker, paraiso-dark, solarized-dark, coffee, github-dark, stata-dark
        ).set(width=7).to_edge(LEFT)

        s.next_slide()
        s.play(FadeIn(code_asp))

        code_python = Code(
            tab_width=2, code_file="./code/control.py",
            language='python',
            # line_spacing=0.7,        # tighter vertically
            formatter_style='one-dark'  # tried with perldoc, gruvbox-dark, vs, dracula, one-dark, monokai, nord-darker, paraiso-dark, solarized-dark, coffee, github-dark, stata-dark
        ).set(width=6).to_edge(RIGHT)

        # s.add(code_asp, code_python)
        s.next_slide()
        s.play(FadeIn(code_python))

        # self._active = VGroup(); s.add(self._active)

        # def show_step(ranges, on=0.25, rt=0.3, pad=0.04):
        #     if len(self._active):
        #         s.play(*[r.animate.set_opacity(0) for r in self._active], run_time=rt/2)
        #         s.remove(self._active)
        #     if len(ranges):
        #         new_rects = VGroup(*[create_code_block(code, a, b, opacity=on, pad=pad) for a, b in ranges])
        #         for r in new_rects: r.set_opacity(0)
        #         s.add(new_rects)
        #         s.play(*[r.animate.set_opacity(on) for r in new_rects], run_time=rt)
        #         self._active = new_rects

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

        def show_code_lines_both():
            TOP_TRIM = 0.15
            # show Control object
            s.wait()
            s.next_slide()
            show_step(code_python, [(4, 4)], top_trim=TOP_TRIM)

            # show loading instance
            s.next_slide()      
            show_step(code_python, [(5, 5)], top_trim=TOP_TRIM)


            # show loading encoding
            s.next_slide()
            show_step(code_python, [(6, 6)], top_trim=TOP_TRIM)
            show_step(code_asp, [(1, 22)]) # entire ASP encoding

            # show grounding base
            s.next_slide()
            show_step(code_python, [(7, 7)], top_trim=TOP_TRIM)
            show_step(code_asp, [(1, 3)])

            #show initializing T
            s.next_slide()
            show_step(code_python, [(8, 8)], top_trim=TOP_TRIM)
            show_step(code_asp, [])

            # show loop
            s.next_slide()
            show_step(code_python, [(9, 9)], top_trim=TOP_TRIM)

            # show grounding update state
            s.next_slide()
            show_step(code_python, [(10, 10)], top_trim=TOP_TRIM)
            show_step(code_asp, [(5, 15)])

            # check satisfiability
            s.next_slide()
            show_step(code_python, [(11,15)], top_trim=TOP_TRIM)
            show_step(code_asp, [])

            # check satisfiability 2
            s.next_slide()
            show_step(code_python, [(16,19)], top_trim=TOP_TRIM)

            # increment t
            s.next_slide()
            show_step(code_python, [(20,20)], top_trim=TOP_TRIM)

            # show grounding
            s.next_slide()
            show_step(code_python, [(21, 21)], top_trim=TOP_TRIM)
            show_step(code_asp, [(17, 19)])

            s.next_slide()
            show_step(code_python, [])
            show_step(code_asp, [])

        # s.wait()
        # s.next_slide()
        show_code_lines_both()
        s.next_slide()

        def fixed_arrow(a, b, tip_h=0.2, tip_w=0.16, stroke=2, color=BLACK):
            p1 = a.get_center() if hasattr(a, "get_center") else np.array(a)
            p2 = b.get_center() if hasattr(b, "get_center") else np.array(b)
            v = p2 - p1
            u = normalize(v)
            end = p2 - u * tip_h
            shaft = Line(p1, end, color=color, stroke_width=stroke)
            w = rotate_vector(u, PI/2) * (tip_w / 2)
            tip = Polygon(end + u*tip_h, end - w, end + w).set_fill(color, 1).set_stroke(width=0)
            return VGroup(shaft, tip)




        FONT_SIZE = 20
        BUFF = 0.5

        GGRAY = '#dddddd'
        first = RoundedRectangle(0.15, width=1.5, height=0.6, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'ground \texttt{base.}\\set \texttt{t:=0}', font_size=FONT_SIZE).set_z_index(99))
        second = RoundedRectangle(0.15, width=2.5, height=0.45, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'ground \texttt{updateState(t).}', font_size=FONT_SIZE).set_z_index(99)).next_to(first, DOWN, buff=BUFF)
        third = RegularPolygon(4, color=BLACK).scale([0.6, 1.3, 1]).rotate(PI/2).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'\texttt{:- not end(p,t).} SAT?', font_size=FONT_SIZE).set_z_index(99)).next_to(second, DOWN, buff=BUFF)
        third_yes = Circle(radius=.25, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'YES', font_size=FONT_SIZE)).next_to(third, RIGHT, buff=1)
        fourth = RegularPolygon(4, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).scale([0.6, 1.3, 1]).rotate(PI/2).set_stroke(width=2).add(TexWrapper(r'\texttt{:- end(o,t).} UNSAT?', font_size=FONT_SIZE).set_z_index(99)).next_to(third, DOWN, buff=BUFF)
        fourth_yes = Circle(radius=.25, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'NO', font_size=FONT_SIZE)).next_to(fourth, RIGHT, buff=1)
        fifth = RoundedRectangle(0.15, width=1.8, height=0.6, color=BLACK).set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2).add(TexWrapper(r'\texttt{t:=t+1}\\ground \texttt{step(t).}', font_size=FONT_SIZE, color=BLACK).set_z_index(99)).next_to(fourth, DOWN, buff=BUFF)

        for m in [first, second, third, third_yes, fourth, fourth_yes, fifth]:
            m.set_z_index(1)
            m[-1].set_z_index(2)


        arrows = VGroup(
            fixed_arrow(first.get_bottom(),  second.get_top()),
            fixed_arrow(second.get_bottom(), third.get_top()),
            fixed_arrow(third.get_right(),   third_yes.get_left()),
            fixed_arrow(third.get_bottom(),  fourth.get_top()),
            fixed_arrow(fourth.get_right(),  fourth_yes.get_left()),
            fixed_arrow(fourth.get_bottom(), fifth.get_top()),
        )

        yes_no_labels = VGroup(
            TextWrapper("YES").scale(0.4).next_to(Line(third.get_right(), third_yes.get_left()).get_center(), UP, buff=0.1),
            TextWrapper("NO").scale(0.4).next_to(Line(third.get_bottom(), fourth.get_top()).get_center(), LEFT, buff=0.1),
            TextWrapper("YES").scale(0.4).next_to(Line(fourth.get_right(), fourth_yes.get_left()).get_center(), UP, buff=0.1),
            TextWrapper("NO").scale(0.4).next_to(Line(fourth.get_bottom(), fifth.get_top()).get_center(), LEFT, buff=0.1),
        )

        x_left = min(b.get_left()[0] for b in [first, second, third, fourth, fifth]) - 0.6
        p0 = fifth.get_left()
        p1 = np.array([x_left, p0[1], 0])
        p2 = np.array([x_left, second.get_left()[1], 0])
        p3 = second.get_left()

        back = VGroup(
            Line(p0, p1).set_stroke(BLACK, 2),
            Line(p1, p2).set_stroke(BLACK, 2),
            fixed_arrow(Dot(p2), Dot(p3))  # arrowhead on the final leg
        )



        diagram = VGroup(first, second, third, third_yes, fourth, fourth_yes, fifth, arrows, back, yes_no_labels).scale(0.8)

        diagram.next_to(code_asp, RIGHT, aligned_edge=UP, buff=1)

        # s.add(diagram)
        s.play(ReplacementTransform(code_python, diagram))
        s.wait()

        def highlight(node, color=YELLOW, opacity=0.75):
            h = node.copy().set_fill(color, opacity).set_stroke(width=0).set_z_index(0)
            return h

        # s.wait()
        s.next_slide()
        

        highlighted_first = highlight(first)
        s.next_slide()



        highlighted_second = highlight(second)
        highlighted_third = highlight(third)
        highlighted_fourth = highlight(fourth)
        highlighted_fifth = highlight(fifth)

        # diagram_group = VGroup(diagram, highlighted_first, highlighted_second, highlighted_third, highlighted_fourth, highlighted_fifth)

        s.play(FadeIn(highlighted_first, scale=1.1))
        s.next_slide()        
        show_step(code_asp, [(1, 3)])
        s.next_slide()        

        # s.play(FadeOut(highlighted_first), FadeIn(highlighted_second, scale=1.1))
        # s.next_slide()
        # s.play(FadeOut(highlighted_second), FadeIn(highlighted_third, scale=1.1))
        # s.next_slide()
        # s.play(FadeOut(highlighted_third), FadeIn(highlighted_fourth, scale=1.1))
        # s.next_slide()
        # s.play(FadeOut(highlighted_fourth), FadeIn(highlighted_fifth, scale=1.1))
        # s.next_slide()
        # s.play(FadeOut(highlighted_fifth), FadeIn(highlighted_second, scale=1.1))


        # s.play(FadeOut(code_python))

        def replace_animate(v1, v2):
            s.play(FadeOut(v1), FadeIn(v2))

        code_asp_instance.next_to(code_asp, RIGHT, aligned_edge=UP)
        graph_obj.next_to(code_asp_instance, DOWN, aligned_edge=LEFT)

        # s.play(ReplacementTransform(diagram_group, instance_group))
        replace_animate(VGroup(highlighted_first, diagram), instance_group)
        s.next_slide()

        lines_group = VGroup()
        instance_group.add(lines_group)

        def show_line(graph_o, line_g, line):
            t = TexWrapper(line, font_size=25).set_z_index(99)
            line_g.add(t)
            line_g.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            line_g.next_to(graph_o, RIGHT, aligned_edge=UP)
            s.play(Write(t))
        
        show_line(graph_obj, lines_group, r'Output:')
        s.next_slide()
        show_step(code_asp, [(3, 3)])

        color_nodes = VGroup()

        s.next_slide()
        d_node_green = highlight(d_node, color=[GREEN,WHITE])
        s.play(FadeIn(d_node_green))
        # instance_group.add(d_node_green)
        color_nodes.add(d_node_green)
        s.next_slide()
        show_line(graph_obj, lines_group, r'\texttt{m(0,p,d).}')  

        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_first, diagram))
        show_step(code_asp, [])

        s.next_slide()
        s.play(FadeOut(highlighted_first), FadeIn(highlighted_second, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(5, 15)])

        s.next_slide()
        replace_animate(VGroup(highlighted_second, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        show_step(code_asp, [(6, 6)])
        s.next_slide()
        a_node_red = highlight(a_node, color=[RED,WHITE])
        s.play(FadeIn(a_node_red))
        instance_group.add(a_node_red)


        s.next_slide()
        show_step(code_asp, [(7, 9)])
        s.next_slide()
        show_step(code_asp, [(10, 11)])
        s.next_slide()
        c_node_blue = highlight(c_node, color=[BLUE,WHITE])
        color_nodes.add(c_node_blue)
        s.play(FadeIn(c_node_blue))
        s.next_slide()
        show_step(code_asp, [(12, 13)])

        s.next_slide()
        show_step(code_asp, [(14, 15)])

        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_second, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_second), FadeIn(highlighted_third, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(12, 13)])
        s.next_slide()
        replace_animate(VGroup(highlighted_third, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_third, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_third), FadeIn(highlighted_fourth, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(14, 15)])
        s.next_slide()
        replace_animate(VGroup(highlighted_fourth, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_fourth, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_fourth), FadeIn(highlighted_fifth, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(17, 19)])
        s.next_slide()
        replace_animate(VGroup(highlighted_fifth, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        show_step(code_asp, [(18, 18)])
        s.next_slide()
        c_node_yellow = highlight(c_node, color=[YELLOW,WHITE])
        # instance_group.add(c_node_yellow)
        color_nodes.add(c_node_yellow)
        s.play(Transform(c_node_blue, c_node_yellow))
        s.next_slide()
        show_line(graph_obj, lines_group, r'\texttt{m(1,o,c).}')
        s.next_slide()
        show_step(code_asp, [(19, 19)])
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_fifth, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_fifth), FadeIn(highlighted_second, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(5, 15)])
        s.next_slide()
        replace_animate(VGroup(highlighted_second, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        show_step(code_asp, [(6, 6)])
        s.next_slide()
        show_step(code_asp, [(7, 9)])
        s.next_slide()
        b_node_blue = highlight(b_node, color=[BLUE,WHITE])
        e_node_blue = highlight(e_node, color=[BLUE,WHITE])
        s.play(FadeIn(b_node_blue), FadeIn(e_node_blue))
        # instance_group.add(b_node_blue, e_node_blue)
        color_nodes.add(e_node_blue, b_node_blue)
        s.next_slide()
        show_step(code_asp, [(10, 11)])
        s.next_slide()
        show_step(code_asp, [(12, 13)])
        s.next_slide()
        show_step(code_asp, [(14, 15)])
        s.next_slide()
        show_step(code_asp, [])
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_second, diagram))
        s.next_slide()
        s.play(FadeOut(highlighted_second), FadeIn(highlighted_third, scale=1.1))
        show_step(code_asp, [(12,13)])
        s.next_slide()
        replace_animate(VGroup(highlighted_third, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes),VGroup(highlighted_third, diagram))
        s.next_slide()
        s.play(FadeOut(highlighted_third), FadeIn(highlighted_fourth, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(14, 15)])
        s.next_slide()
        replace_animate(VGroup(highlighted_fourth, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_fourth, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_fourth), FadeIn(highlighted_fifth, scale=1.1))
        s.next_slide()
        show_step(code_asp, [(17, 19)])
        s.next_slide()
        replace_animate(VGroup(highlighted_fifth, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        show_step(code_asp, [(18,18)])
        s.next_slide()
        show_step(code_asp, [(19,19)])
        graph_obj.add(a_node_red,  b_node_blue, c_node_yellow, d_node_green, e_node_blue)
        graph_code_obj = VGroup(graph_obj, lines_group)
        
        s.next_slide()
        graph_obj_cp = graph_code_obj.copy().shift(DOWN*1.5)
        s.play(TransformFromCopy(graph_code_obj, graph_obj_cp))


        s.next_slide()
        b_node_green = highlight(b_node, color=[GREEN,WHITE])
        s.play(Transform(b_node_blue, b_node_green), FadeOut(e_node_blue))
        s.remove(e_node_blue)
        graph_obj.remove(e_node_blue)
        color_nodes.remove(e_node_blue)
        s.remove(e_node_blue)
        # color_nodes.remove(e_node)
        s.next_slide()
        show_line(graph_obj, lines_group, r'\texttt{m(2,p,b).}')

        s.next_slide()
        b_node_cp = graph_obj_cp[0][1]
        c_node_cp = graph_obj_cp[0][2]
        e_node_cp = graph_obj_cp[0][4]
        b_node_blue_cp = graph_obj_cp[0][-4]
        c_node_yellow_cp = graph_obj_cp[0][-3]
        e_node_blue_cp = graph_obj_cp[0][-1]
        e_node_cp_green = highlight(e_node_cp, color=[GREEN, WHITE])
        s.play(Transform(e_node_blue_cp, e_node_cp_green), FadeOut(b_node_blue_cp))

        graph_obj_cp[0].remove(b_node_blue_cp)
        s.remove(b_node_blue_cp)
        s.next_slide()
        show_line(graph_obj_cp[0], graph_obj_cp[1], r'\texttt{m(2,p,e).}')
        s.next_slide()
        instance_group.add(graph_code_obj, graph_obj_cp, e_node_cp_green)
        # 


        replace_animate(VGroup(instance_group, color_nodes), VGroup(highlighted_fifth, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_fifth), FadeIn(highlighted_second, scale=1.1))
        show_step(code_asp, [(5, 15)])
        s.next_slide()
        replace_animate(VGroup(highlighted_second, diagram), VGroup(instance_group, color_nodes))
        s.next_slide()
        show_step(code_asp, [(6, 6)])
        s.next_slide()
        c_node_red = highlight(c_node, color=[RED,WHITE])
        s.play(FadeOut(c_node_yellow), FadeIn(c_node_red))
        color_nodes.remove(c_node_yellow)
        graph_obj.remove(c_node_yellow)
        s.next_slide()
        #
        b_node_cp_red = highlight(b_node_cp, color=[RED,WHITE])
        c_node_cp_red = highlight(c_node_cp, color=[RED,WHITE])
        #
        s.play(FadeIn(b_node_cp_red), Transform(c_node_yellow_cp, c_node_cp_red))
        s.next_slide()
        show_step(code_asp, [(7, 9)])
        s.next_slide()
        # new_color_nodes.add(e_node_blue)
        show_step(code_asp, [(10, 11)])
        s.next_slide()
        s.play(FadeIn(e_node_blue))
        s.next_slide()

        new_color_nodes = VGroup(b_node_cp_red, c_node_cp_red, c_node_red, e_node_blue)

        show_step(code_asp, [(12, 13)])
        s.next_slide()
        show_line(graph_obj_cp[0], graph_obj_cp[1], r'\texttt{end(2,p).}')
        s.next_slide()
        show_step(code_asp, [(14, 15)])
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes, new_color_nodes), VGroup(highlighted_second, diagram))
        show_step(code_asp, [])
        s.next_slide()
        s.play(FadeOut(highlighted_second), FadeIn(highlighted_third, scale=1.1))
        show_step(code_asp, [(12,13)])
        s.next_slide()
        replace_animate(VGroup(highlighted_third, diagram), VGroup(instance_group, color_nodes, new_color_nodes))
        s.next_slide()
        # highlight_box()
        # highlight first move
        HIGHLIGHT_FILL_OPACITY=0.2
        HIGHLIGHT_BUFF=0.05
        box = highlight_box(graph_obj_cp[1][-1], buff=HIGHLIGHT_BUFF, fill_opacity=HIGHLIGHT_FILL_OPACITY)
        s.play(FadeIn(box))
        s.next_slide()
        s.play(Circumscribe(graph_obj_cp, color=GREEN))
        s.next_slide()
        s.play(FadeOut(box))
        s.next_slide()
        replace_animate(VGroup(instance_group, color_nodes, new_color_nodes), VGroup(highlighted_third, diagram))
        s.next_slide()
        highlighted_third_yes = highlight(third_yes)
        s.play(FadeOut(highlighted_third), FadeIn(highlighted_third_yes, scale=1.1))
        s.play(Circumscribe(highlighted_third_yes, color=GREEN))


class S04AfCodeScene(Slide):
    def construct(self):
        S04AFCode(self, show_footer=True, slide_no=SLIDE_NO, slide_total=SLIDES_NO)
        self.wait()
