"""Entrypoint and validation script for make.fun competition 'news-summary-01'.

This script copies the pre-generated news summary (`summary.txt`) to the target
destination defined by the $MAKEFUN_OUTPUT_DIR environment variable (defaulting to
`/output/entry.txt`) and validates that the output file meets competition requirements:
valid UTF-8 encoding and character count between 1 and 2,000 characters.
"""

import os
import shutil
import sys
from pathlib import Path

MIN_CHARACTERS = 1
MAX_CHARACTERS = 2000


def get_target_path() -> Path:
    """Resolve the destination path from the MAKEFUN_OUTPUT_DIR environment variable.

    Returns:
        Path: Resolved absolute or relative path to the entry output file.
    """
    out_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_env:
        return Path("/output/entry.txt")

    p = Path(out_env)
    if p.suffix == ".txt" or p.name.endswith(".txt"):
        return p
    return p / "entry.txt"


def validate_entry_file(path: Path) -> str:
    """Validate that the target file is UTF-8 encoded and within character limits.

    Args:
        path: Path to the target file to validate.

    Returns:
        str: Decoded UTF-8 content of the file.

    Raises:
        FileNotFoundError: If the target file does not exist.
        UnicodeDecodeError: If the file is not valid UTF-8.
        ValueError: If character count is not between 1 and 2,000 characters.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Target file does not exist: {path}")

    # Read raw bytes and verify strict UTF-8 decoding
    raw_bytes = path.read_bytes()
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as err:
        raise UnicodeDecodeError(
            err.encoding,
            err.object,
            err.start,
            err.end,
            f"Output file {path} is not valid UTF-8: {err}",
        ) from err

    char_count = len(content)
    if not (MIN_CHARACTERS <= char_count <= MAX_CHARACTERS):
        raise ValueError(
            f"Validation failed: character count {char_count} out of range "
            f"[{MIN_CHARACTERS}, {MAX_CHARACTERS}] for {path}."
        )

    return content


def copy_and_validate(src_path: Path, dest_path: Path) -> None:
    """Copy the source summary to the destination and validate the output.

    Args:
        src_path: Source summary file path.
        dest_path: Destination entry file path.
    """
    if not src_path.is_file():
        raise FileNotFoundError(f"Source summary file not found: {src_path}")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src_path, dest_path)
    print(f"Copied source from {src_path} to {dest_path}")

    content = validate_entry_file(dest_path)
    print(
        f"Validation passed for {dest_path}: UTF-8 verified, "
        f"{len(content)} characters (allowed: {MIN_CHARACTERS}-{MAX_CHARACTERS})."
    )


def main() -> None:
    """Main execution entrypoint."""
    base_dir = Path(__file__).resolve().parent
    src_file = base_dir / "summary.txt"
    target_path = get_target_path()

    try:
        copy_and_validate(src_file, target_path)
    except Exception as exc:
        print(f"Error during entry generation or validation: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
