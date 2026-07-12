"""Unit tests simulating missing optional dependencies."""

import builtins
import importlib
import sys

import pytest

from workflow_clinic.exceptions import UnsupportedWorkflowError
from workflow_clinic.parsers import ParserRegistry


def test_parser_registry_survives_missing_nextflow_dependency(monkeypatch) -> None:
    """Verify registry imports successfully and handles missing nextflow dependency."""
    real_import = builtins.__import__

    def fake_import(name: str, *args, **kwargs):
        if name.startswith(("groovy_parser", "workflow_clinic.parsers.nextflow")):
            err_msg = f"Mocked missing module: {name}"
            raise ModuleNotFoundError(err_msg)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # Evict parser modules from sys.modules to force a re-import
    evicted = []
    for mod in list(sys.modules):
        if mod.startswith("workflow_clinic.parsers"):
            evicted.append((mod, sys.modules[mod]))
            del sys.modules[mod]

    # Reset registry parsers state
    original_parsers = dict(ParserRegistry._parsers)
    ParserRegistry._parsers.clear()

    try:
        # Re-import parsers package under simulated environment
        importlib.import_module("workflow_clinic.parsers")

        # Nextflow parser should not be registered
        assert "nextflow" not in ParserRegistry._parsers
    finally:
        # Restore original parser registry and modules
        ParserRegistry._parsers.clear()
        ParserRegistry._parsers.update(original_parsers)
        for mod, value in evicted:
            sys.modules[mod] = value


def test_detect_parser_gives_actionable_error_for_missing_extension(tmp_path) -> None:
    """Confirm detect_parser outputs actionable help for missing optional dependencies."""
    # Test file with .nf suffix
    nf_file = tmp_path / "test.nf"
    nf_file.write_text("process TEST {}", encoding="utf-8")

    # Clear registry
    original_parsers = dict(ParserRegistry._parsers)
    ParserRegistry._parsers.clear()

    try:
        with pytest.raises(UnsupportedWorkflowError) as exc_info:
            ParserRegistry.detect_parser(nf_file)
        assert "No parser available for Nextflow workflows" in str(exc_info.value)
        assert "pip install 'workflow-clinic[nextflow]'" in str(exc_info.value)
    finally:
        ParserRegistry._parsers.clear()
        ParserRegistry._parsers.update(original_parsers)
