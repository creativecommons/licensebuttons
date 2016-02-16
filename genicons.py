# genall.py - generate all the icons.
# Copyright 2016 Creative Commons Corporation.

import errno, math, os
import cairo, pangocairo

SUITES = {"l": {"by": ["b"],
                "by-nc": ["bn", "be", "by"],
                "by-nd": ["bd"],
                "by-sa": ["ba"],
                "by-nc-nd": ["bnd", "bed", "byd"],
                "by-nc-sa": ["bna", "bea", "bya"]},
          "p": {"cc-zero": ["0"],
                "public-domain-mark": ["p"]}}

DIMENSIONS = ((88, 31, 31, 1),
               (80, 15, 15, 4),
               (76, 22, 22, 1))

BACKGROUNDS = ("transparent",
               "000000",
               # Bootstrap well grey
               "eeeeee",
               "ffffff")

# 255 isn't an 8 offset
STEPS = list(range(0, 249, 8)) + [255]

# These will be generated in the colors anyway
#def greys ():
#    return ["%02x%02x%02x" % (x, x, x) for x in STEPS]

def colors ():
    return ["%02x%02x%02x" % (r, g, b)
            for r in STEPS
            for g in STEPS
            for b in STEPS]

FOREGROUNDS = colors() # + greys()

HEX_TO_FLOAT = 1.0 / 255.0

def hexToFloat (digits):
    return HEX_TO_FLOAT * int(digits, 16)

def setColor (ctx, color_string):
    if color_string == 'transparent':
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
    else:
        ctx.set_source_rgb(hexToFloat(color_string[0:2]),
                            hexToFloat(color_string[2:4]),
                            hexToFloat(color_string[4:6]))

def sizeChars (ctx, chars):
    # x, y, width, height, dx, dy
    return [ctx.text_extents(char) for char in chars]

def showChars (ctx, chars, foreground, padding, width, height):
    sizes = sizeChars(ctx, chars)
    total_padding = padding * (len(chars) - 1)
    total_width = reduce(lambda x, y : y[3] + x, sizes, 0.0)
    x = 0.5 + math.ceil((width / 2) - ((total_width + total_padding) / 2))
    y = math.ceil(height / 2) + math.floor(sizes[0][3] / 2)
    setColor(ctx, foreground)
    for char, size in zip(chars, sizes):
        ctx.move_to(math.ceil(x), math.ceil(y))
        ctx.show_text(char)
        x += size[2] + padding
    ctx.stroke()

def createContext (width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    ctx = pangocairo.CairoContext(context)
    return ctx

def setBackground (ctx, background, width, height):
    setColor(ctx, background)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

def configureFont (ctx, size):
    ctx.select_font_face('CC Icons')
    ctx.set_font_size(size)

def iconFilename (dimensions, characters):
    filename = "%ix%i" % (dimensions[0], dimensions[1])
    if ('y' in characters):
        filename += '-y'
    elif ('e' in characters):
        filename += '-e'
    return filename + '.png'

def iconPath (suite, descriptor, background, foreground):
    foreground_path = os.path.join(foreground[0:2], foreground[2:4],
                                   foreground[4:6])
    return os.path.join(suite, descriptor, background, foreground_path)

def genicon (suite, characters, font_size, padding, width, height, background,
             foreground):
    ctx = createContext(width, height)
    setBackground(ctx, background, width, height)
    configureFont(ctx, font_size)
    showChars(ctx, characters, foreground, padding, width, height)
    return ctx

basedir = 'build' #os.path.join(os.getcwd(), 'build')

for suite, licenses in SUITES.iteritems():
    for lic, module_chars in licenses.iteritems():
        for chars in module_chars:
            for dimensions in DIMENSIONS:
                for background in BACKGROUNDS:
                    for foreground in FOREGROUNDS:
                        # e.g. white on white
                        if foreground == background:
                            continue
                        width = dimensions[0]
                        height = dimensions[1]
                        font_size = dimensions[2]
                        padding = dimensions[3]
                        ctx = genicon(suite, chars, font_size, padding,
                                      width, height, background, foreground)
                        path = os.path.join(basedir, iconPath(suite,
                                                              lic,
                                                              background,
                                                              foreground))
                        try:
                            os.makedirs(path)
                        except OSError, exception:
                            if exception.errno != errno.EEXIST:
                                raise
                        filepath = os.path.join(path,
                                                iconFilename(dimensions,
                                                             chars))
                        # Will raise and exception on error
                        ctx.get_target().write_to_png(filepath)
