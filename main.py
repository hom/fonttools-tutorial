import os
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

dirname = pathlib.Path(os.getcwd(), "fonts")


def glyph_to_svg(font_path, character, output_svg_path):
    # 打开字体文件
    font = TTFont(font_path)

    # 获取 'glyf' 表
    glyf_table = font.get("glyf")
    glyph_set = font.getGlyphSet()

    # 获取unicode编码
    unicode_code_point = ord(character)
    # 获取glyf表的字形名称
    glyph_name = font.getBestCmap().get(unicode_code_point, None)

    # 检查字符是否存在
    if glyph_name not in glyf_table.glyphs:
        raise ValueError(f"Glyph '{glyph_name}' not found in font.")

    # 获取指定 Glyph 的路径
    glyph = glyph_set[glyph_name]
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)

    # 获取 SVG 路径数据
    svg_path_data = pen.getCommands()

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
        <path d="{svg_path_data}" stroke="red" fill="none" transform="scale(1, -1)" />
    </svg>"""

    # 创建 SVG 文件并写入路径数据
    with open(output_svg_path, "w") as svg_file:
        svg_file.write(svg)


# 示例调用
glyph_to_svg(dirname / "simsun.ttf", "孟", "output.svg")
