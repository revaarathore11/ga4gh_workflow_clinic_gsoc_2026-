"""Unit tests simulating missing optional dependencies."""

import builtins

import pytest
from typer.testing import CliRunner

from workflow_clinic.cli import app
from workflow_clinic.exceptions import ParserError
from workflow_clinic.parsers.nextflow import NextflowParser


def test_nextflow_parser_raises_parser_error_when_groovy_parser_missing(
    monkeypatch, tmp_path
) -> None:
    """Verify NextflowParser raises an actionable error if groovy-parser is missing."""
    real_import = builtins.__import__

    def fake_import(name: str, *args, **kwargs):
        if name.startswith("groovy_parser"):
            err_msg = f"Mocked missing module: {name}"
            raise ModuleNotFoundError(err_msg, name="groovy_parser")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    parser = NextflowParser()
    nf_file = tmp_path / "test.nf"
    nf_file.write_text("process TEST {}", encoding="utf-8")

    with pytest.raises(ParserError) as exc_info:
        parser.parse(nf_file)

    assert "Nextflow backend dependencies" in str(exc_info.value)
    assert "groovy-parser" in str(exc_info.value)


def test_cli_raises_actionable_error_when_groovy_parser_missing(
    monkeypatch, tmp_path
) -> None:
    """Verify that CLI output contains instructions to install nextflow when dependency is missing."""
    real_import = builtins.__import__

    def fake_import(name: str, *args, **kwargs):
        if name.startswith("groovy_parser"):
            err_msg = f"Mocked missing module: {name}"
            raise ModuleNotFoundError(err_msg, name="groovy_parser")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    nf_file = tmp_path / "test.nf"
    nf_file.write_text("process TEST {}", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(app, ["examine", str(nf_file)])
    assert result.exit_code == 1

    assert "Parse error: Nextflow backend dependencies" in result.output
    assert "pip install" in result.output
    assert "workflow-clinic[nextflow]" in result.output
