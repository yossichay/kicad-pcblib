#!/usr/bin/env python
#!/usr/bin/env python3

# download_ipc

# Copyright 2013, Chris Pavlina
# All rights reserved.
# BSD license.
# c4757p.com/software/kicadlib

# This script downloads the IPC libraries from FreePCB and converts them to
# KiCad format using freepcb2kicad.

import zipfile
import tempfile
import shutil
import imp
import os
import shutil

VERSION = "1.0"

FREEPCB2KICAD_ARGS = ["--blurb", "--rounded-except-1", "--strip-lmn"]

# Py2/3 imports
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

try:
    raw_input
except NameError:
    raw_input = input

try:
    bytes
except NameError:
    bytes = str

# Confirm the FreePCB license
CONFIRMLICENSE_MSG="""\
IPC libraries must be downloaded from FreePCB (www.freepcb.com).
They are covered by the GNU General Public License, version 2 or
later."""
class LicenseException (Exception):
    pass
class ConfirmLicense (object):
    def __init__ (self):
        self.already_confirmed = False
    def __call__ (self):
        if self.already_confirmed:
            return
        print (CONFIRMLICENSE_MSG)
        acc = raw_input ("Do you accept the license? (y/n) ")
        if acc.lower () not in ("y", "yes"):
            raise LicenseException ("License not accepted.")
        self.already_confirmed = True
confirm_license = ConfirmLicense ()


def main ():
    # Get args
    from argparse import ArgumentParser
    description = "Download FreePCB IPC libraries and convert to KiCad " + \
            "format."
    p = ArgumentParser (description=description)
    p.add_argument ("-v", "--version", action="version",
            version="%(prog)s " + VERSION)

    p.add_argument ("src", metavar="SRC", type=str,
            help="URL or path to IPC FreePCB zipfile")

    p.add_argument ("dest", metavar="DEST", type=str,
            help="Path to KiCad output")

    p.add_argument ("fp2kicad", metavar="FP2KICAD", type=str,
            help="Path to freepcb2kicad.py")

    p.add_argument ("--no-confirm-license", dest="no_confirm_license",
            action="store_const", const=True, default=False,
            help="Do not ask the user to accept the GPL")

    p.add_argument ("--3dmap", dest="threedmap", type=str,
            help="Module-3D model map. See freepcb2kicad.py documentation.")

    p.add_argument ("--rounded-pad-exceptions", dest="rpexcept", type=str,
            help="Rounded pad exception file. See freepcb2kicad.py " + \
                    "documentation.")

    args = p.parse_args ()

    if args.threedmap is not None:
        FREEPCB2KICAD_ARGS.extend (["--3dmap", args.threedmap])

    if args.rpexcept is not None:
        FREEPCB2KICAD_ARGS.extend (["--rounded-pad-exceptions", args.rpexcept])

    # Download, if necessary, then open file
    if args.src.startswith ("http:/"):
        if not args.no_confirm_license:
            confirm_license ()
        url = urlopen (args.src)
        try:
            data = url.read ()
        except Exception as e:
            url.close ()
            raise
        else:
            url.close ()
        ipc_f = BytesIO (data) # data is bytes in Py3
    else:
        ipc_f = open (args.src)
    ipc_zip = zipfile.ZipFile (ipc_f)

    # Create a temporary working directory, and extract the IPC files
    # into it.
    tempdir = tempfile.mkdtemp ()

    # Wrap the rest of the code in an exception catcher so we can clean up
    # the files.
    try:
        main_2 (args, tempdir, ipc_zip)
    except:
        try:
            ipc_f.close ()
        except Exception as e:
            print (e)
        try:
            shutil.rmtree (tempdir)
        except Exception as e:
            print (e)
        raise
    else:
        exceptions = []
        try:
            ipc_f.close ()
        except Exception as e:
            exceptions.append (e)
        try:
            shutil.rmtree (tempdir)
        except Exception as e:
            exceptions.append (e)
        for exc in exceptions:
            print exc
        if exceptions:
            raise Exception ("Errors occurred.")

def main_2 (args, tempdir, zipfile):
    # If there is an exception, it will be caught and all working files will
    # be cleaned up.

    # Load freepcb2kicad
    freepcb2kicad = imp.load_source ("freepcb2kicad", args.fp2kicad)

    # Extract all FPL files
    count = 0
    files = []
    for zipmember in zipfile.namelist ():
        if not zipmember.lower ().endswith (".fpl"):
            continue
        destname = os.path.join (tempdir, "%d.fpl" % count)
        count += 1
        files.append (destname)
        with open (destname, 'w') as destfile:
            with zipfile.open (zipmember) as srcfile:
                destfile.write (srcfile.read ())

    # Generate KiCad files
    fpargs = FREEPCB2KICAD_ARGS + [args.dest] + files
    freepcb2kicad.main (fpargs)

if __name__ == "__main__":
    main ()
