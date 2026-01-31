from manim import *

from slides.shared.common import labeled_node, edge_between, FONT_SIZE_TEXT

from slides.shared.colors import HIGH_COLOR, GREEN_PASTEL, D_BLUE, LAT_ORANGE

TEX_TEMPLATE_LOC = 'assets/preamble.tex'
FONT = 'Noto Sans'



def get_tex_template():
    custom_template = TexTemplate()
    custom_template.tex_compiler = 'xelatex'
    custom_template.output_format = ".xdv"


    
    with open(TEX_TEMPLATE_LOC) as f:
        preamble = f.read()
        
        print(preamble)
        custom_template.add_to_preamble(preamble)
        
        # custom_template.tex_compiler = 'xelatex'
        
        return custom_template


class MathTexWrapper(MathTex):
    FONT_SIZE = 35
    FONT_COLOR = BLACK
    TEX_TEMPLATE = get_tex_template()
    
    def __init__(self, *tex_strings, color=FONT_COLOR, font_size=FONT_SIZE,
                 tex_template=TEX_TEMPLATE, **kwargs):
        super().__init__(*tex_strings, color=color, font_size=font_size,
                         tex_template=tex_template, **kwargs)


class TextWrapper(Text):
    FONT_SIZE = 35
    FONT_COLOR = BLACK
    

    def __init__(self, text, **kwargs):
        kwargs.setdefault("color", self.FONT_COLOR)
        kwargs.setdefault("font_size", self.FONT_SIZE)
        kwargs.setdefault("font", FONT)
        super().__init__(text, **kwargs)



class TexWrapper(Tex):
    FONT_SIZE = 35
    FONT_COLOR = BLACK
    TEX_TEMPLATE = get_tex_template()
    
    def __init__(self, *tex_strings, color=FONT_COLOR, font_size=FONT_SIZE, tex_template=TEX_TEMPLATE):
        super().__init__(*tex_strings, color=color, font_size=font_size, tex_template=tex_template)


# def make_cell(text, width, font_size=16, color=BLACK):
#     return Tex(
#         rf"\raggedright\parbox[t]{{{width}cm}}{{{text.replace('\n','\\\\')}}}",
#         font_size=font_size,
#         color=color,
#     )

class TableWrapper(Table):
    FONT_SIZE = 20
    FONT_COLOR = BLACK
    INCLUDE_OUTER_LINES = True

    def __init__(
        self,
        data,
        *,
        font_size=FONT_SIZE,
        color=FONT_COLOR,
        include_outer_lines=INCLUDE_OUTER_LINES,
        max_width=3,  # cm, wrap text if too long
        **kwargs
    ):
        kwargs.setdefault("h_buff", 0.2)
        kwargs.setdefault("v_buff", 0.2)
        kwargs.setdefault("line_config", {"stroke_width": 1})

        def to_mobj(x):
            if isinstance(x, Mobject):
                return x
            text = str(x).replace("\n", r"\\")
            return Tex(
                rf"\raggedright\parbox[t]{{{max_width}cm}}{{{text}}}",
                font_size=font_size,
                color=color,
            )

        kwargs.setdefault("element_to_mobject", to_mobj)
        super().__init__(data, include_outer_lines=include_outer_lines, **kwargs)
        self.set(color=color)

        # header shading
        n_cols = len(self.get_columns())
        for j in range(1, n_cols + 1):
            self.add_highlighted_cell((1, j), color=GREY_E, fill_opacity=0.1)

        # top-align col_labels
        if getattr(self, "col_labels", None):
            top_y = max(lbl.get_top()[1] for lbl in self.col_labels)
            for lbl in self.col_labels:
                lbl.shift(UP * (top_y - lbl.get_top()[1]))


class IconDocumentStack(VGroup):
    def __init__(
        self,
        sheet_width: float = 4.5,
        sheet_height: float = 2.5,
        top_shrink: float = 0.42,     # < 1 → trapezoid (narrower top edge)
        n_visible_layers: int = 7,
        line_color = "#2E2E2E",
        fill_color = "#EAF2FF",
        edge_color = "#2A3B8F",
        base_band_color = "#2A3B8F",
        **kwargs
    ):
        super().__init__(**kwargs)

        w, h = sheet_width, sheet_height
        shrink = top_shrink

        # --- Top trapezoid polygon
        top_points = [
            [-w/2 * shrink,  h/2, 0],   # top left
            [ w/2 * shrink,  h/2, 0],   # top right
            [ w/2, -h/2, 0],            # bottom right
            [-w/2, -h/2, 0],            # bottom left
        ]
        top_sheet = Polygon(*top_points,
                            stroke_color=edge_color, stroke_width=3,
                            fill_color=fill_color, fill_opacity=1.0)

        # --- Fake "text" lines, aligned to trapezoid perspective
        lines = VGroup()
        n_lines = 10
        margin_x = 0.25
        for i in range(n_lines):
            y = h/2 - 0.3 - i*0.25
            # interpolate width according to trapezoid slope
            frac = (h/2 - y) / h  # 0 at top, 1 at bottom
            half_width = (shrink + (1-shrink)*frac) * w/2
            start = [-half_width+margin_x, y, 0]
            end   = [ half_width-margin_x, y, 0]
            l = Line(start, end, stroke_color=line_color,
                     stroke_opacity=0.8, stroke_width=3)
            lines.add(l)

        # --- Base bands (stack layers)
        bands = VGroup()
        # band_w = w * 0.9
        band_w = w
        band_h = 0.12
        for i in range(n_visible_layers):
            band = Rectangle(width=band_w, height=band_h,
                             stroke_width=0,
                             fill_color=base_band_color,
                             fill_opacity=0.9 if i % 2 == 0 else 0.7)
            band.shift(DOWN*(h/2 + 0.05 + i*(band_h+0.04)))
            bands.add(band)

        self.add(bands, top_sheet, lines)
        self.top_sheet = top_sheet
        self.lines = lines

    def attention_anim(self):
        # small wiggle to draw attention
        return Succession(
            self.animate.rotate(0.03).shift(UP*0.02),
            self.animate.rotate(-0.06).shift(DOWN*0.02),
            self.animate.rotate(0.03)
        )
    

