#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
""""Validate configuration files against their format and maybe schema."""
import pathlib
import os
import sys

import gelee.gelee as lint

DEBUG_VAR = "GELEE_DEBUG"
DEBUG = bool(os.getenv(DEBUG_VAR))

ABORT_VAR = "GELEE_ABORT"
ABORT = bool(os.getenv(ABORT_VAR))


# pylint: disable=expression-not-assigned
def main(argv=None, abort=None, debug=None):
    """Dispatch processing of the job.
    This is the strings only command line interface.
    For python API use interact with lint functions directly.
    """
    argv = sys.argv[1:] if argv is None else argv
    debug = debug if debug else DEBUG
    abort = abort if abort else ABORT
    for arg in argv:
        if not pathlib.Path(arg).is_file() and not pathlib.Path(arg).is_dir():
            print("ERROR: For now only existing paths accepted.")
            sys.exit(2)

    code, _ = lint.main(argv, abort=abort, debug=debug)
    return code
