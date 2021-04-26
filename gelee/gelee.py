# -*- coding: utf-8 -*-
# pylint: disable=c-extension-no-member,expression-not-assigned,line-too-long,logging-fstring-interpolation
"""Do the lint."""
import configparser
import csv
import json
import logging
import os
import pathlib
import sys
import toml
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


def load_xml(document_path):
    """
    Parse the document at path (to ensure it is well-formed XML) to obtain an ElementTree object.
    Return value is an ordered pair of Union(None, ElementTree object) and a message string
    """
    try:
        doc = etree.parse(str(document_path), etree.XMLParser(encoding="utf-8"))
    except IOError as err:
        return None, f"file {document_path} failed with IO error {err}"
    except etree.XMLSyntaxError as err:
        return (
            None,
            f"parsing from {document_path} failed with XMLSyntaxError error {err}",
        )

    return doc, f"well-formed xml tree from {document_path}"


def walk_tree_explicit(base_path):
    """Visit the files in the folders below base path."""
    if base_path.is_file():
        yield base_path
    else:
        for entry in base_path.iterdir():
            if entry.is_dir():
                for file_path in entry.iterdir():
                    yield file_path
            else:
                yield entry


def visit(tree):
    """Visit tree and yield the leaves."""
    for path in pathlib.Path(tree).rglob("*"):
        yield path


def main(argv=None, embedded=False, debug=None):
    """Drive the validator.
    This function acts as the command line interface backend.
    There is some duplication to support testability.
    """
    init_logger(level=logging.DEBUG if debug else None)
    forest = argv if argv else sys.argv[1:]
    if not forest:
        print("Usage: gelee paths-to-files")
        return 0
    num_trees = len(forest)
    LOG.debug(f"Guarded dispatch {forest=}, {num_trees=}")
    total, folders, ignored, csvs, inis, jsons, tomls, xmls = 0, 0, 0, 0, 0, 0, 0, 0
    for tree in forest:
        for path in visit(tree):
            LOG.debug(f" - {path=}, {total=}")
            total += 1
            if not path.is_file():
                folders += 1
                continue

            final_suffix = path.suffixes[-1].lower()

            if final_suffix == ".csv":
                csvs += 1
                with open(path, newline='') as handle:
                    try:
                        dialect = csv.Sniffer().sniff(handle.read(1024), ",\t; ")
                        handle.seek(0)
                    except csv.Error as err:
                        if "could not determine delimiter" in str(err).lower():
                            dialect = csv.Dialect()
                            dialect.delimiter = ','
                            dialect.quoting = csv.QUOTE_NONE
                            dialect.strict = True
                        else:
                            return 1, str(err)
                    try:
                        reader = csv.reader(handle, dialect)
                        for _ in reader:
                            pass
                    except csv.Error as err:
                        return 1, str(err)
            elif final_suffix == ".ini":
                inis += 1
                config = configparser.ConfigParser()
                try:
                    config.read(path)
                except configparser.NoSectionError as err:
                    return 1, str(err)
                except configparser.DuplicateSectionError as err:
                    return 1, str(err)
                except configparser.DuplicateOptionError as err:
                    return 1, str(err)
                except configparser.NoOptionError as err:
                    return 1, str(err)
                except configparser.InterpolationDepthError as err:
                    return 1, str(err)
                except configparser.InterpolationMissingOptionError as err:
                    return 1, str(err)
                except configparser.InterpolationSyntaxError as err:
                    return 1, str(err)
                except configparser.InterpolationError as err:
                    return 1, str(err)
                except configparser.MissingSectionHeaderError as err:
                    return 1, str(err)
                except configparser.ParsingError as err:
                    return 1, str(err)
            elif final_suffix in (".geojson", ".json"):
                jsons += 1
                with open(path, "rt", encoding="utf-8") as handle:
                    try:
                        _ = json.load(handle)
                    except Exception as err:
                        return 1, str(err)
            elif final_suffix == ".toml":
                tomls += 1
                with open(path, "rt", encoding="utf-8") as handle:
                    try:
                        _ = toml.load(handle)
                    except Exception as err:
                        return 1, str(err)
            elif final_suffix == ".xml":
                xmls += 1
                xml_tree, message = load_xml(path)
                if not xml_tree:
                    LOG.error(message)
                    return 1, "ERROR"
            else:
                ignored += 1
                continue

    if csvs:
        LOG.info(
            "Validated %d total CSV file%s in %d folder%s (ignored %d non-config file%s)",
            csvs,
            "" if csvs == 1 else "s",
            folders,
            "" if folders == 1 else "s",
            ignored,
            "" if ignored == 1 else "s",
        )
    if inis:
        LOG.info(
            "Validated %d total INI file%s in %d folder%s (ignored %d non-config file%s)",
            inis,
            "" if inis == 1 else "s",
            folders,
            "" if folders == 1 else "s",
            ignored,
            "" if ignored == 1 else "s",
        )
    if jsons:
        LOG.info(
            "Validated %d total JSON file%s in %d folder%s (ignored %d non-config file%s)",
            jsons,
            "" if jsons == 1 else "s",
            folders,
            "" if folders == 1 else "s",
            ignored,
            "" if ignored == 1 else "s",
        )
    if tomls:
        LOG.info(
            "Validated %d total TOML file%s in %d folder%s (ignored %d non-config file%s)",
            tomls,
            "" if tomls == 1 else "s",
            folders,
            "" if folders == 1 else "s",
            ignored,
            "" if ignored == 1 else "s",
        )
    if xmls:
        LOG.info(
            "Validated %d total XML file%s in %d folder%s (ignored %d non-config file%s)",
            xmls,
            "" if xmls == 1 else "s",
            folders,
            "" if folders == 1 else "s",
            ignored,
            "" if ignored == 1 else "s",
        )

    configs = csvs + inis + jsons + tomls + xmls
    LOG.info(f"Finished validation of {configs} configuration files visited {total} paths")
    print("OK")

    return 0, ""

