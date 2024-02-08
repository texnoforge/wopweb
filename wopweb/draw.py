from pathlib import Path

import cairo

from texnomagic.abcs import TexnoMagicAlphabets


def draw_symbol(symbol, out, format='svg'):
    drawing = symbol.random_drawing()
    if not drawing:
        return False

    if format == 'png':
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 640, 640)
    else:
        surface = cairo.SVGSurface(out, 640, 640)

    ctx = cairo.Context(surface)

    ctx.scale(640, 640)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    ctx.fill()

    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.set_line_width(0.03)
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_line_join(cairo.LineJoin.ROUND)
    for curve in drawing.curves_fit_area([0.05, 0.05], [0.9, 0.9]):
        x, y = curve[0]
        ctx.move_to(x, y)
        for x, y in curve[1:]:
            ctx.line_to(x, y)
        ctx.stroke()

    if format == 'png':
        surface.write_to_png(out)

    surface.finish()
    surface.flush()
    return True


def draw_images(outpath, abcs=None, format='svg'):
    if not abcs:
        abcs = TexnoMagicAlphabets()
        abcs.load()

    images_path = Path(outpath) / 'img'
    symbols_path = images_path / 'symbols'

    symbols_path.mkdir(parents=True, exist_ok=True)

    n = 0
    for abc in abcs.abcs.get('tags'):
        abc_path = symbols_path / abc.handle
        abc_path.mkdir(exist_ok=True)
        for symbol in abc.symbols:
            symbol_path = abc_path / f"{symbol.meaning}.{format}"
            print(f"DRAW: {symbol_path}")
            draw_symbol(symbol, symbol_path, format=format)
            n += 1

    print(f"\n{n} symbols drawn 🖼")
