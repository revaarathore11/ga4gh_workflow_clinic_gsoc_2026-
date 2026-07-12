"""Parser infrastructure for Workflow Clinic.

This package defines the BaseParser abstract class and the ParserRegistry
for registering and dynamically selecting workflow parsers.
"""

import logging

from workflow_clinic.parsers.base import BaseParser
from workflow_clinic.parsers.registry import ParserRegistry

logger = logging.getLogger(__name__)

try:
    from workflow_clinic.parsers.nextflow import NextflowParser

    ParserRegistry.register("nextflow", NextflowParser)
except ImportError:
    logger.debug(
        "Nextflow support not installed. "
        "Install with: pip install 'workflow-clinic[nextflow]'"
    )

__all__ = ["BaseParser", "ParserRegistry"]
