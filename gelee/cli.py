#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
""""Validate configuration files against their format and maybe schema."""
import pathlib
import os
import sys

import gelee.gelee as lint

DEBUG_VAR = "MARMELADE_DEBUG"
DEBUG = bool(os.getenv(DEBUG_VAR))


# pylint: disable=expression-not-assigned
def main(argv=None, debug=None):
    """Dispatch processing of the job.
    This is the strings only command line interface.
    For python API use interact with lint functions directly.
    """
    argv = sys.argv[1:] if argv is None else argv
    debug = debug if debug else DEBUG
    for arg in argv:
        if not pathlib.Path(arg).is_file() and not pathlib.Path(arg).is_dir():
            print("ERROR: For now only paths understood.")
            sys.exit(2)

    return lint.main(argv, debug=debug)
