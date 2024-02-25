from pathlib import Path
import shutil

import cairo

from texnomagic.abcs import TexnoMagicAlphabets

from wopweb.config import cfg


def export_drawing(symbol, out, res=1000, format='svg'):
    drawing = symbol.random_drawing()
    if not drawing:
        return False

    if format == 'png':
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, res, res)
    else:
        surface = cairo.SVGSurface(out, res, res)

    ctx = cairo.Context(surface)

    ctx.scale(res, res)
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


def draw_images(outpath, abcs=None, abcs_tag=None, format='svg'):
    if not abcs:
        abcs = TexnoMagicAlphabets()
        abcs.load()
    if not abcs_tag:
        abcs_tag = cfg.abcs_tag

    images_path = Path(outpath) / 'img'
    symbols_path = images_path / 'symbols'

    symbols_path.mkdir(parents=True, exist_ok=True)

    n = 0
    missing = []
    for abc in abcs.abcs.get(abcs_tag):
        abc_path = symbols_path / abc.handle
        abc_path.mkdir(exist_ok=True)
        for symbol in abc.symbols:
            out_path = abc_path / f"{symbol.meaning}.{format}"
            image_path = symbol.get_image_path(format=format)
            if image_path.exists():
                print(f"COPY: {image_path} -> {out_path}")
                shutil.copy(image_path, out_path)
            else:
                print(f"DRAW: {out_path}")
                if export_drawing(symbol, out_path, format=format):
                    n += 1
                else:
                    print(f"  ERROR: no image for {symbol.meaning}")
                    missing.append(f"{abc.handle}/{symbol.meaning}")

    print(f"\n{n} symbols drawn 🖼")
    if missing:
        mstr = ", ".join(missing)
        print(f"\n{len(missing)} missing: {mstr}")
