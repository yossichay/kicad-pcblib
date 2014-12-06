kicad-pcblib
============

These are my KiCad PCB libraries, meant to be used with my schematic
libraries: https://github.com/cpavlin1/kicad-schlib


IPC footprints
--------------

The IPC footprints are auto-generated from the FreePCB IPC libraries.

Requires Make, Python, and the sexpdata Python module. Just run 'make' after
cloning this repository; the makefile will download the FreePCB IPC libraries and
convert them to KiCad .pretty libs. Note that I am not distributing the FreePCB
libraries, but I could (as they're covered by GPL); if they ever become
unavailable I will add them here.

