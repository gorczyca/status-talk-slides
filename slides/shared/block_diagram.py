from manim import *
from manim_slides import Slide
import numpy as np

from shared.wrappers import *


def fixed_arrow(a, b, tip_h=0.2, tip_w=0.16, stroke=2, color=BLACK):
    p1 = a.get_center() if hasattr(a, "get_center") else np.array(a)
    p2 = b.get_center() if hasattr(b, "get_center") else np.array(b)
    v = p2 - p1
    u = normalize(v)
    end = p2 - u * tip_h
    shaft = Line(p1, end, color=color, stroke_width=stroke)
    w = rotate_vector(u, PI / 2) * (tip_w / 2)
    tip = Polygon(end + u * tip_h, end - w, end + w).set_fill(color, 1).set_stroke(width=0)
    return VGroup(shaft, tip)


class BlockDiagram(VGroup):
    def __init__(self, font_size=20, buff=0.5, box_color=BLACK, **kwargs):
        super().__init__(**kwargs)
        GGRAY = '#dddddd'

        def box(txt, w, h):
            return RoundedRectangle(0.15, width=w, height=h, color=box_color)\
                .set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2)\
                .add(TexWrapper(txt, font_size=font_size).set_z_index(99))

        first = box(r'ground \texttt{base.}\\set \texttt{t:=0}', 1.5, 0.6)
        second = box(r'ground \texttt{updateState(t).}', 2.5, 0.45).next_to(first, DOWN, buff=buff)
        third = RegularPolygon(4, color=box_color).scale([0.6, 1.3, 1]).rotate(PI/2)\
            .set_fill(color=[WHITE, GGRAY], opacity=0.5).set_stroke(width=2)\
            .add(TexWrapper(r'\texttt{:- not end(p,t).} SAT?', font_size=font_size).set_z_index(99))\
            .next_to(second, DOWN, buff=buff)
        third_yes = Circle(radius=.25, color=box_color).set_fill(color=[WHITE, GGRAY], opacity=0.5)\
            .set_stroke(width=2).add(TexWrapper(r'YES', font_size=font_size)).next_to(third, RIGHT, buff=1)
        fourth = RegularPolygon(4, color=box_color).set_fill(color=[WHITE, GGRAY], opacity=0.5)\
            .scale([0.6, 1.3, 1]).rotate(PI/2).set_stroke(width=2)\
            .add(TexWrapper(r'\texttt{:- end(o,t).} UNSAT?', font_size=font_size).set_z_index(99))\
            .next_to(third, DOWN, buff=buff)
        fourth_yes = Circle(radius=.25, color=box_color).set_fill(color=[WHITE, GGRAY], opacity=0.5)\
            .set_stroke(width=2).add(TexWrapper(r'NO', font_size=font_size)).next_to(fourth, RIGHT, buff=1)
        fifth = box(r'\texttt{t:=t+1}\\ground \texttt{step(t).}', 1.8, 0.6).next_to(fourth, DOWN, buff=buff)

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
            Text("YES").scale(0.4).next_to(Line(third.get_right(), third_yes.get_left()).get_center(), UP, buff=0.1),
            Text("NO").scale(0.4).next_to(Line(third.get_bottom(), fourth.get_top()).get_center(), LEFT, buff=0.1),
            Text("YES").scale(0.4).next_to(Line(fourth.get_right(), fourth_yes.get_left()).get_center(), UP, buff=0.1),
            Text("NO").scale(0.4).next_to(Line(fourth.get_bottom(), fifth.get_top()).get_center(), LEFT, buff=0.1),
        )

        x_left = min(b.get_left()[0] for b in [first, second, third, fourth, fifth]) - 0.6
        p0 = fifth.get_left()
        p1 = np.array([x_left, p0[1], 0])
        p2 = np.array([x_left, second.get_left()[1], 0])
        p3 = second.get_left()

        back = VGroup(
            Line(p0, p1).set_stroke(box_color, 2),
            Line(p1, p2).set_stroke(box_color, 2),
            fixed_arrow(Dot(p2), Dot(p3))
        )

        self.nodes = {
            "first": first,
            "second": second,
            "third": third,
            "third_yes": third_yes,
            "fourth": fourth,
            "fourth_yes": fourth_yes,
            "fifth": fifth,
        }

        self.add(first, second, third, third_yes, fourth, fourth_yes, fifth, arrows, back, yes_no_labels)
        self.scale(0.8)
        # highlights created later
        self.highlights = {}

    def create_highlights(self, color=YELLOW, opacity=0.75):
        if self.highlights:
            return self.highlights
        for name, node in self.nodes.items():
            h = node.copy().set_fill(color, opacity).set_stroke(width=0)
            h.set_z_index(node.get_z_index() - 1)
            # self.add(h)
            self.highlights[name] = h
        return self.highlights

    def get_highlight(self, name):
        return self.highlights[name]
