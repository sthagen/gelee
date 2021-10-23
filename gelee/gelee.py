# -*- coding: utf-8 -*-
# pylint: disable=c-extension-no-member,expression-not-assigned,line-too-long,logging-fstring-interpolation
"""Do the lint."""
import configparser
import csv
import json
import logging
import pathlib
import sys
import typing
from typing import Any, Tuple, Union

import toml
from lxml import etree  # type: ignore
from yaml import load as load_yaml

try:
    from yaml import CLoader as LoaderYaml
except ImportError:
    from yaml import Loader as LoaderYaml  # type: ignore

ENCODING = "utf-8"

APP = "gelee"

LOG = logging.getLogger()  # Temporary refactoring: module level logger
LOG_FOLDER = pathlib.Path("logs")
LOG_FILE = f"{APP}.log"
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO

FAILURE_PATH_REASON = "Failed validation for path %s with error: %s"


@typing.no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global LOG  # pylint: disable=global-statement

    log_format = {
        "format": "%(asctime)s.%(msecs)03d %(levelname)s [%(name)s]: %(message)s",
        "datefmt": "%Y-%m-%dT%H:%M:%S",
        # 'filename': LOG_PATH,
        "level": LOG_LEVEL if level is None else level,
    }
    logging.basicConfig(**log_format)
    LOG = logging.getLogger(APP if name is None else name)
    LOG.propagate = True


def load_xml(document_path: pathlib.Path) -> Tuple[None, str]:
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


@typing.no_type_check
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


@typing.no_type_check
def visit(tree_or_file_path):
    """Visit tree and yield the leaves."""
    thing = pathlib.Path(tree_or_file_path)
    if thing.is_file():
        yield thing
    else:
        for path in thing.rglob("*"):
            yield path


@typing.no_type_check
def slugify(error) -> str:
    """Replace newlines by space."""
    return str(error).replace("\n", "")


def parse_csv(path: pathlib.Path) -> Tuple[bool, str]:
    """Opinionated csv as config parser returning the COHDA protocol."""
    if not path.stat().st_size:
        return False, "ERROR: Empty CSV file"

    with open(path, newline="") as handle:
        try:
            try:
                dialect = csv.Sniffer().sniff(handle.read(1024), ",\t; ")
                handle.seek(0)
            except csv.Error as err:
                if "could not determine delimiter" in str(err).lower():
                    dialect = csv.Dialect()  # type: ignore
                    dialect.delimiter = ","
                    dialect.quoting = csv.QUOTE_NONE
                    dialect.strict = True
                else:
                    return False, slugify(err)
            try:
                reader = csv.reader(handle, dialect)
                for _ in reader:
                    pass
                return True, ""
            except csv.Error as err:
                return False, slugify(err)
        except (Exception, csv.Error) as err:
            return False, slugify(err)


def parse_ini(path: pathlib.Path) -> Tuple[bool, str]:
    """Simple ini as config parser returning the COHDA protocol."""
    config = configparser.ConfigParser()
    try:
        config.read(path)
        return True, ""
    except (
        configparser.NoSectionError,
        configparser.DuplicateSectionError,
        configparser.DuplicateOptionError,
        configparser.NoOptionError,
        configparser.InterpolationDepthError,
        configparser.InterpolationMissingOptionError,
        configparser.InterpolationSyntaxError,
        configparser.InterpolationError,
        configparser.MissingSectionHeaderError,
        configparser.ParsingError,
    ) as err:
        return False, slugify(err)


def parse_json(path: pathlib.Path) -> Union[Any, Tuple[bool, str]]:
    """Simple json as config parser returning the COHDA protocol."""
    return parse_generic(path, json.load)


def parse_toml(path: pathlib.Path) -> Union[Any, Tuple[bool, str]]:
    """Simple toml as config parser returning the COHDA protocol."""
    return parse_generic(path, toml.load)


