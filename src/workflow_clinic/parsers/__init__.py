"""Parser infrastructure for Workflow Clinic.

This package defines the BaseParser abstract class and the ParserRegistry
for registering and dynamically selecting workflow parsers.
"""

from workflow_clinic.parsers.base import BaseParser
from workflow_clinic.parsers.nextflow import NextflowParser
from workflow_clinic.parsers.registry import ParserRegistry

# Register the Nextflow parser unconditionally
ParserRegistry.register("nextflow", NextflowParser)

__all__ = ["BaseParser", "NextflowParser", "ParserRegistry"]
