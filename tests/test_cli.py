# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import pathlib

import pytest  # type: ignore

import gelee.cli as cli


def test_main_ok_no_args(capsys):
    assert cli.main([], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" in out.lower()
    assert not err


def test_main_ok_single_valid_file_as_arg(capsys):
    assert cli.main(["tests/fixtures/valid/json/empty_object.json"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err


def test_main_ok_tests_fixtures_valid_as_arg(capsys):
    assert cli.main(["tests/fixtures/valid/"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err


def test_main_nok_single_invalid_file_as_arg(capsys):
    assert cli.main(["tests/fixtures/invalid/ini/missing_section_header.ini"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "fail" in out.lower()
    assert not err


def test_main_nok_tests_fixtures_invalid_as_arg(capsys):
    assert cli.main(["tests/fixtures/invalid/"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "fail" in out.lower()
    assert not err


def test_main_nok_bad_arg(capsys):
    with pytest.raises(SystemExit, match="2"):
        cli.main(["non-existing-thing"], debug=False)
    out, err = capsys.readouterr()
    assert "error" in out.lower()
    assert not err
