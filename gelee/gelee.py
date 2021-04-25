# -*- coding: utf-8 -*-
# pylint: disable=c-extension-no-member,expression-not-assigned,line-too-long,logging-fstring-interpolation
"""Do the lint."""
import json
import logging
import os
import pathlib
import sys
import typing

import jsonschema  # type: ignore
from lxml import etree  # type: ignore


ENCODING = "utf-8"

APP = 'gelee'

LOG = logging.getLogger()  # Temporary refactoring: module level logger
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO


def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global LOG  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level
    }
    logging.basicConfig(**log_format)
    LOG = logging.getLogger(APP if name is None else name)


def visit(tree):
    """Visit tree and yield the leaves."""
    for path in pathlib.Path(tree).rglob("*"):
        yield path


def main(argv=None, embedded=False, debug=None):
    """Drive the validator.
    This function acts as the command line interface backend.
    There is some duplication to support testability.
    """
    debug = debug is not None
    init_logger(level=logging.DEBUG if debug else None)
    argv = argv if argv else sys.argv[1:]
    if not argv:
        print("Usage: gelee paths-to-files")
        return 0
    num_args = len(argv)
    LOG.debug(f"guarded dispatch {argv=}, {num_args=}")
    for tree in argv:
        for path in visit(tree):
            print(path)
    return 0

