#!/usr/bin/env python3
# Portions adapted from fonttools ttx.py

from fontTools.ttLib import TTFont

def ttxconv(font_file):
    font_file_sp = font_file.split(".")
    font_file_ttx = ".".join(font_file_sp[:-1]) + ".ttx"
    print(" ** Converting: %s -> %s" % (font_file, font_file_ttx))
    ttf = TTFont(font_file, 0, allowVID=False, ignoreDecompileErrors=True, fontNumber=-1)
    ttf.saveXML(font_file_ttx, splitTables=False, disassembleInstructions=True, bitmapGlyphDataFormat="raw", newlinestr=None)
    ttf.close()
    return font_file_ttx
