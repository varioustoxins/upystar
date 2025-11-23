"""Basic and comprehensive validation tests for upystar STAR parsing functionality."""

import os
import tempfile

# from os import walk
from pathlib import Path
from string import digits

# from textwrap import dedent
import pytest
from upystar import validate_star_file  # , validate_star_string

# Test data directory from ustar project
USTAR_STAR_ROOT = Path("../ustar/tests/test_data")
USTAR_STAR_EXAMPLES = USTAR_STAR_ROOT / "star_examples"
USTAR_STAR_SPEC = USTAR_STAR_ROOT / "star_spec"
STAR_SUFFIXES = {".star", ".cif", ".str", ".nef", ".dic"}
BAD_STAR_FILES = {"warning.cif", "warning.str", "loop4.str", "loop5.str", "mmcif_nef.dic"}


# def test_validate_simple_star_string():
#     """Test parsing a simple STAR/STAR format string."""
#     star_content = 'data_test\n_item "hello world"'
#     result = validate_star_string(star_content)

#     assert result == "Parsed successfully: rule=star_file, span=0-29"


# def test_validate_multiline_star():
#     """Test parsing a multi-line STAR format with loops."""
#     star_content = """
#             data_test
#                 _item_1 "value1"
#                 _item_2 42

#                 loop_
#                     _column_1
#                     _column_2
#                     row1col1 "row1col2"
#                     "row2col1" row2col2
#                 stop_
#         """

#     result = validate_star_string(star_content)
#     assert result == "Parsed successfully: rule=star_file, span=0-276"


def test_validate_star_file():
    """Test parsing STAR content from a file."""
    star_content = """
        data_file_test
            _file_item "test value"
    """

    # Ensure Windows line endings on windows line endings for consistent testing
    if os.name == "nt":  # Windows
        star_content = star_content.replace("\n", "\r\n")

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".star", delete=False) as f:
        f.write(star_content.encode("utf-8"))
        temp_path = f.name

    try:
        file_length = len(star_content)

        result = validate_star_file(temp_path)
        expected = f"Parsed file '{temp_path}' successfully: rule=star_file, span=0-{file_length}"
        assert result == expected

    finally:
        os.unlink(temp_path)


# def test_validate_empty_string():
#     """Test parsing empty string."""
#     result = validate_star_string("")
#     assert "Parsed successfully" in result


# def test_validate_invalid_syntax():
#     """Test parsing invalid STAR syntax."""
#     with pytest.raises(ValueError):
#         validate_star_string("invalid [ syntax here")


# def test_validate_nonexistent_file():
#     """Test parsing non-existent file."""
#     with pytest.raises(OSError):
#         validate_star_file("/nonexistent/file.star")


# def test_validate_semicolon_text():
#     """Test parsing semicolon-bounded text."""
#     star_content = """
#         data_test
#             _long_text
#         ;
#         This is some text
#         with multiple lines
#         ;
#     """
#     star_content = dedent(star_content)

#     result = validate_star_string(star_content)
#     assert result == "Parsed successfully: rule=star_file, span=0-68"


# could do with a better selection of files here Sec5Part4 a dictionary a bmrb file a ciff file and anmmcif file
@pytest.mark.parametrize(
    "star_file",
    [
        "comprehensive_example_crlf.star",
        "comprehensive_example.star",
        "nef_spec/CCPN_Sec5Part3.nef",
        "cod_cif_files/cod_1556498.cif",
        "dicts/mmcif_pdbx_v5_next.dic",
        "pdb_mmcifs/2o65.cif",
    ],
)
def test_comprehensive_star_examples(star_file):
    """Test validation of real STAR example files from ustar."""
    import os

    # Debug: List directory contents on Windows
    if os.name == "nt":
        print("\n=== Windows Debug Info ===")
        print(f"Current working directory: {os.getcwd()}")
        print(f"USTAR_STAR_ROOT: {USTAR_STAR_ROOT}")
        print(f"USTAR_STAR_ROOT exists: {USTAR_STAR_ROOT.exists()}")

        # List mounted drives
        import string

        drives = []
        for letter in string.ascii_uppercase:
            if os.path.exists(f"{letter}:"):
                drives.append(f"{letter}:")
        print(f"Available drives: {drives}")

        # List top level of each drive
        for drive in drives:
            print(f"Contents of {drive}\\:")
            try:
                for item in os.listdir(f"{drive}\\"):
                    print(f"  {drive}\\{item}")
            except Exception as e:
                print(f"  Error listing {drive}: {e}")

        # List parent directories
        current_dir = Path(".")
        print(f"Contents of {current_dir.absolute()}:")
        try:
            for item in current_dir.iterdir():
                print(f"  {item}")
        except Exception as e:
            print(f"  Error listing current dir: {e}")

        parent_dir = Path("..")
        print(f"Contents of {parent_dir.absolute()}:")
        try:
            for item in parent_dir.iterdir():
                print(f"  {item}")
        except Exception as e:
            print(f"  Error listing parent dir: {e}")

        parent_dir = Path("../../..")
        print(f"Contents of {parent_dir.absolute()}:")
        try:
            for item in parent_dir.iterdir():
                print(f"  {item}")
        except Exception as e:
            print(f"  Error listing parent dir: {e}")

    file_path = USTAR_STAR_ROOT / star_file

    result = validate_star_file(str(file_path))
    result = result.rstrip(f"{digits}- \n")

    assert result == f"Parsed file '{file_path}' successfully: rule=star_file, span="


# @pytest.mark.slow
# def test_all_available_star_examples_good():
#     """Test all available STAR example files (if present)."""

#     # python 3.9 no Path.walk
#     file_paths_in_root = [Path(info[0]) / file_name for info in walk(USTAR_STAR_ROOT) for file_name in info[-1]]
#     star_file_paths = [path for path in file_paths_in_root if path.suffix in STAR_SUFFIXES]
#     valid_star_file_paths = [path for path in star_file_paths if "bad" not in path.name]
#     valid_star_file_paths = [path for path in star_file_paths if path.name not in BAD_STAR_FILES]

#     for star_file in valid_star_file_paths:
#         try:
#             result = validate_star_file(str(star_file))
#             print(f"validated {star_file}")
#             assert "successfully" in result
#         except Exception as e:
#             print(f"Failed to validate {star_file.name}: {e}")
