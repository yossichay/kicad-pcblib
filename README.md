kicad-pcblib
============

(Warning: Work in progress!)

These are my KiCad PCB libraries, meant to be used with my schematic
libraries: https://github.com/cpavlin1/kicad-schlib


IPC footprints
--------------

The IPC footprints are auto-generated from the FreePCB IPC libraries.

Requires Make and Python 2.7+/3. Just run 'make' after cloning this repository;
the makefile will download the FreePCB IPC libraries and convert them to KiCad
.pretty libs. Note that I am not distributing the FreePCB libraries, but I
could (as they're covered by GPL); if they ever become unavailable I will add
them here.

3D models
---------

The footprints reference [these nice 3D models](http://smisioto.no-ip.org/elettronica/kicad/kicad-en.htm).
There is a Python script to download and extract them; just run 'make 3d' to
run it.

They're pretty big, so please don't pull them repeatedly. Be nice to his server.
