# Written in 2015 by Chris Pavlina
# CC0 1.0 Universal

# KiCad/pcbnew footprint export library

import time

DEFAULT_LINE_WIDTH = 0.35

class SexpSymbol (object):
    """An s-expression symbol. This is a bare text object which is exported
    without quotation or escaping. Be careful to use valid text here..."""

    def __init__ (self, s):
        self.s = s

    def __str__ (self):
        return self.s

# For short code
S = SexpSymbol

def SexpDump (sexp, f, indentlevel=0):
    """Dump an s-expression to a file.
    indentlevel is used for recursion.
    """

    if isinstance (sexp, list):
        f.write ("(")
        first = True
        for i in sexp:
            if first:
                first = False
            else:
                f.write (" ")

            SexpDump (i, f, indentlevel + 1)
        f.write (")")

    elif isinstance (sexp, str):
        f.write ('"')
        f.write (sexp.encode ("unicode_escape").decode ("ascii"))
        f.write ('"')

    else:
        f.write (str (sexp))

class PCBmodule(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.graphics = []
        self.threed = None

    def sexp(self):
        sexp = [S('module')]

        sexp.append (self.name)
        sexp.append ([S("layer"), "F.Cu"])
        sexp.append ([S("tedit"), "%08X" % int (time.time ())])

        sexp.append ([S("descr"), str(self.description)])

        sexp.append ([S("fp_text"),
            S("reference"), "REF**",
            [S("at"), 0, 0],
            [S("layer"), "F.SilkS"],
            [S("effects"),
                [S("font"),
                    [S("size"), 0.8, 0.8],
                    [S("thickness"), 0.15]]]])

        sexp.append ([S("fp_text"),
            S("value"), self.name,
            [S("at"), 0, 0],
            [S("layer"), "F.Fab"],
            [S("effects"),
                [S("font"),
                    [S("size"), 0.8, 0.8],
                    [S("thickness"), 0.15]]]])

        # Polylines
        for i in self.graphics:
            if not isinstance (i, Polyline): continue
            sexp.extend (i.sexp ())

        # Pads/pins
        for i in self.graphics:
            if not isinstance (i, Pad): continue
            sexp.extend (i.sexp ())

        # 3D
        if self.threed is not None:
            sexp.append(self.threed.sexp())

        return sexp

class ThreeD(object):
    def __init__(self, model, offset, scale, rotation):
        self.model = model
        self.offset = offset
        self.scale = scale
        self.rotation = rotation
    def sexp(self):
        return [S("model"), self.model,
            [S("at"), [S("xyz")] + self.offset],
            [S("scale"), [S("xyz")] + self.scale],
            [S("rotate"), [S("xyz")] + self.rotation]]

class Polyline(object):
    def __init__(self):
        self.linewidth = DEFAULT_LINE_WIDTH
        self.points = []
        self.layer = "F.SilkS"

    def sexp(self):
        sexp = []
        last_corner = self.Points[0]
        for i in self.Points[1:]:
            sexp.append ([S("fp_line"),
                [S("start"), to_mm (last_corner[0]), to_mm (-last_corner[1])],
                [S("end"), to_mm (i[0]), to_mm (-i[1])],
                [S("layer"), self.Layer],
                [S("width"), self.KicadLinewidth]])
            last_corner = i

        return sexp

class Pad(object):
    def __init__(self):
        self.drill = 0
        self.name = "1"
        self.sx = 0
        self.sy = 0
        self.x = 0
        self.y = 0
        self.kind = "smd"   # smd, thru_hole
        self.shape = "rect" # rect, oval, circle
        self.layers = ["F.Cu", "F.Paste", "F.Mask"]

    def sexp(self):
        sexp = [S("pad"), self.name, S(self.kind), S(self.shape),
                [S("at"), self.x, self.y],
                [S("size"), self.sx, self.sy]]
        if self.drill != 0:
            sexp.append([S("drill"), self.drill])
        sexp.append([S("layers")] + self.layers)
        return sexp
