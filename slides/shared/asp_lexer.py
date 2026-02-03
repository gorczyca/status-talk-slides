from manim import *
from manim_slides import Slide
from pathlib import Path



from pygments.lexer import RegexLexer
from pygments.token import Keyword, Name, Number, String, Operator, Comment, Text
# from pygments.lexers import register
import manim.mobject.text.code_mobject as cm
import pygments.lexers as pyg_lex


from pygments.styles import STYLE_MAP


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
            (r"[A-Z][A-Za-z0-9_]*", Name.Builtin),
            (r"[a-z][A-Za-z0-9_]*", Name.Function),
            (r"\d+", Number),
            (r'"[^"]*"', String),
            # (r"[(),.\[\]{};:<>]", Punctuation),
            (r"[(),.\[\]{}]", Operator),
            (r"\s+", Text),
        ],
    }


def set_asp_lexer():
    _orig = pyg_lex.get_lexer_by_name


    def _asp_get(alias, **opts):
        return ASPLexer(**opts) if alias.lower() in ("asp", "clingo") else _orig(alias, **opts)


    pyg_lex.get_lexer_by_name = _asp_get
    cm.get_lexer_by_name = _asp_get


def get_asp_code(code_path, font_size=24, add_line_numbers=False, buff=0.2, line_numbers_from=1):
        code = Code(
            tab_width=2,
            code_string=Path(code_path).read_text(encoding="utf-8"),
            language='asp',
            # padding=padding,
            add_line_numbers=add_line_numbers,
            line_numbers_from=line_numbers_from,
            # font_size=font_size,
            paragraph_config={"font_size": font_size},
            background_config={"buff": buff},
            # line_spacing=line_spacing,        # tighter vertically
            formatter_style='one-dark'  # tried with perldoc, gruvbox-dark, vs, dracula, one-dark, monokai, nord-darker, paraiso-dark, solarized-dark, coffee, github-dark, stata-dark
        )
        # code.background..stretch_to_fit_width(width)
        return code


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