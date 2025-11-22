"""
uPyStar: High-performance Python library for parsing NEF files using USTAR Rust backend.

This library provides both SAS (event-driven) and dict-of-dict interfaces for accessing
NEF (NMR Exchange Format) files with the performance of Rust and convenience of Python.
"""

__version__ = "0.1.0"

from ._core import validate_star_file, validate_star_string  # ty: ignore unresolved-import

__all__ = [
    "validate_star_string",
    "validate_star_file",
]
