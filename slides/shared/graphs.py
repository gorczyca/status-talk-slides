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
from slides.shared.wrappers import MathTexWrapper, TexWrapper, TextWrapper
from slides.shared.colors import D_BLUE, LAT_ORANGE


from slides.shared.common import highlight_box


def fixed_arrow_graph(n1, n2, tip_h=0.2, tip_w=0.16, stroke=2, color=BLACK):
    get_pt = lambda x: x.get_center() if hasattr(x, "get_center") else np.array(x, dtype=float)
    c1, c2 = get_pt(n1), get_pt(n2)
    v = c2 - c1
    u = normalize(v)
    ang = angle_of_vector(v)
    p1 = n1.point_at_angle(ang) if hasattr(n1, "point_at_angle") else c1
    p2 = n2.point_at_angle(ang + PI) if hasattr(n2, "point_at_angle") else c2
    end = p2 - u * tip_h
    shaft = Line(p1, end, color=color, stroke_width=stroke)
    w = rotate_vector(u, PI / 2) * (tip_w / 2)
    base_center = end
    apex = end + u * tip_h
    tip = Polygon(apex, base_center - w, base_center + w).set_fill(color, 1).set_stroke(width=0)
    return VGroup(shaft, tip).set_z_index(99)


def curved_arrow(n1, n2, bend=0.6, color=BLACK, stroke=2):
    c1 = n1.get_center() if hasattr(n1, "get_center") else np.array(n1, float)
    c2 = n2.get_center() if hasattr(n2, "get_center") else np.array(n2, float)

    mid = (c1 + c2) / 2
    normal = rotate_vector(c2 - c1, PI / 2)
    ctrl = mid + normalize(normal) * bend

    start = n1.point_at_angle(angle_of_vector(c2 - c1)) if hasattr(n1, "point_at_angle") else c1
    end = n2.point_at_angle(angle_of_vector(c1 - c2)) if hasattr(n2, "point_at_angle") else c2

    shaft = CubicBezier(start, ctrl, ctrl, end, color=color, stroke_width=stroke)

    p1 = shaft.point_from_proportion(0.97)
    p2 = shaft.get_end()
    ang = angle_of_vector(p2 - p1)

    tip = ArrowTriangleFilledTip(color=color).scale(0.5).move_to(p2).rotate(ang + PI)

    return VGroup(shaft, tip).set_z_index(99)


