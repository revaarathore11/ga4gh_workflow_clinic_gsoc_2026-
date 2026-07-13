import importlib.metadata
import logging
from pathlib import Path
from typing import ClassVar

from workflow_clinic.exceptions import ParserError, UnsupportedWorkflowError
from workflow_clinic.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class ParserRegistry:
    """Registry for workflow parser management.

    Provides dynamic parser detection and retrieval without hardcoded logic.
    """

    _parsers: ClassVar[dict[str, type[BaseParser]]] = {}
    _loaded: ClassVar[bool] = False

    @classmethod
    def _load_entry_points(cls) -> None:
        """Dynamically load and register parsers defined as entry points."""
        if cls._loaded:
            return
        cls._loaded = True

        try:
            eps = importlib.metadata.entry_points(group="workflow_clinic.parsers")
            for ep in eps:
                try:
                    parser_class = ep.load()
                    cls.register(ep.name, parser_class)
                    logger.debug("Registered parser '%s' from entry point", ep.name)
                except Exception:
                    logger.exception(
                        "Failed to load parser entry point '%s'",
                        ep.name,
                    )
        except Exception:
            logger.exception("Failed to load parser entry points")

    @classmethod
    def register(cls, name: str, parser_class: type[BaseParser]) -> None:
        """Register a parser class with a given name.

        Args:
            name: Unique identifier for the parser (e.g., "nextflow", "snakemake")
            parser_class: Parser class that inherits from BaseParser

        Raises:
            ParserError: If parser_class does not inherit from BaseParser
        """
        if not isinstance(parser_class, type) or not issubclass(
            parser_class, BaseParser
        ):
            parser_name = getattr(parser_class, "__name__", repr(parser_class))
            msg = f"Parser class {parser_name} must inherit from BaseParser"
            raise ParserError(msg)
        cls._parsers[name] = parser_class

    @classmethod
    def detect_parser(cls, path: Path) -> str:
        """Detect which parser can handle the given workflow path.

        Args:
            path: Path to a workflow file or directory

        Returns:
            Name of the parser that can handle this workflow

        Raises:
            ParserError: If path does not exist or is not accessible
            UnsupportedWorkflowError: If no registered parser can handle the workflow
        """
        if not path.exists():
            msg = f"Path does not exist: {path}"
            raise ParserError(msg)

        cls._load_entry_points()

        for parser_name, parser_class in cls._parsers.items():
            if parser_class.can_parse(path):
                return parser_name

        msg = f"No registered parser can handle workflow at: {path}"
        raise UnsupportedWorkflowError(msg)

    @classmethod
    def get_parser(cls, name: str) -> BaseParser:
        """Retrieve a parser instance by name.

        Args:
            name: Name of the registered parser

        Returns:
            Instance of the requested parser

        Raises:
            ParserError: If parser name is not registered
        """
        cls._load_entry_points()

        if name not in cls._parsers:
            available = ", ".join(cls._parsers.keys())
            msg = f"Parser '{name}' not registered. Available parsers: {available}"
            raise ParserError(msg)

        parser_class = cls._parsers[name]
        return parser_class()