class IconDocument(VGroup):
    def __init__(
        self,
        sheet_width: float = 4.5,
        sheet_height: float = 2.5,
        top_shrink: float = 0.42,
        line_color = "#2E2E2E",
        fill_color = "#EAF2FF",
        edge_color = "#2A3B8F",
        **kwargs
    ):
        super().__init__(**kwargs)

        w, h = sheet_width, sheet_height
        shrink = top_shrink

        top_points = [
            [-w/2 * shrink,  h/2, 0],
            [ w/2 * shrink,  h/2, 0],
            [ w/2, -h/2, 0],
            [-w/2, -h/2, 0],
        ]
        top_sheet = Polygon(
            *top_points,
            stroke_color=edge_color, stroke_width=3,
            fill_color=fill_color, fill_opacity=1.0
        )

        lines = VGroup()
        n_lines = 9
        margin_x = 0.25
        for i in range(n_lines):
            y = h/2 - 0.3 - i*0.25
            frac = (h/2 - y) / h
            half_width = (shrink + (1-shrink)*frac) * w/2
            start = [-half_width+margin_x, y, 0]
            end   = [ half_width-margin_x, y, 0]
            l = Line(start, end, stroke_color=line_color,
                     stroke_opacity=0.8, stroke_width=3)
            lines.add(l)

        self.add(top_sheet, lines)
        self.top_sheet = top_sheet
        self.lines = lines
    
    
class SmallGraph(VGroup):
        def __init__(self, x, y, **kwargs):
            super().__init__(**kwargs)

            centr_x, centr_y = x, y
            # y_delta = 1
            # x_delta = 3

            # positions = [
                # [centr_x, centr_y, ORIGIN, ''],
                # [centr_x-x_delta, centr_y+y_delta, RIGHT, 'hasAnalysedRisk'],
                # [centr_x-x_delta, centr_y, RIGHT, 'hasHazard'],
                # [centr_x-x_delta, centr_y-y_delta, RIGHT, 'hasInitialP1'],
                # [centr_x+x_delta, centr_y+y_delta,  LEFT, 'hasSequenceOfEvents'],
                # [centr_x+x_delta, centr_y,  LEFT, 'hasHazardousSituation'],
                # [centr_x+x_delta, centr_y-y_delta,  LEFT, '...'],
            # ]

            node_1 = labeled_node('', [centr_x, centr_y, 0])
            node_2 = labeled_node('', [centr_x-0.75, centr_y+0.6, 0])
            node_3 = labeled_node('', [centr_x+0.85, centr_y+0.5, 0])
            node_4 = labeled_node('', [centr_x, centr_y-0.8, 0])

            # to be inferred
            node_5 = labeled_node('', [centr_x, centr_y+1, 0], color=D_BLUE)

            edge_1_2 = edge_between(node_1, node_2, out_dir=LEFT, in_dir=RIGHT)
            edge_3_1 = edge_between(node_3, node_1, out_dir=LEFT, in_dir=RIGHT)
            edge_1_4 = edge_between(node_1, node_4, out_dir=DOWN, in_dir=UP)

            edge_1_5 = edge_between(node_1, node_5, out_dir=UP, in_dir=DOWN, color=D_BLUE)


            # central_node = labeled_node('1', [centr_x, centr_y, 0])
            # self.slide.play(Create(central_node[0]), FadeIn(central_node[1]))
            # self.slide.next_slide()
            # graph_elems = [central_node]

            self.add(node_1, node_2, node_3, node_4, edge_1_2, edge_3_1, edge_1_4)
                
            self.to_add = VGroup(edge_1_5, node_5)

            self.to_highlight = [node_1, node_3]
                
            # self.slide.play(FadeOut(hl), run_time=0.2)
            # self.slide.play(VGroup(*graph_elems).animate.scale(0.7).shift(LEFT*3))


# TODO
WIDTH = 13
BUFF=1.5


def bullet_line(text, width=WIDTH, font_size=FONT_SIZE_TEXT):
    bullet = TexWrapper(r"$\bullet$", font_size=font_size)
    body = TexWrapper(
        r"\parbox[t]{%scm}{\sffamily %s}" % (width, text),
        font_size=font_size,
        color=BLACK,
    )
    body.next_to(bullet, RIGHT, aligned_edge=UP, buff=0.25).shift(UP*0.1)
    return VGroup(bullet, body).align_to(bullet, LEFT)

def tex_paragraph(text, width=WIDTH, font_size=FONT_SIZE_TEXT, color=BLACK):
    return TexWrapper(
        r"\parbox[t]{%scm}{\sffamily %s}" % (width, text),
        font_size=font_size,
        color=color,
    )


def enum_line(num, text, width=WIDTH, font_size=FONT_SIZE_TEXT):
    label = TexWrapper(rf"\textsf{{{num}.}}", font_size=font_size)
    body = TexWrapper(
        r"\parbox[t]{%scm}{\sffamily %s}" % (width, text),
        font_size=font_size,
        color=BLACK,
    )
    body.next_to(label, RIGHT, aligned_edge=UP, buff=0.25) #.shift(UP*0.1)
    return VGroup(label, body).align_to(label, LEFT)