import time

PAD_W = 1.524
PAD_H = 2.286
PAD_DRILL = 1.

def gen_fp (f, name, npins, model=None):
    """Generate a header connector given an output file to receive the
    footprint, a footprint name, and a number of pins.
    """

    f.write ("(module %s (layer F.Cu) (tedit %08X)\n" % (name, time.time ()))
    f.write ("  (fp_text reference REF** (at 0 0) (layer F.SilkS)\n")
    f.write ("    (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    f.write ("  )\n")
    f.write ("  (fp_text value %s (at 0 0) (layer F.Fab)\n" % name)
    f.write ("    (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    f.write ("  )")


    pin_left = -(2.54 * (npins - 1)) / 2
    pin_right = -pin_left
    
    cyard_left = pin_left - 1.905
    cyard_right = pin_right + 1.905
    cyard_top = -1.905
    cyard_bottom = 1.905

    # Three boxes: courtyard, fab, silk
    for layer, width in [("F.CrtYd", 0.15), ("F.Fab", 0.15), ("F.SilkS", 0.35)]:
        f.write ("  (fp_line (start %f %f) (end %f %f) (layer %s) (width %f))\n" %
                    (cyard_left, cyard_top, cyard_right, cyard_top, layer, width))
        f.write ("  (fp_line (start %f %f) (end %f %f) (layer %s) (width %f))\n" %
                    (cyard_right, cyard_top, cyard_right, cyard_bottom, layer, width))
        f.write ("  (fp_line (start %f %f) (end %f %f) (layer %s) (width %f))\n" %
                    (cyard_right, cyard_bottom, cyard_left, cyard_bottom, layer, width))
        f.write ("  (fp_line (start %f %f) (end %f %f) (layer %s) (width %f))\n" %
                    (cyard_left, cyard_bottom, cyard_left, cyard_top, layer, width))

    # Silkscreen line separating pin 1 from pin 2
    sep_x = (2*pin_left + 2.54) / 2
    f.write ("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.35))\n" %
                (sep_x, cyard_top, sep_x, cyard_bottom))
    f.write ("  (fp_line (start %f %f) (end %f %f) (layer F.Fab) (width 0.15))\n" %
                (sep_x, cyard_top, sep_x, cyard_bottom))

    # Silkscreen line under pin 1
    p1mark_y = cyard_bottom + 0.635
    f.write ("  (fp_line (start %f %f) (end %f %f) (layer F.SilkS) (width 0.15))\n" %
                (cyard_left, p1mark_y, sep_x, p1mark_y))

    # Pads
    for i in range (1, npins + 1):
        if i == 1:
            shape = "rect"
        else:
            shape = "oval"
        pad_x = pin_left + (2.54 * (i - 1))
        f.write ("  (pad %d thru_hole %s (at %f 0) (size %f %f) (drill %f) (layers *.Cu *.Mask F.SilkS))\n" %
                (i, shape, pad_x, PAD_W, PAD_H, PAD_DRILL))

    if model is not None:
        f.write ("  (model %s\n" % model)
        f.write ("    (at (xyz 0 0 0))\n")
        f.write ("    (scale (xyz 1 1 1))\n")
        f.write ("    (rotate (xyz 0 0 0))\n")
        f.write ("  )\n")

    f.write (")\n")

for i in range (1, 25):
    fpname = "CONN-100MIL-F-1x%d" % i
    model = "pin_strip/pin_socket_%d.wrl" % i
    with open (fpname + ".kicad_mod", 'w') as f:
        gen_fp (f, fpname, i, model)

for i in range (1, 25):
    fpname = "CONN-100MIL-M-1x%d" % i
    model = "pin_strip/pin_strip_%d.wrl" % i
    with open (fpname + ".kicad_mod", 'w') as f:
        gen_fp (f, fpname, i, model)
