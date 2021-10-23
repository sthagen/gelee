#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Validate configuration files against their format and maybe schema."""
import os
import pathlib
import sys
import typing
from typing import List

import typer

import gelee
import gelee.gelee as lint

DEBUG_VAR = "GELEE_DEBUG"
DEBUG = bool(os.getenv(DEBUG_VAR))

ABORT_VAR = "GELEE_ABORT"
ABORT = bool(os.getenv(ABORT_VAR))

APP_NAME = 'Gelee - a finer confiture.'
APP_ALIAS = 'gelee'
app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the gelee version and exit',
        is_eager=True,
    )
) -> None:
    """
    Gelee - a finer confiture.

    Validate configuration files against their format and maybe schema.
    """
    if version:
        typer.echo(f'{APP_NAME} version {gelee.__version__}')
        raise typer.Exit()


@app.command('cook')
def cook(
    unique_trees: List[pathlib.Path],
    abort: bool = typer.Option(
        False,
        '-a',
        '--abort',
        help='Flag to abort execution on first fail (default is False)',
        metavar='bool',
    ),
    debug: bool = typer.Option(
        False,
        '-d',
        '--debug',
        help='Flag to debug execution by adding more context info (default is False)',
        metavar='bool',
    ),
) -> int:
    """
    Cook the gelee from the files in the tree below path.
    """
    return sys.exit(main(unique_trees, abort=abort, debug=debug))


@app.command('version')
def app_version() -> None:
    """
    Display the gelee version and exit
    """
    callback(True)


# pylint: disable=expression-not-assigned
# @app.command()
@typing.no_type_check
def main(argv=None, abort=None, debug=None):
    """Dispatch processing of the job.
    This is the strings only command line interface.
    For python API use interact with lint functions directly.
    """
    argv = sys.argv[1:] if argv is None else argv
    debug = debug if debug else DEBUG
    abort = abort if abort else ABORT
    unique_trees = {arg: None for arg in argv}
    for tree_or_leaf in unique_trees:
        if not pathlib.Path(tree_or_leaf).is_file() and not pathlib.Path(tree_or_leaf).is_dir():
            print("ERROR: For now only existing paths accepted.")
            sys.exit(2)

    code, _ = lint.main(unique_trees, abort=abort, debug=debug)
    return code
