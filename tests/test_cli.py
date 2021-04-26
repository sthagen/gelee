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


def test_main_ok_tests_fixtures_arg(capsys):
    assert cli.main(["tests/fixtures/"], debug=False) == (0, '')
    out, err = capsys.readouterr()
    assert "usage" not in out.lower()
    assert "ok" in out.lower()
    assert not err


def test_main_nok_bad_arg(capsys):
    with pytest.raises(SystemExit, match="2"):
        cli.main(["non-existing-thing"], debug=False)
    out, err = capsys.readouterr()
    assert "error" in out.lower()
    assert not err
