"""Unit tests simulating missing optional dependencies."""

import builtins
import contextlib
import importlib
import sys

import pytest
from typer.testing import CliRunner

from workflow_clinic.cli import app
from workflow_clinic.parsers.registry import ParserRegistry


def test_nextflow_parser_raises_import_error_when_groovy_parser_missing(
    monkeypatch, tmp_path
) -> None:
    """Verify that NextflowParser.parse() propagates ModuleNotFoundError when dependency is missing."""
    real_import = builtins.__import__

    def fake_import(name: str, *args, **kwargs):
        if name.startswith(("groovy_parser", "lark")):
            err_msg = f"Mocked missing module: {name}"
            raise ModuleNotFoundError(err_msg, name=name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # Clean cached modules from sys.modules
    for module_name in ["workflow_clinic.parsers.nextflow", "groovy_parser", "lark"]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    # Reset registry state
    ParserRegistry._loaded = False
    if "nextflow" in ParserRegistry._parsers:
        del ParserRegistry._parsers["nextflow"]

    # Trigger registry loader
    parser = ParserRegistry.get_parser("nextflow")

    nf_file = tmp_path / "test.nf"
    nf_file.write_text("process TEST {}", encoding="utf-8")

    try:
        with pytest.raises(ModuleNotFoundError) as exc_info:
            parser.parse(nf_file)

        assert "groovy_parser" in str(exc_info.value) or "lark" in str(exc_info.value)
    finally:
        # Restore normal environment for other tests
        monkeypatch.undo()
        for module_name in [
            "workflow_clinic.parsers.nextflow",
            "groovy_parser",
            "lark",
        ]:
            if module_name in sys.modules:
                del sys.modules[module_name]
        ParserRegistry._loaded = False
        if "nextflow" in ParserRegistry._parsers:
            del ParserRegistry._parsers["nextflow"]
        with contextlib.suppress(ImportError):
            importlib.import_module("workflow_clinic.parsers.nextflow")


def test_cli_raises_actionable_error_when_groovy_parser_missing(
    monkeypatch, tmp_path
) -> None:
    """Verify that CLI output contains instructions to install nextflow when dependency is missing."""
    real_import = builtins.__import__

    def fake_import(name: str, *args, **kwargs):
        if name.startswith(("groovy_parser", "lark")):
            err_msg = f"Mocked missing module: {name}"
            raise ModuleNotFoundError(err_msg, name=name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # Clean cached modules from sys.modules
    for module_name in ["workflow_clinic.parsers.nextflow", "groovy_parser", "lark"]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    # Reset registry state
    ParserRegistry._loaded = False
    if "nextflow" in ParserRegistry._parsers:
        del ParserRegistry._parsers["nextflow"]

    nf_file = tmp_path / "test.nf"
    nf_file.write_text("process TEST {}", encoding="utf-8")

    try:
        runner = CliRunner()
        result = runner.invoke(app, ["examine", str(nf_file)])
        assert result.exit_code == 1

        assert "Parse error: Mocked missing module" in result.output
        assert "pip install" in result.output
        assert "workflow-clinic[nextflow]" in result.output
    finally:
        # Restore normal environment for other tests
        monkeypatch.undo()
        for module_name in [
            "workflow_clinic.parsers.nextflow",
            "groovy_parser",
            "lark",
        ]:
            if module_name in sys.modules:
                del sys.modules[module_name]
        ParserRegistry._loaded = False
        if "nextflow" in ParserRegistry._parsers:
            del ParserRegistry._parsers["nextflow"]
        with contextlib.suppress(ImportError):
            importlib.import_module("workflow_clinic.parsers.nextflow")
