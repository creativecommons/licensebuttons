# genicons.py - generate all the icons.
# Copyright 2016 Creative Commons Corporation.

# Standard library
import errno
import math
import os
import os.path

# Third-party
import cairo
import gi
gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo as pangocairo
from functools import reduce


SUITES = {
    "l": {
        "by": ["b"],
        "by-nc": ["bn", "be", "by"],
        "by-nd": ["bd"],
        "by-sa": ["ba"],
        "by-nc-nd": ["bnd", "bed", "byd"],
        "by-nc-sa": ["bna", "bea", "bya"],
    },
    "p": {"cc-zero": ["0"], "public-domain-mark": ["p"]},
}

DIMENSIONS = ((88, 31, 31, 1), (80, 15, 15, 4), (76, 22, 22, 1))

BACKGROUNDS = (
    "transparent",
    "000000",
    # Bootstrap well grey
    "eeeeee",
    "ffffff",
)

STEPS = ["00", "11", "22", "33", "66", "99", "ff"]

FOREGROUNDS = [
    "%s%s%s" % (r, g, b) for r in STEPS for g in STEPS for b in STEPS
]

HEX_TO_FLOAT = 1.0 / 255.0


def hex_to_float(digits):
    return HEX_TO_FLOAT * int(digits, 16)


def set_color(ctx, color_string):
    if color_string == "transparent":
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
    else:
        ctx.set_source_rgb(
            hex_to_float(color_string[0:2]),
            hex_to_float(color_string[2:4]),
            hex_to_float(color_string[4:6]),
        )


def size_chars(ctx, chars):
    # x, y, width, height, dx, dy
    return [ctx.text_extents(char) for char in chars]


def show_chars(ctx, chars, foreground, padding, width, height):
    sizes = size_chars(ctx, chars)
    total_padding = padding * (len(chars) - 1)
    total_width = reduce(lambda x, y: y[3] + x, sizes, 0.0)
    x = 0.5 + math.ceil((width / 2) - ((total_width + total_padding) / 2))
    y = math.ceil(height / 2) + math.floor(sizes[0][3] / 2)
    set_color(ctx, foreground)
    for char, size in zip(chars, sizes):
        ctx.move_to(math.ceil(x), math.ceil(y))
        ctx.show_text(char)
        x += size[2] + padding
    ctx.stroke()


def create_context(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    return ctx


def set_background(ctx, background, width, height):
    set_color(ctx, background)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()


def configure_font(ctx, size):
    ctx.select_font_face("CC Icons")
    ctx.set_font_size(size)


def icon_filename(dimensions, characters):
    filename = "%ix%i" % (dimensions[0], dimensions[1])
    if "y" in characters:
        filename += "-y"
    elif "e" in characters:
        filename += "-e"
    return filename + ".png"


def icon_path(suite, descriptor, background, foreground):
    foreground_path = os.path.join(
        foreground[0:2], foreground[2:4], foreground[4:6]
    )
    return os.path.join(suite, descriptor, background, foreground_path)


def genicon(
    suite,
    characters,
    font_size,
    padding,
    width,
    height,
    background,
    foreground,
):
    ctx = create_context(width, height)
    set_background(ctx, background, width, height)
    configure_font(ctx, font_size)
    show_chars(ctx, characters, foreground, padding, width, height)
    return ctx


font_map = pangocairo.font_map_get_default()
font_families = [family.get_name() for family in font_map.list_families()]
if "CC Icons" not in font_families:
    raise Exception(
        "CC Icons font not installed. See" " <https://wiki.debian.org/Fonts>."
    )

script_dir = os.path.dirname(__file__)
basedir = os.path.realpath(
    os.path.abspath(os.path.join(script_dir, "..", "www", "i"))
)
print("# basedir:", basedir)

for suite, licenses in SUITES.items():
    for lic, module_chars in licenses.items():
        for chars in module_chars:
            for dimensions in DIMENSIONS:
                for background in BACKGROUNDS:
                    for foreground in FOREGROUNDS:
                        # e.g. white on white
                        if foreground == background:
                            continue
                        path = os.path.realpath(
                            os.path.abspath(
                                os.path.join(
                                    basedir,
                                    icon_path(
                                        suite, lic, background, foreground
                                    ),
                                )
                            )
                        )
                        filepath = os.path.realpath(
                            os.path.abspath(
                                os.path.join(
                                    path, icon_filename(dimensions, chars)
                                )
                            )
                        )
                        if os.path.exists(filepath):
                            continue
                        width = dimensions[0]
                        height = dimensions[1]
                        font_size = dimensions[2]
                        padding = dimensions[3]
                        ctx = genicon(
                            suite,
                            chars,
                            font_size,
                            padding,
                            width,
                            height,
                            background,
                            foreground,
                        )
                        try:
                            os.makedirs(path)
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
                        # Will raise and exception on error
                        ctx.get_target().write_to_png(filepath)
