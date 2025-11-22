# CLAUDE.md

- in all interactions and commit messages be extremely concise and sacrifice grammar for the sake of conciseness

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a hybrid Rust/Python library called **upystar** that provides high-performance NEF (NMR Exchange Format) file parsing for scientific applications. It uses PyO3 to create Python bindings for a Rust backend library called "ustar".

**The plan describing how it will be developed is in issue #1 in the github repo upystar**

## Architecture

- **Rust Core** (`src/lib.rs`): Contains PyO3 bindings that expose two main functions:
  - `parse_nef_string()` - Parses NEF content from a string
  - `parse_nef_file()` - Parses NEF content from a file path
- **Python Interface** (`python/upystar/`): Python module that imports and exposes the Rust functions
- **Tests** (`tests/`): Python test suite using pytest
- **Dependencies**: The project depends on an external `ustar` Rust library (located at `../ustar`)

## Development Commands

### Project Management

The management of the project will use the uv tool from astral, which will be used for all parts of the development cycle including
- package management `uv add`
- virtual environment creation 
- build
- release

specific commands:
*   **To add a package:** Use `uv add <package-name>`
*   **To run a script:** Use `uv run <filename.py>`
*   **To run Python code directly:** Use `uv run python3 -c "<code>"`
*   **To install with dependencies:** Use `uv run --with "package_name" python3 -c "<code>"`


### Building
```bash
# Build the Rust extension and install Python package
maturin develop
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_basic_parsing.py
```

**When testing text output prefer snapshots as against bare asserts unless you are testing something simple [a simple value or a line or two of text]. To check snapshots use pytest-snapshot. Snapshots should be stored in tests/snapshots. It is particularly __BAD__ to test text output by making a series of asserts against it**

**Test string formatting: When creating multiline test strings, format them for human readability with proper indentation. Use `textwrap.dedent()` to make them valid. See `test_validate_multiline_nef` as example. Do NOT reformat existing test strings - preserve their human-readable layout.**  

### Code Quality
```bash
# Format Python code
uv format .

# Lint Python code
uv run ruff .

# Type checking
ty .
```

### Installing Development Dependencies
```bash
# Install with development dependencies
uv pip install -e ".[dev]"
```

## File Structure

- `Cargo.toml` - Rust dependencies and library configuration
- `pyproject.toml` - Python packaging, dependencies, and tool configuration
- `src/lib.rs` - Main Rust PyO3 bindings
- `python/upystar/__init__.py` - Python module interface
- `tests/` - Test suite with sample NEF data files
- `target/` - Rust build artifacts (gitignored)

## Key Dependencies

- **Rust**: PyO3 for Python bindings, ustar library for NEF parsing
- **Python**: pytest for testing, maturin for building extensions

## Testing Notes

Tests use temporary files and include both valid and invalid NEF parsing scenarios. Test data files are located in `tests/test_data/`.