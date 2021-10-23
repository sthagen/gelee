# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-docstring,reimported,unused-import,unused-variable
import logging

import pytest  # type: ignore

import gelee.cli as cli


def test_main_ok_no_args(capsys):
    assert cli.main([], debug=False) == 0
    out, err = capsys.readouterr()
    assert "ok" in out.lower()
    assert not err


def test_main_ok_single_ignore_file_as_arg(caplog, capsys):
    caplog.set_level(logging.INFO)
    assert cli.main(["tests/fixtures/ignore/markdown/empty.md"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err
    assert "ignored 1 non-config file" in caplog.text.lower()


def test_main_ok_single_valid_file_as_arg(capsys):
    assert cli.main(["tests/fixtures/valid/json/empty_object.json"], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err


def test_main_ok_duplicated_single_valid_file_as_args(caplog, capsys):
    caplog.set_level(logging.INFO)
    duplicate = "tests/fixtures/valid/json/empty_object.json"
    assert cli.main([duplicate, duplicate], debug=False) == 0
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err
    assert "starting validation visiting a forest with 1 tree" in caplog.text.lower()
    assert "successfully validated 1 total json file." in caplog.text.lower()
    assert (
        "finished validation of 1 configuration file with 0 failures"
        " visiting 1 path (ignored 0 non-config files in 0 folders)"
    ) in caplog.text.lower()


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


def test_main_nok_single_invalid_empty_csv_file_as_arg_and_abort(caplog, capsys):
    caplog.set_level(logging.ERROR)
    assert cli.main(["tests/fixtures/invalid/csv/empty.csv"], abort=True, debug=False) == 1
    out, err = capsys.readouterr()
    assert not out
    assert not err
    assert "failed validation for path" in caplog.text.lower()


def test_main_nok_single_invalid_file_as_arg_and_abort(caplog, capsys):
    caplog.set_level(logging.ERROR)
    assert cli.main(["tests/fixtures/invalid/ini/missing_section_header.ini"], abort=True, debug=False) == 1
    out, err = capsys.readouterr()
    assert not out
    assert not err
    assert "failed validation for path" in caplog.text.lower()


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
    assert "for now only existing paths accepted." in out.lower()
    assert not err