def make_dispute_diagram():
    RADIUS = 0.25
    STROKE_WIDTH = 1
    HOR_DIST = 0.5

    # from your original
    PROP_COLOR = ["#E8FFE8", "#B5FFB5"]
    DEFEAT_COLOR = ["#FFE8E8", "#FFB5B5"]
    OPPONENT_COLOR = ["#FFFBE8", "#FFF1B5"]

    # --- NODES (all on top) ---
    s_node = Circle(
        radius=RADIUS,
        color=WHITE,
        stroke_opacity=0,
        fill_opacity=0
    ).add(MathTexWrapper("s")).set_z_index(99)

    d = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("d")).set_z_index(99)\
        .next_to(s_node, LEFT, buff=HOR_DIST).shift(UP)

    p = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0)\
        .add(MathTexWrapper("p")).set_z_index(99)\
        .next_to(s_node, LEFT, buff=HOR_DIST)

    a = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("a")).set_z_index(99)\
        .next_to(s_node, LEFT, buff=HOR_DIST).shift(DOWN)

    xc = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0)\
        .add(MathTexWrapper(r"\bar{c}")).set_z_index(99)\
        .next_to(p, LEFT, buff=HOR_DIST)

    f = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("f")).set_z_index(99)\
        .next_to(xc, LEFT, buff=HOR_DIST)

    xd = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0)\
        .add(MathTexWrapper(r"\bar{d}")).set_z_index(99)\
        .next_to(f, LEFT, buff=1.5 * HOR_DIST).shift(UP)

    e = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("e")).set_z_index(99)\
        .next_to(xd, LEFT, buff=HOR_DIST)

    xa = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0)\
        .add(MathTexWrapper(r"\bar{a}")).set_z_index(99)\
        .next_to(f, LEFT, buff=1.5 * HOR_DIST).shift(DOWN)

    b = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("b")).set_z_index(99)\
        .next_to(xa, LEFT, buff=HOR_DIST).shift(0.5 * UP)

    t = Circle(radius=RADIUS, color=WHITE, stroke_opacity=0, fill_opacity=0)\
        .add(MathTexWrapper("t")).set_z_index(99)\
        .next_to(xa, LEFT, buff=HOR_DIST).shift(0.5 * DOWN)

    c = Circle(radius=RADIUS, color=BLACK, stroke_width=STROKE_WIDTH)\
        .add(MathTexWrapper("c")).set_z_index(99)\
        .next_to(t, LEFT, buff=HOR_DIST)

    xe = Circle(
        radius=RADIUS,
        color=BLACK,
        stroke_width=STROKE_WIDTH,
        fill_color=PROP_COLOR,
        fill_opacity=1
    ).add(MathTexWrapper(r"\bar{e}")).set_z_index(99)\
     .next_to(e, LEFT, buff=HOR_DIST)

    # --- EDGES (default z, they can go under nodes because nodes are 99) ---
    edges = VGroup(
        fixed_arrow_graph(d, s_node.get_left() + UP * 0.1, color=BLACK),    # 0
        fixed_arrow_graph(p, s_node.get_left(), color=BLACK),               # 1
        fixed_arrow_graph(a, s_node.get_left() + DOWN * 0.1, color=BLACK),  # 2
        
        fixed_arrow_graph(xc, p.get_left(), color=BLACK),                   # 3

        fixed_arrow_graph(f, xc.get_left(), color=BLACK),                   # 4

        fixed_arrow_graph(e, xd.get_left(), color=BLACK),                   # 5
        fixed_arrow_graph(xd, d.get_left(), color=RED),                     # 6

        fixed_arrow_graph(b, xa.get_left() + UP * 0.1, color=BLACK),        # 7
        fixed_arrow_graph(t, xa.get_left() + DOWN * 0.1, color=BLACK),      # 8
        fixed_arrow_graph(xa, a.get_left(), color=RED),                     # 9

        fixed_arrow_graph(c, t.get_left(), color=BLACK),                    # 10

        fixed_arrow_graph(xe, e.get_left(), color=RED),                     # 11

        curved_arrow(xc.get_bottom(), c.get_right() + 0.1 * DOWN + 0.2 * RIGHT, bend=1, color=RED), # 12
    )


    # --- HIGHLIGHT BOXES (preserving your z orders) ---

    # this was .set_z_index(3) in your anim
    proponent_core = highlight_box(
        VGroup(s_node, d, p, a),
        fill_opacity=1,
        fill_color=PROP_COLOR,
        buff=0.1,
        dashed=False
    ).set_z_index(3)

    # these two were set_z_index(0)
    e_xd_block = highlight_box(
        VGroup(e, xd),
        fill_opacity=1,
        fill_color=DEFEAT_COLOR,
        buff=0.1,
        dashed=False
    ).set_z_index(0)

    t_b_xa_block = highlight_box(
        VGroup(t, b, xa),
        fill_opacity=1,
        fill_color=OPPONENT_COLOR,
        buff=0.15,
        dashed=False
    ).set_z_index(3)

    # c_t was set_z_index(5)
    c_t_block = highlight_box(
        VGroup(c, t),
        fill_opacity=1,
        fill_color=DEFEAT_COLOR,
        buff=0.1,
        dashed=False
    ).set_z_index(5)

    # opp_arg had no z in your code, leave default
    opp_arg_block = highlight_box(
        VGroup(c_t_block, b, xa),
        fill_opacity=1,
        fill_color=OPPONENT_COLOR,
        buff=0.3,
        dashed=False
    )
    # xc_p was set_z_index(4)
    xc_p_block = highlight_box(
        VGroup(xc, p),
        fill_opacity=1,
        fill_color=PROP_COLOR,
        buff=0.15,
        dashed=False
    ).set_z_index(4)

    # f_xc was set_z_index(5)
    f_xc_block = highlight_box(
        VGroup(f, xc),
        fill_opacity=1,
        fill_color=PROP_COLOR,
        buff=0.1,
        dashed=False
    ).set_z_index(5)

    # s_arg was set_z_index(0)
    s_arg_block = highlight_box(
        VGroup(f, s_node, d, a),
        fill_opacity=1,
        fill_color=PROP_COLOR,
        buff=0.3,
        dashed=False
    ).set_z_index(0)

    diagram = VGroup(
        # highlights first (bottom layers)
        # nodes
        s_node, d, p, a,  # s <- d,p,a
        edges[0:3],
        proponent_core,
        # s_arg_block,  # show P argument
        xd, e,            # xd <- e
        edges[5],    
        edges[6],      # show attack

        xa, b, t,      # xa <-b,t
        edges[7:9],
        t_b_xa_block,
        edges[9],      # show attack

        c,
        edges[10],      # t <-c
        opp_arg_block,

        xc,
        edges[3],      # 
        xc_p_block,

        f,
        edges[4],      # 
        f_xc_block,
        s_arg_block,
        curved_arrow(xc.get_bottom(), c.get_right() + 0.1 * DOWN + 0.2 * RIGHT, bend=1, color=RED), # 12
        c_t_block,

        xe,
        edges[11],
        e_xd_block

        # xc,
        # edges[3],
        # f,
        # edges[4],




        
        # xc,
        # edges[3], 
        # f, xd, e, xa, b, t, c, xe,
        # # edges
        # edges,
        # e_xd_block,
        # t_b_xa_block,
        # c_t_block,
        # opp_arg_block,
        # xc_p_block,
        # f_xc_block,
        # proponent_core,

    ).move_to(ORIGIN)

    return diagram
