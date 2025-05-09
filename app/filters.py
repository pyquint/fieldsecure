import re

import jinja2
import numpy as np
from flask import Blueprint
from sympy.abc import mu

# https://stackoverflow.com/a/24435908
bp = Blueprint("filters", __name__)


@bp.app_template_filter()
def join(lst: list[int], sep=","):
    return sep.join(map(str, lst))


@bp.app_template_filter()
def nptl(nparray: np.ndarray):
    return mu.np_to_latex(nparray)


@bp.app_template_filter()
def tex_escape(text: str):
    # https://stackoverflow.com/a/25875504

    """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }

    regex = re.compile(
        "|".join(
            re.escape(str(key))
            for key in sorted(conv.keys(), key=lambda item: -len(item))
        )
    )

    return regex.sub(lambda match: conv[match.group()], text)
