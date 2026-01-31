import textwrap

from manim import *
from manim.mobject.geometry.line import Line

from slides.shared.colors import HIGH_COLOR, GREEN_PASTEL
# from slides.shared.wrappers import TexWrapper

FONT_SIZE_TEXT = 32


def ind_edge(edg):
    return [Indicate(edg[1][0], color=GREEN_PASTEL, scale_factor=1.05), Indicate(edg[0], color=HIGH_COLOR, scale_factor=1)]



def boxed(*mobj, color=BLUE, pad=0.2, width=None, buff=0.5):
    group = VGroup(*mobj).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    ul = group.get_corner(UL) + LEFT*pad + UP*pad
    w = width or (config.frame_width - 5)
    h = group.height + 2*pad
    rect = Rectangle(width=w, height=h).set_stroke(color, width=2) #.set_fill(color, 0.2)
    rect.align_to(ul, UL)
    group.align_to(rect, UL).shift(DOWN*pad+RIGHT*pad)
    return VGroup(rect, group)



def labeled_node(text, pos, max_text_width=25, padding=0.4, color=BLACK, aligned_edge=LEFT):
    # wrap into lines of at most N characters (rough control)
    wrapped = "\n".join(textwrap.wrap(text, width=max_text_width))
    label = Paragraph(wrapped, alignment="center", color=BLACK, font_size=13)

    box = RoundedRectangle(
        corner_radius=0.05,
        width=label.width + padding,
        height=label.height + padding,
        stroke_width=1,
        color=color,
        # fill_color=[WHITE, GRAY],   # gradient colors
        fill_color=[WHITE, "#D4FAFA"],  # nearly white, slightly gray
        # fill_gradient=(WHITE, WHITE, "#f2f2f2"),  # top white, bottom light gray
        fill_opacity=1
    )
    group = VGroup(box, label).move_to(pos, aligned_edge=aligned_edge)
    return group


def edge_between(src, dst, out_dir=RIGHT, in_dir=LEFT, color=BLACK, label_text=None, font_size=14):
    # endpoints
    if np.allclose(out_dir, RIGHT):  start = [src.get_right()[0],  src.get_center()[1], 0]
    elif np.allclose(out_dir, LEFT): start = [src.get_left()[0],   src.get_center()[1], 0]
    elif np.allclose(out_dir, UP):   start = [src.get_center()[0], src.get_top()[1],    0]
    else:                            start = [src.get_center()[0], src.get_bottom()[1], 0]

    if np.allclose(in_dir, RIGHT):   end = [dst.get_right()[0],  dst.get_center()[1], 0]
    elif np.allclose(in_dir, LEFT):  end = [dst.get_left()[0],   dst.get_center()[1], 0]
    elif np.allclose(in_dir, UP):    end = [dst.get_center()[0], dst.get_top()[1],    0]
    else:                            end = [dst.get_center()[0], dst.get_bottom()[1], 0]

    edge = Line(start, end, color=color, stroke_width=1.5).add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=0.15, tip_width=0.15)
    if not label_text:
        return edge

    # centered label box with white fill + border
    # mid = (np.array(start) + np.array(end)) / 2
    mid = np.array(start) * 0.6 + np.array(end) * 0.4
    txt = Tex(r'\texttt{' + label_text + r'}', font_size=font_size, color=color)
    box = RoundedRectangle(corner_radius=0.07, width=txt.width+0.25, height=txt.height+0.18,
                           color=color, fill_color=WHITE, fill_opacity=1,  stroke_width=1)
    lbl = VGroup(box, txt).move_to(mid)
    return VGroup(edge, lbl)


def highlight_box(obj, color_border=BLACK, fill_color=YELLOW, fill_opacity=0.35,
                  buff=0.0, stroke_width=1.5, dashed=False, num_dashes=50):
    bg = BackgroundRectangle(
        obj,
        color=color_border,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        buff=buff
    ).set_z_index(0)

    rect = SurroundingRectangle(
        obj,
        color=color_border,
        buff=buff,
        stroke_width=stroke_width
    ).set_z_index(0)

    if dashed:
        rect = DashedVMobject(rect, num_dashes=num_dashes)

    return VGroup(bg, rect)