def parse_xml(path: pathlib.Path) -> Union[Any, Tuple[bool, str]]:
    """Simple xml as config parser returning the COHDA protocol."""
    if not path.stat().st_size:
        return False, "ERROR: Empty XML file"

    xml_tree, message = load_xml(path)
    if xml_tree:
        return True, ""

    return False, slugify(message)


def parse_yaml(path: pathlib.Path) -> Union[Any, Tuple[bool, str]]:
    """Simple yaml as config parser returning the COHDA protocol."""
    return parse_generic(path, load_yaml, {"Loader": LoaderYaml})


@typing.no_type_check
def parse_generic(path: pathlib.Path, loader, loader_options=None) -> Tuple[bool, str]:
    """Simple generic parser proxy."""
    if loader_options is None:
        loader_options = {}
    with open(path, "rt", encoding="utf-8") as handle:
        try:
            _ = loader(handle, **loader_options)
            return True, ""
        except Exception as err:
            return False, slugify(err)


@typing.no_type_check
def process(path, handler, success, failure):
    """Generic processing of path yields a,ended COHDA protocol."""
    valid, message = handler(path)
    if valid:
        return True, message, success + 1, failure

    return False, message, success, failure + 1


@typing.no_type_check
def main(argv=None, abort=False, debug=None):
    """Drive the validator.
    This function acts as the command line interface backend.
    There is some duplication to support testability.
    """
    init_logger(level=logging.DEBUG if debug else None)
    forest = argv if argv else sys.argv[1:]
    if not forest:
        print("Usage: gelee paths-to-files")
        return 0, "USAGE"
    num_trees = len(forest)
    LOG.debug("Guarded dispatch forest=%s, num_trees=%d", forest, num_trees)

    LOG.info(
        "Starting validation visiting a forest with %d tree%s",
        num_trees,
        "" if num_trees == 1 else "s",
    )
    total, folders, ignored, csvs, inis, jsons, tomls, xmls, yamls = (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    failures = 0
    for tree in forest:
        for path in visit(tree):
            LOG.debug(" - path=%s, total=%d", path, total)
            total += 1
            if not path.is_file():
                folders += 1
                continue

            final_suffix = "" if not path.suffixes else path.suffixes[-1].lower()

            if final_suffix == ".csv":
                valid, message, csvs, failures = process(path, parse_csv, csvs, failures)
            elif final_suffix == ".ini":
                valid, message, inis, failures = process(path, parse_ini, inis, failures)
            elif final_suffix in (".geojson", ".json"):
                valid, message, jsons, failures = process(path, parse_json, jsons, failures)
            elif final_suffix == ".toml":
                valid, message, tomls, failures = process(path, parse_toml, tomls, failures)
            elif final_suffix == ".xml":
                valid, message, xmls, failures = process(path, parse_xml, xmls, failures)
            elif final_suffix in (".yaml", ".yml"):
                valid, message, yamls, failures = process(path, parse_yaml, yamls, failures)
            else:
                ignored += 1
                continue

            if not valid:
                LOG.error(FAILURE_PATH_REASON, path, message)
            if abort:
                return 1, message

    success = "Successfully validated"
    pairs = (
        (csvs, "CSV"),
        (inis, "INI"),
        (jsons, "JSON"),
        (tomls, "TOML"),
        (xmls, "XML"),
        (yamls, "YAML"),
    )
    for count, kind in pairs:
        if count:
            LOG.info(
                "- %s %d total %s file%s.",
                success,
                count,
                kind,
                "" if count == 1 else "s",
            )

    configs = csvs + inis + jsons + tomls + xmls + yamls
    LOG.info(  # TODO remove f-strings also here
        f"Finished validation of {configs} configuration file{'' if configs == 1 else 's'}"
        f" with {failures} failure{'' if failures == 1 else 's'}"
        f" visiting {total} path{'' if total == 1 else 's'}"
        f" (ignored {ignored} non-config file{'' if ignored == 1 else 's'}"
        f" in {folders} folder{'' if folders == 1 else 's'})"
    )
    print(f"{'OK' if not failures else 'FAIL'}")

    return 0, ""
